from __future__ import unicode_literals
from prompt_toolkit import Application, HTML
from prompt_toolkit.buffer import Buffer
from prompt_toolkit.layout.containers import HSplit, Window, FloatContainer, Float
from prompt_toolkit.layout.controls import BufferControl, FormattedTextControl
from prompt_toolkit.layout.layout import Layout
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit import PromptSession
from prompt_toolkit.layout.menus import CompletionsMenu
from prompt_toolkit.widgets import (
    Box,
    Button,
    Checkbox,
    Dialog,
    Frame,
    Label,
    MenuContainer,
    MenuItem,
    ProgressBar,
    RadioList,
    TextArea,
)
from prompt_toolkit.layout.controls import SearchBufferControl
from prompt_toolkit.completion import WordCompleter
import webbrowser
import html
import ads

from ads_variables import ads_query_completer

# fields to get from query
_fl = [
    "title",
    "bibcode",
    "author",
    "first_author",
    "year",
    "abstract",
    "citation_count",
    "read_count",
]


# Define UI
kb = KeyBindings()
kb_search = KeyBindings()
kb_output = KeyBindings()

infoFrame = Frame(
    Window(wrap_lines=True, height=10, content=FormattedTextControl(text=""))
)
output = HSplit([])


# import pickle
# dummy content to format stuff
# with open("dump.pkl", "rb") as f:
#     q = pickle.load(f)


buffer1 = Buffer(
    completer=ads_query_completer, complete_while_typing=True
)  # Editable buffer.

statusbar = Window(
    FormattedTextControl('Press "c-d" to quit.'), height=1, style="reverse"
)

searchbar = FloatContainer(
    content=HSplit(
        [statusbar, Window(height=4, content=BufferControl(buffer=buffer1))],
        key_bindings=kb_search,
    ),
    floats=[
        Float(
            xcursor=True,
            ycursor=True,
            content=CompletionsMenu(max_height=3, scroll_offset=1),
        )
    ],
)

# Put it all together
root_container = HSplit([searchbar, output, infoFrame])
layout = Layout(root_container)
app = Application(layout=layout, full_screen=True, key_bindings=kb)

# These are app-wide stateful variables; not sure how to structure things.
app.ads_q = None  # either None or ads.SearchQuery
app.ads_page = 0  # current page
app.ads_item_idx = 0  # current item index within page
app.NITEMS = 5  # number of items per page
app.pages = None  # chunked list of articles (list of lists)


def format_article_info(article):
    """Format current article's info for infoFrame"""
    return HTML(
        f"<b>{html.escape(article.title[0])}</b>\n"
        f"{html.escape('; '.join(article.author[:3]))}\n"
        "<seagreen>Citations:</seagreen> "
        f"{article.citation_count}\n"
        "<seagreen>Read count:</seagreen> "
        f"{article.read_count}\n"
        "<seagreen>Abstract:</seagreen>\n"
        f"{article.abstract}"
    )


def get_entries(articles):
    """Returns a list of Windows each containing one article"""
    items = []
    for i, a in enumerate(articles):
        w = Window(
            height=2,
            content=FormattedTextControl(
                focusable=True,
                text=HTML(
                    f"{i:2d} <skyblue>{html.escape(a.title[0])}</skyblue>\n"
                    f"   <violet>{html.escape('; '.join(a.author[:3]))}</violet> "
                    f"<gray>{a.year}</gray> "
                    f"{html.escape(a.bibcode)}"
                ),
            ),
        )
        w.bibcode = a.bibcode
        items.append(w)
    return items


@kb_output.add("j")
def next_entry(event):
    """Go to next entry"""
    q = event.app.ads_q
    event.app.layout.focus_next()
    app = event.app
    if app.ads_item_idx != 4:
        app.ads_item_idx += 1
        idx = app.NITEMS * app.ads_page + app.ads_item_idx
        infoFrame.body.content.text = format_article_info(q.articles[idx])


@kb_output.add("k")
def previous_entry(event):
    """Go to previous entry"""
    q = event.app.ads_q
    event.app.layout.focus_previous()
    app = event.app
    if app.ads_item_idx != 0:
        app.ads_item_idx -= 1
        idx = app.NITEMS * app.ads_page + app.ads_item_idx
        infoFrame.body.content.text = format_article_info(q.articles[idx])


@kb.add("c-d")
def exit_(event):
    """
    Pressing Ctrl-D will exit the user interface.

    Setting a return value means: quit the event loop that drives the user
    interface and return this value from the `Application.run()` call.
    """
    event.app.exit(result=None)


@kb_output.add("l")
def next_page(event):
    """Go to next page
    """
    app = event.app
    try:
        items = get_entries(app.pages[app.ads_page + 1])
        app.ads_page += 1
    except IndexError:
        return
    event.app.layout.container.children[1].children = items
    event.app.layout.focus(items[0])
    infoFrame.body.content.text = format_article_info(app.pages[app.ads_page][0])


@kb_output.add("h")
def previous_page(event):
    """Go to previous page
    """
    app = event.app
    if app.ads_page == 0:
        return
    app.ads_page -= 1
    items = get_entries(app.pages[app.ads_page])
    event.app.layout.container.children[1].children = items
    event.app.layout.focus(items[0])
    infoFrame.body.content.text = format_article_info(app.pages[app.ads_page][0])


@kb_search.add("c-j")
def go_to_output(event):
    event.app.layout.focus(event.app.layout.container.children[1])


@kb_search.add("c-s")
def send_query(event):
    """Do an ADS search"""
    query = buffer1.text
    q = ads.SearchQuery(q=query, fl=_fl)
    # this can be empty
    #
    try:
        list(q)
    except (
        ads.exceptions.APIResponseError,
        ads.exceptions.SolrResponseParseError,
    ) as e:
        statusbar.content.text = "Boom! Your query failed."
        return
    if len(q.articles) == 0:
        statusbar.content.text = "Your query returned nothing."
        return
    app = event.app
    app.ads_q = q

    def chunks(l, n):
        """Yield successive n-sized chunks from l."""
        for i in range(0, len(l), n):
            yield l[i : i + n]

    app.pages = list(chunks(q.articles, app.NITEMS))

    app.ads_page = 0
    items = get_entries(app.pages[0])
    event.app.layout.container.children[1].children = items
    event.app.layout.focus(items[0])
    infoFrame.body.content.text = format_article_info(app.pages[app.ads_page][0])


@kb_output.add("o")
def select_(event):
    cw = event.app.layout.current_window
    url = f"https://ui.adsabs.harvard.edu/abs/{cw.bibcode}"
    webbrowser.open_new_tab(url)


@kb_output.add("p")
def select_(event):
    cw = event.app.layout.current_window
    url = f"https://ui.adsabs.harvard.edu/link_gateway/{cw.bibcode}/PUB_PDF"
    webbrowser.open_new_tab(url)


@kb_output.add("e")
def select_(event):
    cw = event.app.layout.current_window
    url = f"https://ui.adsabs.harvard.edu/link_gateway/{cw.bibcode}/EPRINT_PDF"
    webbrowser.open_new_tab(url)


output.key_bindings = kb_output
output.children = [
    Window(
        FormattedTextControl('Input query and press "<CTRL-S>" to run.'),
        height=1,
        style="reverse",
    )
]


def run():
    app.run()


if __name__ == "__main__":
    run()
