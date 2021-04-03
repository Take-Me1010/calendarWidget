
'''A simple calendar widget for Kivy

Todo:
    - more documentation
    - enable user to customize the two buttons to change its month.
'''

from typing import Any, Dict, List, Optional, Union
try:
    from typing import Annotated
except:
    from typing_extensions import Annotated

from datetime import datetime, timedelta
import calendar
from kivy.uix.behaviors.button import ButtonBehavior

from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.graphics import Rectangle, Color
from kivy.lang.builder import Builder

from kivycalendarwidget.colors import KivyRgbaColor, ColorTheme
from kivycalendarwidget.backgroundwidgets import BackgroundButton, BackgroundColor, BackgroundLabel


Builder.load_string('''
#<KvLang>
<TitleLabel>:
    label_month: lbl_month
    label_year: lbl_year
    Label:
        id: lbl_month
        pos_hint: {'x': 2/7, 'y': 0}
        size_hint: 3/7, 1
        # text: '3月'
        font_size: 25
    
    Label:
        id: lbl_year
        pos_hint: {'x': 0, 'y': 0}
        size_hint: 2/7, 0.5
        # text: '2021'
    
    Button:
        id: btn_previous
        pos_hint: {'x': 5/7, 'y': 0}
        size_hint: 1/7, 1
        text: '<<'
    
    Button:
        id: btn_next
        pos_hint: {'x': 6/7, 'y': 0}
        size_hint: 1/7, 1
        text: '>>'
    
#</KvLang>
''')


class TitleLabel(FloatLayout):
    label_month: Label
    label_year: Label
    monthformat: Union[str, List[str]]

    def __init__(self, **kwargs):
        super(TitleLabel, self).__init__(**kwargs)
        self.monthformat = None

    def set_month(self, month: str, monthFormat: Optional[Union[str, List[str]]] = None):
        if monthFormat:
            self.monthformat = monthFormat
        self.label_month.text = self.getFormattedMonth(month)

    def getFormattedMonth(self, month: Annotated[int, (1, 12)]) -> str:
        monthString: str = str(month)
        if self.monthformat is None:
            return monthString

        monthFormat = self.monthformat
        if isinstance(monthFormat, str):
            monthString = monthFormat.replace('${month}', str(month))
        elif isinstance(monthFormat, list):
            try:
                monthString = monthFormat[month -
                                          1].replace('${month}', str(month))
            except IndexError:
                raise IndexError(
                    f'The length of argument:monthFormat must be 12, not {len(monthString)}')
        else:
            raise TypeError(
                f'The type of argument:monthFormat must be str or list, not {type(monthFormat)}')

        return monthString

    def set_year(self, year: str):
        self.label_year.text = year

    def load_style(self, month_color: KivyRgbaColor, year_color: KivyRgbaColor):
        self.label_month.color = month_color
        self.label_year.color = year_color


Builder.load_string('''
#<KvLang>
<DayHeader>:
    cols: 7
    rows: 1
#</KvLang>
''')


class DayHeader(GridLayout):
    header: List[str]
    label_headers: List[BackgroundLabel]

    def __init__(self, **kwargs):
        super(DayHeader, self).__init__(**kwargs)
        header = calendar.day_name[:]
        header[0], header[6] = header[6], header[0]
        self.header = header
        self.label_headers = []
        for day in header:
            lbl = BackgroundLabel(
                text=day
            )
            self.label_headers.append(lbl)
            self.add_widget(lbl)

    def load_style(self, style: List[Dict[str, Any]]):
        for child, s in zip(self.label_headers, style):
            for key in s.keys():
                child.__setattr__(key, s[key])


Builder.load_string('''
#<KvLang>
<DateCell>:

<DayTable>:
    cols: 7
    rows: 6

#</KvLang>
''')

# DateCellをカスタムする際に継承する必要があるクラス


class DateCellBase(ButtonBehavior, BackgroundColor):

    # 曜日を表す数字0~6
    day: int
    # 日にちを表す文字列
    date: str
    # 月を表す数字(1~12)
    month: int
    # この日にちが現在の月かどうか
    is_now_month: bool
    # テーマ
    theme: ColorTheme

    def __init__(self, day: int, date: str, month: int, is_now_month: bool = True, **kwargs):
        super(DateCellBase, self).__init__(**kwargs)
        self.day = day
        self.date = date
        self.month = month
        self.is_now_month = is_now_month

    def set_theme(self, theme: ColorTheme):
        self.theme = theme

    def set_background_color(self, background_color: KivyRgbaColor):
        self.background_color = background_color

    def set_color(self, color: KivyRgbaColor):
        """必ずオーバーライドするメソッド。

        Args:
            color (KivyRgbaColor): ColorTheme.nowdays_colorなどが月に応じて渡される。

        Raises:
            NotImplementedError: 未実装の時
        """
        raise NotImplementedError()

