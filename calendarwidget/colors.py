

from typing import Union, List, Tuple, NamedTuple

# The type for rgba, like [0.8, 0.8, 0.8, 1]
KivyRgbaColor = Union[List[float], Tuple[float]]

class KivyColors:
    # refer : https://www.color-site.com/english_names
    BLACK: KivyRgbaColor = (0, 0, 0, 1)
    WHITE: KivyRgbaColor = (1, 1, 1, 1)
    TAUPE: KivyRgbaColor = (86/255, 85/255, 101/255, 1)
    SKY_GRAY: KivyRgbaColor = (191/255, 197/255, 202/255, 1)
    STEEL_GRAY: KivyRgbaColor = (108/255, 103/255, 110/255, 1)
    
    RED: KivyRgbaColor = (1, 0, 0, 1)
    SCARLET: KivyRgbaColor = (241/255, 91/255, 71/255, 1)
    PINK: KivyRgbaColor = (248/255, 171/255, 166/255, 1)
    OLD_ROSE: KivyRgbaColor = (213/255, 132/255, 140/255, 1)
    
    GREEN: KivyRgbaColor = (0, 1, 0, 1)
    ICE_GREEN: KivyRgbaColor = (204/255, 231/255, 211/255, 1)
    IVY_GREEN: KivyRgbaColor = (72/255, 124/255, 56/255, 1)
    ALMOND_GREEN: KivyRgbaColor = (93/255, 129/255, 101/255, 1)
    AQUA_GREEN: KivyRgbaColor = (136/255, 191/255, 191/255, 1)
    
    BLUE: KivyRgbaColor = (0, 0, 1, 1)
    SKY_BLUE: KivyRgbaColor = (144/255, 215/255, 236/255, 1)

class ColorTheme(NamedTuple):
    # カレンダーの背景色
    background_color: KivyRgbaColor = KivyColors.BLACK
    # 月タイトル文字色
    month_color: KivyRgbaColor = KivyColors.WHITE
    # 年タイトル文字色
    year_color: KivyRgbaColor = KivyColors.WHITE
    # 曜日ヘッダーの背景色
    header_background: KivyRgbaColor = KivyColors.BLACK
    # 日曜の文字色
    sunday : KivyRgbaColor = KivyColors.RED
    # 平日の文字色
    weekdays : KivyRgbaColor = KivyColors.WHITE
    # 土曜の文字色
    saturday: KivyRgbaColor = KivyColors.BLUE
    
    # 現在選択している月に属する日の背景色と文字色
    nowdays_background: KivyRgbaColor = KivyColors.STEEL_GRAY
    nowdays_color: KivyRgbaColor = KivyColors.WHITE
    # 先月の月に属する日の背景色と文字色
    previousdays_background: KivyRgbaColor = KivyColors.TAUPE
    previousdays_color: KivyRgbaColor = KivyColors.WHITE
    # 来月の月に属する日の背景色と文字色
    nextdays_background: KivyRgbaColor = KivyColors.TAUPE
    nextdays_color: KivyRgbaColor = KivyColors.WHITE
    # 押された時の強調色
    pressed_background: KivyRgbaColor = [0.8, 0.2, 0.2, 1]

class CalenderThemes:
    DARK_THEME = ColorTheme()
    LIGHT_THEME = ColorTheme(
        background_color=KivyColors.WHITE,
        header_background=KivyColors.WHITE,
        month_color=KivyColors.BLACK,
        year_color=KivyColors.BLACK,
        weekdays=KivyColors.BLACK,
        nowdays_background=KivyColors.WHITE,
        nowdays_color=KivyColors.BLACK,
        previousdays_background=KivyColors.SKY_GRAY,
        previousdays_color=KivyColors.BLACK,
        nextdays_background=KivyColors.SKY_GRAY,
        nextdays_color=KivyColors.BLACK,
        pressed_background=[0.8, 0, 0, 0.5]
    )
    ICE_GREEN_THEME = ColorTheme(
        background_color=KivyColors.ICE_GREEN,
        month_color=KivyColors.BLACK,
        year_color=KivyColors.BLACK,
        header_background=KivyColors.ICE_GREEN,
        weekdays=KivyColors.BLACK,
        nowdays_background=KivyColors.WHITE,
        nowdays_color=KivyColors.BLACK,
        previousdays_background=KivyColors.AQUA_GREEN,
        previousdays_color=KivyColors.BLACK,
        nextdays_background=KivyColors.AQUA_GREEN,
        nextdays_color=KivyColors.BLACK,
        pressed_background=[0.5, 1, 0.8, 0.5]
    )
