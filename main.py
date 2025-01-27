from tkinter import Tk, ttk

from tables.secondary_widgets import field_info_table
from tables.find_widgets import field_find_table
from tables.finance_widgets import field_finance_table

window = Tk()
window.geometry("500x700")
window.resizable(False, False)

notebook = ttk.Notebook(window)

finance_tab = ttk.Frame(notebook)
find_tab = ttk.Frame(notebook)
info_tab = ttk.Frame(notebook)

notebook.add(finance_tab, text='Финансы')
notebook.add(find_tab, text='Поиск')
notebook.add(info_tab, text='Инфо')

notebook.pack(expand=True, fill='both')

style = ttk.Style()
style.configure("TNotebook.Tab", padding=[10, 4], font=('Calibri', 12))

notebook.configure(style="TNotebook")

field_finance_table(finance_tab)
field_find_table(find_tab)
field_info_table(info_tab)


window.mainloop()