# Calendar Widget

A simple calendar widget written by pure Python and Kivy.

unreleased now.

## features

- this calendar only shows days, dates, year and month.
- you can set some functions that is called when a user selects a day, or deselects it, and when calendar goes to next month or previous month.
- you can customize appearance of this calendar easily. See some files in sample folder.



## requirements

maybe independent on the version of kivy
but in src code, I used Annotated in typing module which is added in python 3.9
So if you use python 3.8 or below, you must install typing_extensions.


日本語は基本的に文字化けするため、[sample/basic.py](sample/basic.py)などではjapanize_kivyを使用しています。
`pip install japanize_kivy`してください。
