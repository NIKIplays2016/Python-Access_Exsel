from tkinter import *
from modules.db_requests import get_data_about_database
from tkinter import ttk



def create_xslx():
    pass


def toggle_losses_expenses():
    state = losses_var_expenses.get()
    for checkbox in losses_expense_checkboxes:
        losses_checkbox_var[checkbox].set(state)


def toggle_profit_expenses():
    state = profit_var_expenses.get()
    for checkbox in profit_expense_checkboxes:
        profit_checkbox_var[checkbox].set(state)


def field_finance_table(root):
    global losses_var_expenses
    global losses_expense_checkboxes
    global losses_checkbox_var
    global profit_var_expenses
    global profit_checkbox_var
    global profit_expense_checkboxes

    # Создание "стилей" для заголовков
    header1 = ('Calibri', 12)
    header2 = ('Calibri', 10)
    header3 = ('Calibri', 8)

    options = ["По дням", "По месяцам", "По сезонам", "По годам"]

    Label(root, text="Вывести:", font= header1).place(x=20, y=50)
    combobox = ttk.Combobox(root, values=options, height=3, width=15)
    combobox.set("Выберите поле")  # Установить начальное значение
    combobox.place(x=100, y=50)



    lframe = Frame(root, width=200, height=100)
    rframe = Frame(root, width=200, height=100)

    lframe.place(x=40, y=140)
    rframe.place(x=250, y=140)

    # rframe
    losses_var_expenses = IntVar()


    Label(rframe, text="Вывод расходов", font=header1).grid(row=1,column=1, sticky="w")
    cb_expenses = Checkbutton(rframe, variable=losses_var_expenses, command=toggle_losses_expenses)
    cb_expenses.grid(row=1, sticky="e", column=2)

    expense_categories = ["Учет доставки","Учет налога НДС", "Учет Зп", "Учет непредвиденных трат"]

    # Dictionary to store the variables for each checkbox
    losses_checkbox_var = {}
    losses_expense_checkboxes = []

    # Create checkboxes for each expense category
    for i, category in enumerate(expense_categories):
        var = IntVar()
        losses_checkbox_var[category] = var
        Label(rframe, text=category,  font=header2).grid(row=i+2, column=1, sticky='w', padx=10)
        cb = Checkbutton(rframe, variable=var)
        cb.grid(row=i + 2, column=2, sticky='e')
        losses_expense_checkboxes.append(category)

    #lframe
    profit_var_expenses = IntVar()

    Label(lframe, text="Вывод доходов", font=header1).grid(row=1,column=1, sticky="w")
    cb_expenses = Checkbutton(lframe, variable=profit_var_expenses, command=toggle_profit_expenses)
    cb_expenses.grid(row=1, sticky="e", column=2)

    expense_categories = ["Продукты","Топливо"]

    # Dictionary to store the variables for each checkbox
    profit_checkbox_var = {}
    profit_expense_checkboxes = []

    # Create checkboxes for each expense category
    for i, category in enumerate(expense_categories):
        var = IntVar()
        profit_checkbox_var[category] = var
        Label(lframe, text=category,  font=header2).grid(row=i+2, column=1, sticky='w', padx=10)
        cb = Checkbutton(lframe, variable=var)
        cb.grid(row=i + 2, column=2, sticky='e')
        profit_expense_checkboxes.append(category)


    about_db = get_data_about_database()
    Label(root, text=f"Кол-во строк: {about_db['count_row']}", font= header2).place(x=20, y=340)
    Label(root, text=f"Дата первой записи: {about_db['start_date']}", font=header2).place(x=20, y=370)
    Label(root, text=f"Дата последней записи: {about_db['end_date']}", font=header2).place(x=20, y=400)

    Label(root, text="Начать с:", font=header3).place(x=20, y=500)
    start_time_entry = Entry(root, width=12)
    start_time_entry.place(x=80, y=500)

    Label(root, text="Закончить на:", font=header3).place(x=200, y=500)
    end_time_entry = Entry(root, width=12)
    end_time_entry.place(x=285, y=500)

    Button(
        root,
        text="Создать",
        background="#33CC33",
        command=create_xslx,
        width=10,
        height=2
    ).place(x=200, y= 550)

