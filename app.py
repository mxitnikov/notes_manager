"""
Модуль flet используется для создания основного интерфейса программы
Модуль _database используется для взаимодействия с базой данных
Модуль styles используется для хранения некоторых стилей
Модуль objects используется для хранения некоторых объектов страницы
"""
import flet as ft
from _database import add_note, search_notes, delete_note, fetch_note_by_id
from styles import note_style, add_btn_style
from objects import note_title, note_content, notes_list


def main(page: ft.Page) -> None:
    """
    Основная функция, настраивающая приложение менеджера заметок.
    """
    page.title = "Менеджер заметок"
    page.window_resizable = False

    def update_notes_list() -> None:
        """
        Функция для обновления списка заметок при различных действиях
        """
        # Очистка текущего списка заметок в программе
        notes_list.controls.clear()
        # Поиск заметок по ключевой фразе и добавление их на страницу
        results = search_notes(keyword=search_bar.content.value.strip())
        for note in results:
            notes_list.controls.append(ft.Container(
                ft.TextButton(
                    content=ft.Container(
                        alignment=ft.alignment.center_left,
                        content=ft.Text(
                            value=f"{note.title}",
                            color="black",
                            font_family="Roboto",
                            size=48),
                        margin=5,
                        padding=5),
                    style=note_style,
                    data=note.id,
                    on_click=open_note)
            ))
        # Обновление информации о количестве найденных заметок
        if len(results) > 0:
            status_bar.value = f"Элементов найдено: {len(results)}"
        else:
            status_bar.value = "Ничего не найдено"
        # Обновление состояния страницы
        page.update()

    def find_notes(e) -> None:
        """
        Event handler для поиска заметок в базе данных.
        :param e: Объект события.
        """
        del e
        # Обновление состояния страницы
        update_notes_list()

    def add_new_note_modal(e) -> None:
        """
        Event handler модального окна для добавления новой заметки.
        :param e: Объект события.
        """
        del e
        # Открытие модального окна для добавления новой заметки
        page.dialog = new_note_modal
        new_note_modal.open = True
        # Обновление состояния страницы
        page.update()

    def clear_add_new_note_modal() -> None:
        """
        Функция для очистки памяти элементов для создания новой заметки.
        """
        note_title.value = None
        note_content.value = None
        note_title.hint_text = "Введите заголовок заметки"
        note_title.hint_style = ft.TextStyle(color=ft.colors.SECONDARY)
        new_note_modal.open = False

    def no_data_in_title_input() -> None:
        """
        Функция для изменения дизайна модального окна создания новой заметки
        при отсутствии вводимых данных в окне для ввода заголовка заметки.
        """
        note_title.hint_text = "Введите хотя бы 1 символ в названии заметки"
        note_title.hint_style = ft.TextStyle(
            color=ft.colors.RED
        )

    def create_new_note(e) -> None:
        """
        Event handler для создания новой заметки.
        :param e: Объект события.
        """
        del e
        # Проверка наличия заголовка заметки
        if len(note_title.value) > 0:
            notes_list.controls.clear()
            add_note(note_content.value, note_title.value)
            clear_add_new_note_modal()
            update_notes_list()
        else:
            no_data_in_title_input()
        # Обновление состояния страницы
        page.update()

    def close_add_note_modal(e) -> None:
        """
        Event handler для закрытия модального окна для добавления заметки.
        :param e: Объект события.
        """
        del e
        # Закрытие модального окна для добавления новой заметки
        new_note_modal.open = False
        page.update()
        # Очистка памяти элементов модального окна
        note_title.value = None
        note_content.value = None
        note_title.hint_text = "Введите заголовок заметки"
        note_title.hint_style = ft.TextStyle(color=ft.colors.SECONDARY)

    def close_open_note_modal(e) -> None:
        """
        Event handler для закрытия модального окна для просмотра заметки.
        :param e: Объект события.
        """
        del e
        # Закрытие модального окна для просмотра заметки
        open_note_modal.open = False
        # Обновление состояния страницы
        page.update()

    def delete_note_btn_modal(e) -> None:
        """
        Event handler для удаления заметки из базы данных.
        :param e: Объект события.
        """
        # Удаление заметки из базы данных
        delete_note(e.control.data)
        # Закрытие модального окна просмотра заметки
        open_note_modal.open = False
        # Обновление списка заметок
        update_notes_list()

    def open_note(e) -> None:
        """
        Event handler для открытия подробной информации о заметке.
        :param e: Объект события.
        """
        # Поиск заметки по идентификатору из базы данных
        note_id, title, content = fetch_note_by_id(e.control.data)

        open_note_modal.title = ft.Text(value=title,
                                        font_family="Roboto",
                                        size=32,
                                        color=ft.colors.PRIMARY)

        open_note_modal.shape = ft.RoundedRectangleBorder(
            radius=12
        )

        open_note_modal.content = ft.Container(
            ft.Column(
                [
                    ft.Container(
                        ft.TextField(
                            value=content if content else "Пустая заметка",
                            read_only=True,
                            multiline=True,
                            border=ft.InputBorder.NONE,
                            expand=True),
                        expand=True)
                ], expand=True),
            height=700,
            width=700)

        open_note_modal.actions = [
            ft.IconButton(icon=ft.icons.KEYBOARD_ARROW_LEFT,
                          on_click=close_open_note_modal,
                          icon_color=ft.colors.PRIMARY),
            ft.IconButton(icon=ft.icons.DELETE,
                          on_click=delete_note_btn_modal,
                          data=note_id,
                          icon_color=ft.colors.RED_600)
        ]
        # Открытие модального окна для просмотра заметки
        page.dialog = open_note_modal
        open_note_modal.open = True
        # Обновление состояния страницы
        page.update()

    new_note_modal = ft.AlertDialog(
        modal=False,
        title=ft.Text("Добавление новой заметки",
                      size=32,
                      font_family="Roboto"),
        content=ft.Container(ft.Column([
            ft.Container(ft.Text("Заголовок заметки")),
            ft.Container(note_title),
            ft.Container(ft.Text("Содержание заметки")),
            ft.Container(note_content, expand=True),
        ], expand=True), height=700, width=700),
        actions=[
            ft.TextButton("Добавить",
                          on_click=create_new_note),
            ft.TextButton("Отмена",
                          on_click=close_add_note_modal,
                          style=ft.ButtonStyle(color=ft.colors.RED)),
        ],
        on_dismiss=close_add_note_modal
    )

    open_note_modal = ft.AlertDialog(
        modal=False,
        on_dismiss=close_open_note_modal
    )

    status_bar = ft.Text()

    search_bar = ft.Container(
        ft.TextField(
            hint_text="Введите название заметки или ключевые слова",
            on_change=find_notes,
            on_submit=find_notes
        ), padding=(ft.padding.only(left=20)),
        expand=True)

    search_options = ft.Row(
        [search_bar, ft.Container(
            ft.IconButton(
                icon=ft.icons.SEARCH,
                on_click=find_notes)
        )]
    )

    notes_add_btn = ft.Row(
        [ft.Container(
            ft.IconButton(
                icon=ft.icons.ADD,
                icon_color=ft.colors.WHITE,
                style=add_btn_style,
                expand=True,
                width=96,
                height=96,
                on_click=add_new_note_modal),
            padding=20,
            expand=True)]
    )

    update_notes_list()

    page.add(search_options, notes_add_btn,
             ft.Container(content=notes_list, expand=True),
             status_bar)


ft.app(target=main)
