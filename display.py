
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
