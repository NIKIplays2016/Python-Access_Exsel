from tkinter import *
from tkinter import ttk
from modules.db_requests import search_line

options = ["id", "тип", "название", "Кол-во", "Цена", "Код", "Прочие рассходы", "Дата"]
collums = {
    "id": "id",
    "тип": "type",
    "название": "trans_name",
    "Кол-во": "count",
    "Цена": "price",
    "Код": "code",
    "Прочие рассходы": "unexpected_expenses",
    "Дата": "trans_date"

}


def field_find_table(place: Frame) -> None:
    """Fills in the tab 'Инфо'"""
    combobox = ttk.Combobox(place, values=options, height=3, width=15)
    combobox.set("Выберите поле")  # Установить начальное значение
    combobox.place(x=50, y=70)


