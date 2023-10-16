import flet as ft

note_title = ft.TextField(hint_text="Введите заголовок заметки",
                          expand=True,
                          max_length=50)

note_content = ft.TextField(hint_text="Введите содержание заметки",
                            multiline=True,
                            border=ft.InputBorder.NONE)

notes_list = ft.ListView(expand=True,
                         spacing=10,
                         padding=20)