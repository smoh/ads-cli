from prompt_toolkit import Application, HTML
from prompt_toolkit.buffer import Buffer, reshape_text
from prompt_toolkit.layout.containers import VSplit, HSplit, Window
from prompt_toolkit.layout.controls import BufferControl, FormattedTextControl
from prompt_toolkit.layout.layout import Layout
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.application import get_app
from prompt_toolkit.styles import Style
from prompt_toolkit.key_binding.bindings.focus import focus_next, focus_previous
from prompt_toolkit.shortcuts import message_dialog
from prompt_toolkit import PromptSession
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
from prompt_toolkit.completion import WordCompleter
import webbrowser
import pickle
import ads

ads_query_completer = WordCompleter(
    ["author", "first_author", "year", "property", "title"], ignore_case=True
)

# dummy content to format stuff
with open("dump.pkl", "rb") as f:
    q = pickle.load(f)

kb = KeyBindings()
kb_search = KeyBindings()
kb_output = KeyBindings()

kb_output.add("j")(focus_next)
kb_output.add("k")(focus_previous)


@kb.add("c-d")
def exit_(event):
    """
    Pressing Ctrl-Q will exit the user interface.

    Setting a return value means: quit the event loop that drives the user
    interface and return this value from the `Application.run()` call.
    """
    event.app.exit(result=[result, duh])


@kb_output.add("n")
def next_(event):
    """
    Pressing Ctrl-Q will exit the user interface.

    Setting a return value means: quit the event loop that drives the user
    interface and return this value from the `Application.run()` call.
    """
    app.page += 1
    n = app.page
    items = []
    for i in range(10 * n, 10 * (n + 1)):
        w = Window(
            height=2,
            content=FormattedTextControl(
                focusable=True,
                text=HTML(
                    f"{i:2d} {q.articles[i].title[0][:]}\n"
                    f"   <u>{q.articles[i].first_author}</u>"
                    f"{q.articles[i].year} {q.articles[i].bibcode}"
                ),
            ),
        )
        w.bibcode = q.articles[i].bibcode
        items.append(w)
    event.app.layout.container.children = [
        Window(height=3, content=BufferControl(buffer=buffer1)),
        *items,
    ]
    event.app.layout.focus(items[0])


@kb_search.add("c-j")
def go_to_output(event):
    event.app.layout.focus(event.app.layout.container.children[1])


@kb_search.add("c-s")
def search_(event):
    q = buffer1.text
    duh.append(q)
    q = ads.SearchQuery(q=q)
    list(q)

    items = []
    for i in range(min([10, len(q.articles)])):
        w = Window(
            height=2,
            content=FormattedTextControl(
                focusable=True,
                text=HTML(
                    f"{i:2d} {q.articles[i].title[0][:]}\n"
                    f"   <u>{q.articles[i].first_author}</u>"
                    f"{q.articles[i].year} {q.articles[i].bibcode}"
                ),
            ),
        )
        w.bibcode = q.articles[i].bibcode
        items.append(w)
    output.children = items
    event.app.layout.focus(output)


@kb_output.add("c")
def select_(event):
    # event.app.layout.current_window.content = FormattedTextControl(text="dksjfksdjf")
    # event.app.layout.current_window.style = "bg:red"
    cw = event.app.layout.current_window
    # event.app.get_parent(cw).style = "bg:blue"
    if cw.bibcode in result:
        cw.style = "bg:"
        cw.content.style = "bg:"
        result.discard(cw.bibcode)
    else:
        cw.style = "bg:blue"
        cw.content.style = "bg:blue"
        result.add(cw.bibcode)


@kb_output.add("o")
def select_(event):
    # event.app.layout.current_window.content = FormattedTextControl(text="dksjfksdjf")
    # event.app.layout.current_window.style = "bg:red"
    cw = event.app.layout.current_window
    url = f"https://ui.adsabs.harvard.edu/abs/{cw.bibcode}"
    webbrowser.open_new_tab(url)


@kb_output.add("p")
def select_(event):
    # event.app.layout.current_window.content = FormattedTextControl(text="dksjfksdjf")
    # event.app.layout.current_window.style = "bg:red"
    cw = event.app.layout.current_window
    url = f"https://ui.adsabs.harvard.edu/link_gateway/{cw.bibcode}/PUB_PDF"
    webbrowser.open_new_tab(url)


@kb_output.add("a")
def select_(event):
    cw = event.app.layout.current_window
    bibcode = cw.bibcode
    q = ads.SearchQuery(q=f"bibcode:{bibcode}", fl="abstract")
    abstract = q.next().abstract
    # duh.append(abstract)
    # event.app.layout.container.children[0].content.content = "fudksdjfdksj"
    statusbar.body.content.text = abstract
    # reshape_text(buffer1)
    # message_dialog(title="sdlkfj", text="lorem")


buffer1 = Buffer(
    completer=ads_query_completer, complete_while_typing=True
)  # Editable buffer.
searchbar = Frame(
    title="Search",
    body=HSplit(
        [Window(height=3, content=BufferControl(buffer=buffer1), wrap_lines=True)]
    ),
    key_bindings=kb_search,
)

output = HSplit([], key_bindings=kb_output)

statusbar = Frame(
    Window(wrap_lines=True, height=0, content=FormattedTextControl(text="abcde"))
)

result = set()
duh = []
# page = 0


items = []
for i in range(10):
    w = Window(
        height=2,
        content=FormattedTextControl(
            focusable=True,
            text=HTML(
                f"{i:2d} {q.articles[i].title[0]}\n"
                f"   <u>{q.articles[i].first_author}</u>"
                f"{q.articles[i].year} {q.articles[i].bibcode}"
            ),
        ),
    )
    w.bibcode = q.articles[i].bibcode
    items.append(w)
output.children = items

root_container = HSplit([searchbar, output, statusbar])
layout = Layout(root_container)
app = Application(layout=layout, full_screen=True, key_bindings=kb)
app.page = 0


def run():
    result = app.run()
    print(result)


if __name__ == "__main__":
    run()
