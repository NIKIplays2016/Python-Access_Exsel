"""
Программа создает транзакции
"""
import pyodbc
import decimal
from datetime import datetime, timedelta
from random import randrange, randint



conn_str = (
    r"DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};"
    r"DBQ=..\data\Database.accdb;"
)
connection = pyodbc.connect(conn_str)
cursor = connection.cursor()

normal_date = {                 #Словарь в котором указан диапазон количества товара которое обычно покупают
    "Пиво": [1, 5],
    "Сигареты": [1,5],
    "ДЗ-5": [10,120],
    "Кириешки": [1,3],
    "Молоко": [1,2],
    "Сосиски": [1,2],
    "Сыр": [1,2],
    "Сметана": [1,3],
    "Куриное мясо": [1, 5],
    "Свинное мясо": [1, 7],
    "Вода": [1,7],
    "Газировка": [1,5],
    "Здания": [1,1],
    "Канализация": [1,1],
    "Электричество": [500, 2000],
    "Деньги": [1,50],
    "Бензин": [10, 80],
    "Бинт": [1,4],
    "Активированный уголь":[1,2],
    "Заправки":[1,1],

}


def create_trans_code() -> str:
    trans_code = ""
    for i in range(32):  # generate transaction code
        trans_code += chr(randint(65, 122))
    return trans_code

def ecording_transaction(trans_type: str, trans_name: str, count: int, price: float, trans_date: datetime, trans_code = "") -> None:
    """add transaction in table 'transactions' """

    if trans_code == "":
        trans_code = create_trans_code()

    price *= count
    if randint(0, 3000) == 7:
        if price > 0:
            unexpected_expenses = -price * decimal.Decimal(randint(1, 200) / 100)
        else:
            unexpected_expenses = price * decimal.Decimal(randint(1, 200) / 100)
    else:
        unexpected_expenses = 0

    cursor.execute(
        "INSERT INTO transactions (type, trans_name, count, price, code, unexpected_expenses, trans_date) VALUES (?,?,?,?,?,?,?)",
        (trans_type, trans_name, count, price, trans_code, unexpected_expenses, trans_date)
    )
    cursor.commit()
    connection.commit()


def salary_issuance(date: datetime) -> None:
    """write in transactions table salary issuance"""
    day = date.day

    cursor.execute(f"SELECT * FROM workers WHERE salary_at = {day}")
    salarys = cursor.fetchall()

    if salarys:
        for people in salarys:
            hours_worked = round(160 * people[6] * (randrange(6,12) / 10))    #Генерация отработанных часов

            data = (people[1], people[3], hours_worked, people[5], date)                #Сбор всех нужных данных для функции в кортеж
            ecording_transaction(*data)


def take_random_purchases(goods_ids) -> list:
    """Choise random space in database (goods table) and make purchases"""

    goods_id = randint(1,15)
    if goods_id in goods_ids:
        return take_random_purchases(goods_ids)

    goods_ids.append(goods_id)
    cursor.execute(f"SELECT * FROM goods WHERE id = {goods_id}")
    goods = cursor.fetchall()[0]

    counts = normal_date[goods[2]]
    count = randint(counts[0], counts[1])

    purchases = [goods[1], goods[2], count, goods[6]]

    return purchases


def make_transactions(write_time: datetime) -> None:
    """make transaction, and add they in database"""

    trans_code = create_trans_code()

    goods_ids = []          # Список, который будет хранить id продуктов наход. в корзиге покупатель, для исключения повтора
    for i in range(randint(1,10)):
        purchases = take_random_purchases(goods_ids)

        ecording_transaction(*purchases, write_time, trans_code)


def payment_of_bills(write_time: datetime) -> None:
    """make transaction with payment watter, electric ..."""
    cursor.execute("SELECT * FROM service")
    service_list = cursor.fetchall()
    for service in service_list:
        trans_code = create_trans_code()

        counts = normal_date[service[2]]
        count = randint(counts[0], counts[1])

        ecording_transaction(service[1], service[2], count, service[3], write_time, trans_code)


def __main():
    write_time = datetime(2021, 6, 5, 00, 00)        # Задаем время с которого мы хотим начать записи в БД
    for a in range(365*3):                                                             # Теперь идем по каждому дню до настоящего времени
        write_time = write_time.replace(hour=6, minute=0, second=0)                 # делаем так, чтобы транзакции начинались в 6 часов утра

        print(f"{a} proccessing.." )

        if write_time.day == 21:
            payment_of_bills(write_time)

        salary_issuance(write_time)

        for b in range(0, 1080, 10):                                                # Теперь проходим каждый день c 6 утра до 12 вечера промежутком по 10 минут

            if randint(1,10) <= 7:                                            # теперь с вероятностью в 70 процентов у нас произойдет транзакция
                write_time = write_time.replace(second=randint(0, 59))
                write_time += timedelta(minutes=randint(0,9))

                make_transactions(write_time)

            if write_time.hour < 1:
                break

            write_time += timedelta(minutes=10)


if __name__ == "__main__":
    cursor.execute("DELETE FROM transactions;")
    cursor.execute("ALTER TABLE transactions ALTER COLUMN id COUNTER(1, 1);")
    __main()