# DateCellはBaseと、見た目をカスタムするためのwidgetを継承する


class DateCell(DateCellBase, Label):
    def __init__(self, day: int, date: str, month: int, is_now_month: bool = True, **kwargs):
        super(DateCell, self).__init__(
            day, date, month, is_now_month, **kwargs)
        self.text = str(date) if is_now_month else f'{month}/{date}'

    # 必ずオーバーライトする。
    def set_color(self, color: KivyRgbaColor):
        if self.day == 0:
            self.color = self.theme.sunday
        elif self.day == 6:
            self.color = self.theme.saturday
        else:
            self.color = color


class DayTable(GridLayout):
    callback: callable
    theme: ColorTheme

    def __init__(self, cell_cls: DateCellBase = DateCell, **kwargs):
        super(DayTable, self).__init__(**kwargs)
        self.cell_cls = cell_cls

    def set_cell_callback(self, callback: callable):
        self.callback = callback

    def set_table(self, year: int, month: int, cell_cls: Optional[DateCellBase] = None):
        self.clear_widgets()
        date_first = datetime.strptime(f'{year}/{month}/1', '%Y/%m/%d')
        #! 以下は日曜=0の前提の処理。
        day_index: int = (date_first.weekday() + 1) % 7
        # 左上の日にちを計算
        date = date_first - timedelta(days=day_index)
        if cell_cls:
            self.cell_cls = cell_cls
        c = self.cell_cls
        for i in range(self.rows*self.cols):
            cell = c(day=i % 7, date=str(date.day), month=date.month,
                     is_now_month=(date.month == month))
            cell.bind(on_release=self.callback)
            self.add_widget(cell)
            date += timedelta(days=1)

        # テーマをリロード
        if hasattr(self, 'theme'):
            self.load_theme(self.theme)

    def load_theme(self, theme: ColorTheme):
        self.theme = theme
        # 6*7の日の一覧表の中心は各月
        month_now: int = self.children[21].month
        for cell in self.children:
            cell.set_theme(theme)
            if cell.month < month_now:
                background_color = theme.previousdays_background
                color = theme.previousdays_color
            elif cell.month == month_now:
                background_color = theme.nowdays_background
                color = theme.nowdays_color
            else:
                background_color = theme.nextdays_background
                color = theme.nextdays_color

            cell.set_background_color(background_color)
            cell.set_color(color)


