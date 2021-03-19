from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.lang.builder import Builder
Builder.load_string('''
#<KvLang>
# Define your background color Template
<BackgroundColor>
    background_color: 1, 1, 1, 1
    canvas.before:
        Color:
            rgba: root.background_color
        Rectangle:
            size: self.size
            pos: self.pos
# Now you can simply Mix the `BackgroundColor` class with almost
# any other widget... to give it a background.
<BackgroundLabel>
    background_color: 0, 0, 0, 0
    # Default the background color for this label
    # to r 0, g 0, b 0, a 0
<BackgroundButton>:
    background_color: 0, 0, 0, 0
    background_normal: ''
    # background_down: ''
#</KvLang>
''')
class BackgroundColor(Widget):
    pass

class BackgroundLabel(Label, BackgroundColor):
    pass

class BackgroundButton(Button, BackgroundColor):
    pass

