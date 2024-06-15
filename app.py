import tkinter as tk
from tkinter import ttk
from ttkbootstrap import Style
import requests
import re

def get_stock_price(symbol, api_key):
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval=1min&apikey={api_key}'
    response = requests.get(url)
    data = response.json()

    if 'Time Series (1min)' in data:
        latest_time = list(data['Time Series (1min)'].keys())[0]
        latest_price = data['Time Series (1min)'][latest_time]['1. open']
        return latest_price
    else:
        return None

def get_historical_price(symbol, date, api_key):
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={api_key}'
    response = requests.get(url)
    data = response.json()

    if 'Time Series (Daily)' in data and date in data['Time Series (Daily)']:
        closing_price = data['Time Series (Daily)'][date]['4. close']
        return closing_price
    else:
        return None

def get_company_overview(symbol, api_key):
    url = f'https://www.alphavantage.co/query?function=OVERVIEW&symbol={symbol}&apikey={api_key}'
    response = requests.get(url)
    data = response.json()

    if 'Name' in data:
        overview = f"{data['Name']} ({data['Symbol']}): {data['Description']}"
        return overview
    else:
        return None

def process_user_input():
    user_input = entry.get().strip().upper()

    if user_input.lower() == 'exit':
        chatbox.config(state=tk.NORMAL)
        chatbox.insert(tk.END, "Goodbye!\n")
        chatbox.config(state=tk.DISABLED)
        return

    chatbox.config(state=tk.NORMAL)
    chatbox.insert(tk.END, f"You: {user_input}\n")

    # Check for stock price inquiry (case insensitive and flexible)
    match_current_price = re.match(r'.*CURRENT PRICE.* ([A-Z]+)', user_input, re.IGNORECASE)
    if match_current_price:
        symbol = match_current_price.group(1)
        stock_price = get_stock_price(symbol, api_key)
        if stock_price:
            chatbox.insert(tk.END, f"Bot: The current price of {symbol} is ${stock_price}\n")
        else:
            chatbox.insert(tk.END, f"Bot: Could not retrieve data for {symbol}. Please try again.\n")
        chatbox.config(state=tk.DISABLED)
        return

    # Check for historical price inquiry (case insensitive and flexible)
    match_historical_price = re.match(r'.*CLOSING PRICE.* ([A-Z]+) ON (\d{4}-\d{2}-\d{2})', user_input, re.IGNORECASE)
    if match_historical_price:
        symbol = match_historical_price.group(1)
        date = match_historical_price.group(2)
        historical_price = get_historical_price(symbol, date, api_key)
        if historical_price:
            chatbox.insert(tk.END, f"Bot: The closing price of {symbol} on {date} was ${historical_price}\n")
        else:
            chatbox.insert(tk.END, f"Bot: Could not retrieve historical data for {symbol} on {date}. Please try again.\n")
        chatbox.config(state=tk.DISABLED)
        return

    # Check for company overview inquiry (case insensitive and flexible)
    match_company_overview = re.match(r'TELL ME ABOUT ([A-Z]+)', user_input, re.IGNORECASE)
    if match_company_overview:
        symbol = match_company_overview.group(1)
        overview = get_company_overview(symbol, api_key)
        if overview:
            chatbox.insert(tk.END, f"Bot: {overview}\n")
        else:
            chatbox.insert(tk.END, f"Bot: Could not retrieve company overview for {symbol}. Please try again.\n")
        chatbox.config(state=tk.DISABLED)
        return

    chatbox.insert(tk.END, "Bot: I can provide stock prices, historical prices, and company overviews. Please ask a valid question.\n")
    chatbox.config(state=tk.DISABLED)

def clear_chat():
    chatbox.config(state=tk.NORMAL)
    chatbox.delete('1.0', tk.END)
    chatbox.config(state=tk.DISABLED)

api_key = 'YOUR_ALPHA_VANTAGE_API_KEY'

root = tk.Tk()
root.title("Stock Market Chatbot")
root.geometry("600x400")

style = Style(theme="superhero")  # Choose a ttkbootstrap theme

main_frame = ttk.Frame(root, padding="20")
main_frame.pack(fill=tk.BOTH, expand=True)

entry = ttk.Entry(main_frame, width=50, font=('Arial', 14))
entry.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

send_button = ttk.Button(main_frame, text="Send", command=process_user_input)
send_button.grid(row=0, column=1, padx=5, pady=5)

clear_button = ttk.Button(main_frame, text="Clear", command=clear_chat)
clear_button.grid(row=0, column=2, padx=5, pady=5)

chatbox = tk.Text(main_frame, wrap="word", state=tk.DISABLED, font=('Arial', 12))
chatbox.grid(row=1, column=0, columnspan=3, padx=5, pady=5, sticky="nsew")

scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=chatbox.yview)
scrollbar.grid(row=1, column=3, sticky="ns")
chatbox.config(yscrollcommand=scrollbar.set)

root.mainloop()
