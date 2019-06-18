from prompt_toolkit import Application, HTML
from prompt_toolkit.buffer import Buffer
from prompt_toolkit.layout.containers import VSplit, HSplit, Window
from prompt_toolkit.layout.controls import BufferControl, FormattedTextControl
from prompt_toolkit.layout.layout import Layout
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.application import get_app
from prompt_toolkit.styles import Style
from prompt_toolkit.key_binding.bindings.focus import focus_next, focus_previous
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


import pickle

with open("dump.pkl", "rb") as f:
    q = pickle.load(f)

kb = KeyBindings()

buffer1 = Buffer()  # Editable buffer.


@kb.add("q")
def exit_(event):
    """
    Pressing Ctrl-Q will exit the user interface.

    Setting a return value means: quit the event loop that drives the user
    interface and return this value from the `Application.run()` call.
    """
    event.app.exit()


@kb.add("a")
def exit_(event):
    """
    Pressing Ctrl-Q will exit the user interface.

    Setting a return value means: quit the event loop that drives the user
    interface and return this value from the `Application.run()` call.
    """
    get_app().layout.focus(items[0])


kb_elem = KeyBindings()
kb.add("j")(focus_next)
kb.add("k")(focus_previous)


selected_style = Style.from_dict({"window.border": "#238400"})


@kb_elem.add("c")
def select_(event):
    # event.app.layout.current_window.content = FormattedTextControl(text="dksjfksdjf")
    # event.app.layout.current_window.style = "bg:red"
    event.app.layout.current_window.style = "bg:blue"


items = [
    Window(
        height=2,
        content=FormattedTextControl(
            focusable=True,
            text=HTML(
                f"{i:2d} {q.articles[i].title[0][:85]}\n"
                f"   <u>{q.articles[i].first_author}</u> {q.articles[i].year} {q.articles[i].bibcode}"
            ),
            key_bindings=kb_elem,
        ),
    )
    for i in range(10)
]

boxes = [
    Checkbox(
        text=HTML(
            f"{i:2d} {q.articles[i].title[0][:85]}\n"
            f"   <u>{q.articles[i].first_author}</u> {q.articles[i].year} {q.articles[i].bibcode}"
        )
    )
    for i in range(10)
]

checkbox1 = Checkbox(text="Checkbox")
checkbox2 = Checkbox(text="Checkbox")


root_container = HSplit(
    [
        # One window that holds the BufferControl with the default buffer on
        # the left.
        # Window(height=3, content=BufferControl(buffer=buffer1)),
        # A vertical line in the middle. We explicitly specify the width, to
        # make sure that the layout engine will not try to divide the whole
        # width by three for all these windows. The window will simply fill its
        # content by repeating this character.
        # Window(char="-"),
        # Display the text 'Hello world' on the right.
        Frame(body=HSplit(items)),
        # *items,
        # checkbox1,
        # checkbox2,
        # VSplit([Frame(title="clsdkjf", body=HSplit(boxes))]),
    ]
)

layout = Layout(root_container)

app = Application(layout=layout, full_screen=False, key_bindings=kb)
app.run()  # You won't be able to Exit this app

