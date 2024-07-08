from tkinter import *

def field_info_table(place: Frame) -> None:
    """Fills in the tab 'Инфо'"""
    Label(place, text="Программа для вывода сводной таблицы", font=('Arial', 15)).pack(pady=10)

    Label(
        place,
          text="В вкладке 'Финансы' можно выбрать интересующие критерии\n"
               "И после нажатия кнопки 'Создать' данные с нужными критериями \n"
               "загрузятся в 'summary_table.xlsx' \n"

          ).pack(pady=10)
