
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.lang.builder import Builder


from kivycalendarwidget import DateCellBase, KivyCalendarWidget
from kivycalendarwidget.backgroundwidgets import BackgroundLabel
from kivycalendarwidget.colors import KivyRgbaColor, CalenderThemes


Builder.load_string('''
#<KvLang>
<MyDateCell>:
    orientation: 'vertical'
    label_date: lbl_date
    label_schedule: lbl_schedule
    BackgroundLabel:
        id: lbl_date
        background_color: root.background_color
        size_hint_y: 0.5
    
    BackgroundLabel:
        id: lbl_schedule
        background_color: root.background_color
        size_hint_y: 0.5
        text: 'something'

#</KvLang>
''')

class MyDateCell(DateCellBase, BoxLayout):
    label_date: BackgroundLabel
    label_schedule: BackgroundLabel
    def __init__(self, day: int, date: str, month: int, is_now_month: bool, **kwargs):
        super(MyDateCell, self).__init__(day, date, month, is_now_month, **kwargs)
        self.label_date.text = str(date) if is_now_month else f'{month}/{date}'
    
    # @overwrite
    def set_color(self, color: KivyRgbaColor):
        self.label_date.color = color
        self.label_schedule.color = color
    # @overwrite
    def set_background_color(self, background_color: KivyRgbaColor):
        self.label_date.background_color = background_color
        self.label_schedule.background_color = background_color
        self.background_color = background_color

    def set_schedule(self, text: str):
        self.label_schedule.text = text

class CostomCellApp(App):
    def __init__(self, **kwargs):
        super(CostomCellApp, self).__init__(**kwargs)
        
    def build(self):
        self.root = BoxLayout()
        
        c = KivyCalendarWidget(
            theme=CalenderThemes.ICE_GREEN_THEME,
            cell_cls=MyDateCell
        )
        c.bind(
            on_day_select=self._on_day_select
        )
        self.root.add_widget(c)
        
        return self.root

    def _on_day_select(self, instance: KivyCalendarWidget, cell: MyDateCell):
        cell.set_schedule('Done!')
    

def main():
    CostomCellApp().run()


if __name__ == '__main__':
    main()