
from typing import List

from kivy.app import App

from kivy.uix.boxlayout import BoxLayout

from kivycalendarwidget import KivyCalendarWidget, DateCell
from kivycalendarwidget.colors import CalenderThemes


class TestApp(App):
    def __init__(self, **kwargs):
        super(TestApp, self).__init__(**kwargs)
        
    def build(self):
        self.root = BoxLayout()
        monthsEnglish: List[str] = [
            'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'
        ]
        # monthFormat must be List[str] whose length is 12 or str which contains ${month}
        # if List[str], its order must correspond to 1-12 month.
        # if str, ${month} is replaced an actual month; 1-12.
        monthFormat: List[str] = monthsEnglish
        
        c = KivyCalendarWidget(do_highlight_pressed_day=True, do_deselect_double_pressed_day=True, monthFormat=monthFormat)
        c.bind(
            on_previous_month=self._on_pre,
            on_next_month=self._on_next,
            on_day_select=self._on_select_day,
            on_day_deselect=self._on_deselect_day
        )
        # load theme. if no theme given, default theme (dark) used.
        c.load_theme(CalenderThemes.LIGHT_THEME)
        
        self.root.add_widget(c)
        return self.root

    def _on_pre(self, instance: KivyCalendarWidget, cell: DateCell, month_src: int, month_dest: int):
        """called when the current month turns into its previous month.

        Args:
            instance (KivyCalendarWidget): instance
            cell (DateCell): the instance of its cell class which is set when making instance of KivyCalendarWidget
            month_src (int): the month just before.
            month_dest (int): the month which is turned into
        """
        print(f'_on_pre called : month_src = {month_src} -> month_dest= {month_dest}')
    
    def _on_next(self, instance: KivyCalendarWidget, cell: DateCell, month_src: int, month_dest: int):
        """called when the current month turns into its next month.

        Args:
            instance (KivyCalendarWidget): instance
            cell (DateCell): the instance of its cell class which is set when making instance of KivyCalendarWidget
            month_src (int): the month just before.
            month_dest (int): the month which is turned into
        """
        print(f'_on_next called : month_src = {month_src} -> month_dest = {month_dest}')
        
    def _on_select_day(self, instance: KivyCalendarWidget, cell: DateCell):
        """called when user select a day.

        Args:
            instance (KivyCalendarWidget): instance
            cell (DateCell): the instance of its cell class which is set when making instance of KivyCalendarWidget
        """
        print(f'_on_select_day called : {cell.month} / {cell.date}')
    
    def _on_deselect_day(self, instance: KivyCalendarWidget, cell: DateCell):
        """called when user deselect a day.

        Args:
            instance (KivyCalendarWidget): instance
            cell (DateCell): the instance of its cell class which is set when making instance of KivyCalendarWidget
        """
        print(f'_on_deselect_day : {cell.month} / {cell.date}')

def main():
    TestApp().run()


if __name__ == '__main__':
    main()
