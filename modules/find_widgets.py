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

def get_lines():
    collumn_value = collumn_value_entry.get()
    sign = sign_entry.get()

    error_label.config(text="")

    try:
        collumn_name = collums[combobox.get()]
    except KeyError:
        error_label.config(text="Выберите название колонки", fg="#9E9900")
        return 0

    try:
        lines = search_line(collumn_name, collumn_value, sign, start_time_entry.get(), end_time_entry.get())
    except ValueError:
        error_label.config(text="Не верно введено время\nФормат: 01-01-2024 14:58:40", fg="#CF2222")
        return 0
    except TypeError:
        error_label.config(text="Некорректный ввод\nПроверьте поле 'Значение'", fg="#CC2222")
        return 0
    except SyntaxError:
        error_label.config(text="Проверьте поля на корректность", fg="#CC2222")
        return 0

    text_widget.delete(1.0, END)

    if len(lines) > 500:
        error_label.config(text="Слишком много данных\nВыведено 500", fg="#9E9900")
    elif len(lines) == 0:
        text_widget.insert(END, "Ничего не найдено")

    for record in lines[:500]:
        sms = (f"______________________________________________________\n"
               f"ID: {record[0]} Тип: {record[1]}\n "
               f"Название: {record[2]} \n"
               f"Кол-во:  {record[3]} Сумма:  {record[4]}руб\n"
               f"Непредвиденных трат:  {record[6]} руб\n"
               f"Код: {record[5]}\n"
               f"Дата: {record[7]} \n")
        text_widget.insert(END, sms)


def field_find_table(room: Frame) -> None:
    """Fills in the tab 'Инфо'"""
    global start_time_entry
    global end_time_entry
    global collumn_value_entry
    global combobox
    global sign_entry
    global error_label
    global text_widget

    error_label = Label(room, font=('Calibri', 10))
    error_label.place(x=20, y=30)

    label_combox = Label(room, text="Название колонки")
    combobox = ttk.Combobox(room, values=options, height=3, width=15)
    combobox.set("Выберите поле")  # Установить начальное значение
    label_combox.place(x=10, y=100)
    combobox.place(x=10, y=120)

    collumn_value_label = Label(room, text="Значение")
    collumn_value_entry = Entry(room)
    collumn_value_label.place(x=200, y=100)
    collumn_value_entry.place(x=200, y=120)

    sign_label = Label(room, text="Знак")
    sign_entry = Entry(room, width=2)
    sign_entry.insert(0,"=")
    sign_label.place(x=160, y=100)
    sign_entry.place(x=165, y=120)

    start_time_label = Label(room, text="Начать с:")
    start_time_entry = Entry(room)
    start_time_label.place(x=220, y=30)
    start_time_entry.place(x=320, y=30)


    end_time_label = Label(room, text="Закончить на:")
    end_time_entry = Entry(room)
    end_time_label.place(x=220, y=60)
    end_time_entry.place(x=320, y=60)
    entry_comment_label = Label(room, text="(формат: 01-01-2024 00:00:00)", font=('Calibri', 7))
    entry_comment_label.place(x=325, y=85)

    find_button = Button(
        room,
        text= "Поиск",
        background= "#33CC33",
        command= get_lines,
        width= 8,
        height= 1
    )
    find_button.place(x=380, y=110)

    text_widget = Text(room, wrap=WORD, width=80, height=30)  # Используем Text виджет
    text_widget.place(x=0, y=150)

    # Добавление полос прокрутки
    scrollbar_y = ttk.Scrollbar(room, orient=VERTICAL, command=text_widget.yview)
    scrollbar_y.place(x=580, y=150, height=200)
    text_widget.config(yscrollcommand=scrollbar_y.set)