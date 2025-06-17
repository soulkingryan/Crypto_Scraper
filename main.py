import matplotlib.pyplot as plt
import requests
import sqlite3
import csv
from datetime import datetime
from openpyxl import Workbook

def fetch_data():
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        'vs_currency': 'usd',
        'order': 'market_cap_desc',
        'per_page': 10,
        'page': 1,
        'sparkline': 'false',
        'price_change_percentage': '24h'
    }
    response = requests.get(url, params=params)
    return response.json()

def save_to_db(coins):
    connect = sqlite3.connect("crypto_data.db")
    cursor = connect.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS crypto_data(
            name TEXT,
            price TEXT,
            volume TEXT,
            change_24h TEXT,
            timestamp TEXT
        )
    ''')
    cursor.execute('DELETE FROM crypto_data')  # clear old data
    for coin in coins:
        name = coin['name']
        price = f"${coin['current_price']:,}"
        volume = f"${coin['total_volume']:,}"
        change_24h = f"{coin['price_change_percentage_24h']:.2f}%"
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute('INSERT INTO crypto_data (name, price, volume, change_24h, timestamp) VALUES (?, ?, ?, ?, ?)',
                       (name, price, volume, change_24h, timestamp))
    connect.commit()
    connect.close()

def export_to_csv(coins):
    with open("crypto_data.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Name", "Price", "Volume", "24h Change (%)"])
        for coin in coins:
            writer.writerow([
                coin['name'],
                coin['current_price'],
                coin['total_volume'],
                round(coin['price_change_percentage_24h'], 2)
            ])

def export_to_excel(coins):
    wb = Workbook()
    ws = wb.active
    ws.title = "Crypto Data"
    ws.append(["Name", "Price", "Volume", "24h Change (%)"])
    for coin in coins:
        ws.append([
            coin['name'],
            coin['current_price'],
            coin['total_volume'],
            round(coin['price_change_percentage_24h'], 2)
        ])
    wb.save("crypto_data.xlsx")

def show_price_chart(coins):
    names = [coin['name'] for coin in coins]
    prices = [coin['current_price'] for coin in coins]
    plt.bar(names, prices)
    plt.xticks(rotation=45)
    plt.title("Crypto Prices")
    plt.tight_layout()
    plt.show()

def generate_gui_file():
    with open("display.py", "w") as f:
        f.write('''
from tkinter import *
from tkinter import ttk
import sqlite3
import requests
from datetime import datetime

def refresh_data():
    import requests
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        'vs_currency': 'usd',
        'order': 'market_cap_desc',
        'per_page': 10,
        'page': 1,
        'sparkline': 'false',
        'price_change_percentage': '24h'
    }
    response = requests.get(url, params=params)
    coins = response.json()
    
    conn = sqlite3.connect("crypto_data.db")
    cur = conn.cursor()
    cur.execute("DELETE FROM crypto_data")
    for coin in coins:
        name = coin['name']
        price = f"${coin['current_price']:,}"
        volume = f"${coin['total_volume']:,}"
        change = f"{coin['price_change_percentage_24h']:.2f}%"
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cur.execute("INSERT INTO crypto_data (name, price, volume, change_24h, timestamp) VALUES (?, ?, ?, ?, ?)",
                    (name, price, volume, change, timestamp))
    conn.commit()
    conn.close()
    load_data()

def load_data():
    for item in tree.get_children():
        tree.delete(item)
    conn = sqlite3.connect("crypto_data.db")
    cur = conn.cursor()
    cur.execute("SELECT name, price, volume, change_24h, timestamp FROM crypto_data")
    rows = cur.fetchall()
    for i, row in enumerate(rows):
        tag = "evenrow" if i % 2 == 0 else "oddrow"
        tree.insert("", "end", values=row, tags=(tag,))
    conn.close()

win = Tk()
win.title("Live Crypto Tracker")

style = ttk.Style()
style.configure("Treeview", font=("Helvetica", 12), rowheight=30, foreground="black")
style.configure("Treeview.Heading", font=("Helvetica", 13, "bold"), foreground="white", background="#444444")


tree = ttk.Treeview(win, columns=("Name", "Price", "Volume", "24h Change", "Timestamp"), show="headings")
for col in tree["columns"]:
    tree.heading(col, text=col)
tree.tag_configure("evenrow", background="#e6e6e6")
tree.tag_configure("oddrow", background="#ffffff")
tree.pack(padx=10, pady=10, fill=BOTH, expand=True)

Button(win, text="Refresh", command=refresh_data).pack(pady=10)

load_data()
win.mainloop()
''')

# Run all processes
coins = fetch_data()
save_to_db(coins)
export_to_csv(coins)
export_to_excel(coins)
generate_gui_file()
show_price_chart(coins)