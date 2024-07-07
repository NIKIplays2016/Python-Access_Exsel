import pyodbc
from decimal import Decimal
from datetime import datetime


connection = pyodbc.connect(r"DRIVER={Microsoft Access Driver (*.mdb, *.accdb)}; DBQ=data\Database.accdb;")

def create_sql_time(str_time: str) -> str:
    formats = [
        '%d-%m-%Y %H:%M:%S',  # Формат с часами, минутами и секундами
        '%d-%m-%Y %H:%M',  # Формат с часами и минутами
        '%d-%m-%Y %H',  # Формат только с часами
        '%d-%m-%Y',  # Формат только с датой
        '%Y-%m',
        '%Y',
        '%m'
    ]
    if len(str_time) <= 11:
        str_time = str_time.replace(" ", "")

    for fmt in formats:
        try:
            dt = datetime.strptime(str_time, fmt)
            break
        except ValueError:
            continue

    try:
        formatted_time = dt.strftime('%Y-%m-%d %H:%M:%S')
        sql_time = f"#{formatted_time}#"
    except:
        sql_time=""
    return sql_time


def search_line(collumn_name: str, collumn_value: str, sign: str, start_date = None, end_date = None ) -> list:
    cursor = connection.cursor()

    filter = {
        "id": int,
        "count": int,
        "price": Decimal,
        "unexpected_expenses": create_sql_time,
        "trans_date": datetime
    }

    converter = filter.get(collumn_name, str)  # По умолчанию, используем str
    try:
        collumn_value = converter(collumn_value)
    except:
        raise TypeError

    if start_date or end_date:
        start_date_sql = create_sql_time(start_date)
        end_date_sql = create_sql_time(end_date)
        if not start_date:
            request = f"SELECT * FROM transactions WHERE {collumn_name} {sign} {collumn_value} AND trans_date < {end_date_sql}"
        elif not end_date:
            request = f"SELECT * FROM transactions WHERE {collumn_name} {sign} {collumn_value} AND trans_date > {start_date_sql}"
        else:
            request = f"SELECT * FROM transactions WHERE {collumn_name} {sign} {collumn_value} AND trans_date BETWEEN {start_date_sql} AND {end_date_sql}"
    else:
        request = f"SELECT * FROM transactions WHERE {collumn_name} {sign} {collumn_value}"

    try:
        cursor.execute(request)
    except:
        raise SyntaxError

    transactions = cursor.fetchall()
    cursor.close()

    return transactions

#transactions = find_line("price", "1", ">", "01-10-2023 11:11:11","02-10-2023" )
#print(transactions)