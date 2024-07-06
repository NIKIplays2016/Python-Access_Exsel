from json import load
from tkinter import *
def take_color_settings() -> dir:
    with open(r"..\data\viev_settings.json", "r") as file:
        color_dir = load(file)
    return color_dir

def change_color_mode(window: Tk,color_name:str) -> None:
    """Изменяет цвет текста для всех виджетов в основном окне"""
    color_dir = take_color_settings()

    window.configure(bg=color_dir["color_settings"][color_name]["window_color"])

    for widget in window.winfo_children():
        if isinstance(widget, (Label, Button, Entry, Text, Text)):
            widget.config(fg=color_dir["color_settings"][color_name]["text_color"])



