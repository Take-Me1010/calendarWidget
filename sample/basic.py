

from kivy.app import App
#* config *#
from kivy.config import Config
# Config.set('modules', 'inspector', '')
# Config.set('modules', 'showborder', '')
import japanize_kivy

from calendarwidget import 


def main():
    
    class TestApp(App):
        def __init__(self, **kwargs):
            super(TestApp, self).__init__(**kwargs)
            
        def build(self):
            self.root = BoxLayout()
            monthsEnglish = [
                'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'
            ]
            # monthFormat: str = '${month}月だよ！'
            # monthFormat: List[str] = [
            #     'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'
            # ]
            monthFormat: List[str] = [m[:3]+'.' for m in monthsEnglish]
            
            c = KivyCalender(do_highlight_pressed_day=True, do_deselect_double_pressed_day=True, monthFormat=monthFormat)
            c.bind(
                on_previous_month=self._on_pre,
                on_next_month=self._on_next,
                on_day_select=self._on_select_day,
                on_day_deselect=self._on_deselect_day
            )
            
            # c.load_theme(CalenderThemes.LIGHT_THEME)
            c.load_theme(CalenderThemes.ICE_GREEN_THEME)
            
            self.root.add_widget(c)
            return self.root

        def _on_pre(self, instance: KivyCalender, cell: DateCell, month_src: int, month_dest: int):
            print(f'{month_src} -> {month_dest}')
        
        def _on_next(self, instance: KivyCalender, cell: DateCell, month_src: int, month_dest: int):
            print(f'{month_src} -> {month_dest}')
            
        def _on_select_day(self, instance: KivyCalender, cell: DateCell):
            print(f'Select {cell.month} / {cell.date}')
        
        def _on_deselect_day(self, instance: KivyCalender, cell: DateCell):
            print(f'Deselect {cell.month} / {cell.date}')
    
    TestApp().run()


if __name__ == '__main__':
    main()
