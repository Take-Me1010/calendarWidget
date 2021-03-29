
from logging import root

from kivy.uix.boxlayout import BoxLayout
from kivycalendarwidget import KivyCalendarWidget
from kivycalendarwidget.colors import ColorTheme, KivyColors

from kivy.app import App


class MyThemeCalendarApp(App):
    def __init__(self, **kwargs):
        super(MyThemeCalendarApp, self).__init__(**kwargs)
        
    def build(self):
        # You can customize calendar appearance easily by using ColorTheme(NamedTuple).
        MyTheme = ColorTheme(
            background_color=KivyColors.SKY_BLUE,
            header_background=KivyColors.AQUA_GREEN,
            nowdays_background=KivyColors.WHITE,
            nowdays_color=KivyColors.BLACK,
            previousdays_background=KivyColors.SKY_GRAY,
            nextdays_background=KivyColors.SKY_GRAY
        )
        
        c = KivyCalendarWidget(theme=MyTheme)
        self.root = BoxLayout()
        self.root.add_widget(c)
        
        return self.root


def main():
    MyThemeCalendarApp().run()


if __name__ == '__main__':
    main()

