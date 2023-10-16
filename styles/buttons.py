import flet as ft

# Стиль для элемента списка заметок
note_style = ft.ButtonStyle(
    overlay_color=ft.colors.YELLOW_100,
    shape={
        ft.MaterialState.HOVERED: ft.RoundedRectangleBorder(radius=30),
        ft.MaterialState.DEFAULT: ft.RoundedRectangleBorder(radius=15),
    },
    side={
        ft.MaterialState.DEFAULT: ft.BorderSide(3, ft.colors.YELLOW_100),
        ft.MaterialState.HOVERED: ft.BorderSide(2, ft.colors.YELLOW_100),
    },
    bgcolor=ft.colors.YELLOW_100,
    animation_duration=35
)
# Стиль для кнопки добавления новой заметки
add_btn_style = ft.ButtonStyle(
    overlay_color=ft.colors.GREEN_300,
    shape={
        ft.MaterialState.HOVERED: ft.RoundedRectangleBorder(radius=50),
        ft.MaterialState.DEFAULT: ft.RoundedRectangleBorder(radius=25)
    },
    side={
        ft.MaterialState.DEFAULT: ft.BorderSide(3, ft.colors.GREEN_300),
        ft.MaterialState.HOVERED: ft.BorderSide(2, ft.colors.GREEN_300)
    },
    color=ft.colors.GREEN_300,
    bgcolor=ft.colors.GREEN_300,
    animation_duration=35
)