class KivyCalendarWidget(BoxLayout):
    ''' A simple calender widget made by Kivy

        this widget provides easy customization for its appearance!

    Attributes:
        pressed (None | DateCell | any class inheriting DateCellBase) the cell user selects. If None, no cell is selected.

    '''
    __events__ = ('on_next_month', 'on_previous_month',
                  'on_day_select', 'on_day_deselect')
    today: datetime
    title_label: TitleLabel
    day_header: DayHeader
    day_table: DayTable
    year_now: int
    month_now: int
    # 選択した日にちを次に選択するまでハイライトするかどうか
    # whether calendar do highlight against the day if user select/press it.
    do_highlight_pressed_day: bool
    # 二回押されたら選択を解除するか
    # whether calendar deselect the day user selected if user select/press same day.
    do_deselect_double_pressed_day: bool
    # 押されたセルを記録しておく
    pressed: Union[DateCell, None]
    # 強調前の元々の色を保存
    pressed_background_before: KivyRgbaColor

    def __init__(self, theme: Optional[ColorTheme] = None, do_highlight_pressed_day: bool = True,
                 do_deselect_double_pressed_day: bool = False, cell_cls: DateCellBase = DateCell, monthFormat: Union[str, List[str]] = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'], **kwargs):
        """A simple calendar widget for Kivy

        Args:
            theme (Optional[ColorTheme], optional): theme object generated through ColorTheme. if None, default theme will be used. Defaults to None.
            do_highlight_pressed_day (bool, optional): define if the cell user selects is highlighted. Defaults to True.
            do_deselect_double_pressed_day (bool, optional): define if the cell is deselected when user selects it twice. Defaults to False.
            cell_cls (DateCellBase, optional): an argument prepared to custom. See README and samples. Defaults to DateCell.
            monthFormat (Union[str, List[str]], optional): an argument to deside what kind of style the calendar widget shows the current month. Defaults to '${month}'.
        """
        super().__init__(**kwargs)
        # now, calendar shows the month of today at first.
        today = datetime.now()
        self.year_now = today.year
        self.month_now = today.month

        self.do_highlight_pressed_day = do_highlight_pressed_day
        self.do_deselect_double_pressed_day = do_deselect_double_pressed_day

        self.pressed = None

        # build
        self.orientation = 'vertical'
        self.title_label = TitleLabel(size_hint_y=0.1)
        self.add_widget(self.title_label)
        self.day_header = DayHeader(size_hint_y=0.15)
        self.add_widget(self.day_header)
        self.day_table = DayTable(cell_cls, size_hint_y=0.75)
        self.add_widget(self.day_table)

        # bind
        self.bind(size=self._update_rect, pos=self._update_rect)
        self.title_label.ids['btn_next'].bind(on_release=self.next_month)
        self.title_label.ids['btn_previous'].bind(
            on_release=self.previous_month)
        self.day_table.set_cell_callback(self.datecell_released)

        # init calendar appearance
        self.set_month(self.month_now, monthFormat)
        self.set_year(self.year_now)
        if theme is None:
            theme = ColorTheme()
        self.load_theme(theme)

    def reload(self, month: Optional[int] = None):
        self.set_month(month or self.month_now)

    def datecell_released(self, instance: DateCell):
        month_selected = instance.month
        if month_selected < self.month_now:
            self.dispatch('on_previous_month', instance,
                          self.month_now, month_selected)
            self.previous_month(instance)
        elif month_selected > self.month_now:
            self.dispatch('on_next_month', instance,
                          self.month_now, month_selected)
            self.next_month(instance)
        else:
            pass

        if instance != self.pressed or not self.do_deselect_double_pressed_day:
            self.deselect_cell()
            self.select_cell(instance)
        else:
            self.deselect_cell()

    def select_cell(self, cell: DateCell):
        ''' cellを選択状態にする '''
        self.dispatch('on_day_select', cell)
        self.pressed = cell
        if self.do_highlight_pressed_day:
            self.pressed_background_before = cell.background_color
            cell.background_color = self.pressed_background

    def deselect_cell(self):
        ''' 選択中のセルの選択を解除する '''
        if self.pressed:
            self.dispatch('on_day_deselect', self.pressed)
            self.pressed.background_color = self.pressed_background_before
        self.pressed = None

    def on_previous_month(self, *args, **kwargs):
        pass

    def on_next_month(self, *args, **kwargs):
        pass

    def on_day_select(self, *args, **kwargs):
        pass

    def on_day_deselect(self, *args, **kwargs):
        pass

    def next_month(self, *args):
        """翌月のカレンダーを表示する
        """
        month_next = self.month_now + 1
        if month_next >= 13:
            self.set_year(self.year_now+1)
            month_next %= 12
        self.set_month(month=month_next)

    def previous_month(self, *args):
        """先月のカレンダーを表示する
        """
        month_previous = self.month_now - 1
        if month_previous <= 0:
            self.set_year(self.year_now-1)
            month_previous += 12
        self.set_month(month=month_previous)

    def set_year(self, year: int):
        self.year_now = year
        self.title_label.set_year(str(year))
        self.day_table.set_table(year=year, month=self.month_now)

    def set_month(self, month: Annotated[int, (1, 12)], monthFormat: Optional[Union[str, List[str]]] = None):
        """表示する月をセットする

        Args:
            month int: 月。1~12のint
            monthFormat Union[str, List[str]]: 表示する月のフォーマット。配列の場合は、そのindexが各月に対応するように、長さは12でないといけない。
        """
        self.month_now = month

        self.title_label.set_month(month, monthFormat)
        self.day_table.set_table(year=self.year_now, month=month)

    def set_background_color(self, color: List[float]):
        # self.canvas.before.clear()
        with self.canvas.before:
            Color(rgba=color)
            self.rect = Rectangle(
                size=self.size,
                pos=self.pos
            )

    def _update_rect(self, instance, value):
        if hasattr(self, 'rect'):
            self.rect.size = instance.size
            self.rect.pos = instance.pos

    def load_theme(self, theme: ColorTheme):
        self.set_background_color(theme.background_color)

        self.title_label.load_style(theme.month_color, theme.year_color)

        header_style = [{'color': theme.sunday,
                         'background_color': theme.header_background}]
        header_style.extend(
            [{'color': theme.weekdays, 'background_color': theme.header_background} for _ in range(5)])
        header_style.append(
            {'color': theme.saturday, 'background_color': theme.header_background})
        self.day_header.load_style(header_style)

        self.day_table.load_theme(theme)

        self.pressed_background = theme.pressed_background


def test():
    from kivy.app import App
    from kivycalendarwidget.colors import CalenderThemes

    class TestApp(App):
        def __init__(self, **kwargs):
            super(TestApp, self).__init__(**kwargs)

        def build(self):
            self.root = BoxLayout()
            c = KivyCalendarWidget(
                theme=CalenderThemes.ICE_GREEN_THEME, monthFormat='${month}')
            self.root.add_widget(c)

            return self.root

    TestApp().run()


if __name__ == '__main__':
    test()
