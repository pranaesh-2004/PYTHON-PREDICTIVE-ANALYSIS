import tkinter as tk
from tkinter import messagebox, simpledialog
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime
import matplotlib.dates as mdates
from mplfinance.original_flavor import candlestick_ohlc
df = pd.read_excel(r"C:\Users\dushyanth m\Documents\PREDICTIVE ANALYSI\USDINR=X.xlsx")
print(df.columns)

root = tk.Tk()
root.title("Stock Trading")

cash_balance = 10000

fig, ax = plt.subplots()
canvas = FigureCanvasTkAgg(fig, master=root)
canvas_widget = canvas.get_tk_widget()
canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=True)  
canvas_widget.config(width=800)  


pointer = 0
buy_stack = [] 
sell_stack = []
annotations = {}

buy_df = pd.DataFrame(columns=['Share Price', 'Multiplier', 'Date'])
sell_df = pd.DataFrame(columns=['Share Price', 'Multiplier', 'Date', 'Sell Price'])

def save_transactions_to_excel():
    with pd.ExcelWriter(r"C:\Users\dushyanth m\Downloads\AUDINR=X2.xlsx", engine='openpyxl') as writer:
        buy_df.to_excel(writer, sheet_name='Buy Transactions', index=False)
        sell_df.to_excel(writer, sheet_name='Sell Transactions', index=False)

def buy_button_action(current_value, multiplier):
    global pointer, cash_balance
    multiplier = float(multiplier)
    share_price = current_value * multiplier
    current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if multiplier >=1:  
        if share_price <= cash_balance:
            messagebox.showinfo("Buy Stock", f"You bought the stock for {share_price} at index {pointer} with multiplier {multiplier} on {current_date}")
            cash_balance -= share_price
            pointer += 1 
            buy_stack.append((share_price, multiplier, current_date))
            new_entry = {'Share Price': share_price, 'Multiplier': multiplier, 'Date': current_date}
            buy_df.loc[len(buy_df)] = new_entry
            update_price_label()
            save_transactions_to_excel()

            
        else:
            messagebox.showerror("Insufficient Funds", "You do not have enough funds to buy this stock.")

def sell_button_action(current_value, multiplier):
    global cash_balance, pointer, sell_stack, buy_stack, sell_df
    
    total_sell_amount = 0  
    
    if buy_stack:
        remaining_multiplier = float(multiplier)
        
        if sum(stock[1] for stock in buy_stack) > 0:  
            while remaining_multiplier > 0 and buy_stack:
                share_price, stock_multiplier, current_date = buy_stack[0]  
                if stock_multiplier >= 1:  
                    if stock_multiplier >= remaining_multiplier:
                        sell_price = current_value * remaining_multiplier
                        cash_balance += sell_price
                        total_sell_amount += sell_price
                        buy_stack[0] = (share_price, stock_multiplier - remaining_multiplier, current_date) 
                        sell_stack.append((share_price, remaining_multiplier, current_date, sell_price))
                        new_entry = {'Share Price': share_price, 'Multiplier': remaining_multiplier, 'Date': current_date, 'Sell Price': sell_price}
                        sell_df.loc[len(sell_df)] = new_entry
                        remaining_multiplier = 0  
                    else:
                        sell_price = current_value * stock_multiplier
                        cash_balance += sell_price
                        total_sell_amount += sell_price
                        sell_stack.append((share_price, stock_multiplier, current_date, sell_price))
                        new_entry = {'Share Price': share_price, 'Multiplier': stock_multiplier, 'Date': current_date, 'Sell Price': sell_price}
                        sell_df.loc[len(sell_df)] = new_entry
                        update_price_label()
                        remaining_multiplier -= stock_multiplier
                        buy_stack.pop(0)  
                else:
                    messagebox.showerror("Invalid Multiplier", "Multiplier should be greater than or equal to 1.")
                    return  
            
            messagebox.showinfo("Sell Stock", f"Selling completed successfully. Total selling price: ${total_sell_amount:.2f}")
            save_transactions_to_excel()
        else:
            messagebox.showerror("Error", "No stocks available to sell.")
    else:
        messagebox.showerror("Error", "No stocks available to sell.")

