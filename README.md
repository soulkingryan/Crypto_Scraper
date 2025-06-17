# Crypto Scraper

This project is a full-stack Python application that retrieves real-time cryptocurrency market data using the CoinGecko API and presents it through multiple user-friendly outputs including database storage, visual charts and a graphical interface.

## Key Features
**Live Data**: Retrieves the top 10 cryptocurrencies by market cap with current pricing, volume and 24-hour change percentages from CoinGecko.
**Local Database Storage**: Stores all data in a structured SQLite database (`crypto_data.db`) with a timestamp for each entry.
- **Data Export Options**:
  - CSV format (`crypto_data.csv`)
  - Excel spreadsheet (`crypto_data.xlsx`)
- **Price Visualization**: Generates a real-time bar chart using `matplotlib` to display price comparisons.
- **Graphical User Interface (GUI)**:
  - Built using `Tkinter` for a clean, native desktop experience
  - Displays name, price, volume, 24h % change, and timestamp
  - Includes a **Refresh** button to retrieve and reload the latest data
  - Alternating row colors and styled column headers for readability

## Files
- `main.py` — Runs all processes, including GUI generator
- `display.py` — Auto-generated GUI interface that displays the crypto data
- `crypto_data.db` — SQLite database storing coin data
- `crypto_data.csv` — CSV export
- `crypto_data.xlsx` — Excel export

## Dependencies
Install requirements (if not already installed) are ```bash and pip install matplotlib openpyxl requests

### How to Run
**Step 1:** Clone or download this repository
**Step 2:** Always run `main.py` first. This fetches the latest cryptocurrency data, updates the database, and regenerates the GUI file.
**Step 3:** Then run `display.py` to launch the GUI and view the live data.

Please note, always run main.py before display.py to update data and regenerate the GUI.


#### Screenshots 
`main.py:` (Data Retrieval, Processing & Visualization)
<img width="1091" alt="Screenshot 2025-06-16 at 9 32 03 PM" src="https://github.com/user-attachments/assets/139d326a-03c3-4395-875a-2935d12d982d" />

`display.py` (GUI Display)
<img width="1013" alt="Screenshot 2025-06-16 at 9 33 27 PM" src="https://github.com/user-attachments/assets/f7c813ff-b0b4-455d-85a4-e46c78656899" />