def update_plot():
    global pointer
    ax.clear()  
    
    ohlc = df[['Name', 'Open', 'High', 'Low', 'Close','Comment','SMA']].iloc[:pointer+1]
    
    ohlc['Name'] = pd.factorize(ohlc['Name'])[0]  
    
    candlestick_ohlc(ax, ohlc[['Name', 'Open', 'High', 'Low', 'Close']].values, width=0.6, colorup='g', colordown='r', alpha=0.7)
    
    ax.plot(range(len(ohlc)), ohlc['SMA'], label='SMA', color='blue')  
    
    ax.set_xticks(range(len(ohlc)))
    ax.set_xticklabels(ohlc['Name'])
    
    for i, (name, open_price, high_price) in enumerate(zip(ohlc['Name'], ohlc['Open'], ohlc['High'])):
        comment = df['Comment'].iloc[i]
        if pd.notnull(comment):
            if len(comment.split()) > 20:  
            
                lines = [comment[i:i+50] for i in range(0, len(comment), 50)]  
            
                annotation_text = '\n'.join(lines)
            else:
                annotation_text = comment
        
            if i not in annotations:
                annotations[i] = ax.annotate(annotation_text, (i, high_price), xytext=(0, 5), textcoords='offset points', ha='center', fontsize=8, visible=True)
            else:
                annotations[i].xy = (i, high_price)
                annotations[i].set_text(annotation_text)
                annotations[i].set_visible(True)  
        else:
            if i in annotations:
                annotations[i].set_visible(False)
     
    canvas.draw()
    

    if pointer < len(df) - 1:
        pointer += 1  
        update_price_label()  
        root.after(1500, update_plot)  
    else:
        current_value = df['Close'].iloc[pointer]  
        buy_button.config(command=lambda val=current_value: buy_button_action(val, multiplier_entry.get())) 
        sell_button.config(command=lambda val=current_value: sell_button_action(val, multiplier_entry.get()))
        update_price_label()


    canvas.draw()


def update_price_label():
    current_price_label.config(text=f"Current Price: {df['Open'][pointer]}")   

def print_buy_history():
    buy_history = "\n".join([f"Stock: {stock}, Multiplier: {multiplier}, Date: {date}" for stock, multiplier, date in buy_stack if multiplier >= 1])
    messagebox.showinfo("Buy History", f"Buy History:\n{buy_history}")

def print_sell_stack():
    sell_history = "\n".join([f"Stock: {share_price}, Multiplier: {multiplier}, Date: {date}" for share_price, multiplier, date, _ in sell_stack])
    messagebox.showinfo("Sell History", f"Sell History:\n{sell_history}")

def validate_multiplier():
    multiplier = multiplier_entry.get()
    if multiplier:
        share_price = df['Open'][pointer]
        if share_price * float(multiplier) <= cash_balance:
            buy_button_action(share_price, multiplier)
        else:
            messagebox.showerror("Insufficient Funds", "You do not have enough funds to buy this stock.")
    else:
        messagebox.showerror("Error", "Multiplier field is required.")

def show_balance():
    messagebox.showinfo("Cash Balance", f"Available Cash: ${cash_balance}")

def add_cash():
    global cash_balance
    amount = simpledialog.askfloat("Add Cash", "Enter the amount to add:")
    if amount is not None:
        cash_balance += amount
        messagebox.showinfo("Add Cash", f"${amount} added successfully. New balance: ${cash_balance}")

start_button = tk.Button(root, text="Start Animation", command=update_plot)
start_button.pack()

multiplier_label = tk.Label(root, text="Multiplier: ")
multiplier_label.pack()

multiplier_entry = tk.Entry(root)
multiplier_entry.pack()

buy_button = tk.Button(root, text="BUY", command=validate_multiplier)
buy_button.pack()

print_stack_button = tk.Button(root, text="Purchase History", command=print_buy_history)
print_stack_button.pack()

sell_button = tk.Button(root, text="Sell History", command=print_sell_stack)
sell_button.pack()

account_balance_button = tk.Button(root, text="Account Balance", command=show_balance)
account_balance_button.pack()

add_cash_button = tk.Button(root, text="Add Cash", command=add_cash)
add_cash_button.pack()

current_price_label = tk.Label(root, text="Current Price: ")
current_price_label.pack()

sell_button = tk.Button(root, text="SELL", command=lambda: sell_button_action(df['Open'][pointer], multiplier_entry.get()))
sell_button.pack()

root.mainloop()
