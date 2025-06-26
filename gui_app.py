import tkinter as tk
from tkinter import messagebox
import ebay_api  # This imports your API logic

# Function to handle the search and display the results
def on_search():
    query = entry_product.get()
    if not query:
        messagebox.showwarning("Input Error", "Please enter a product name.")
        return

    try:
        access_token = ebay_api.get_access_token()

        sold_items = ebay_api.search_ebay(query, access_token, sold=True, limit=50)
        active_items = ebay_api.search_ebay(query, access_token, sold=False, limit=50)

        if not sold_items and not active_items:
            messagebox.showwarning("No Results", "No sold or active listings found for this product.")
            return

        # Calculate Sell-Through Rate
        sold_count = len(sold_items)
        active_count = len(active_items)
        str_percent = ebay_api.calculate_sell_through_rate(sold_count, active_count)

        display_results(sold_items, active_items, str_percent)
        ebay_api.save_to_csv(sold_items + active_items)

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

# Function to display results in the interface
# Function to display results in the interface
def display_results(sold_items, active_items, str_percent):
    results_text.delete(1.0, tk.END)

    # Combine sold and active items for price stats
    all_items = sold_items + active_items

    # Calculate price statistics (min, max, average)
    prices = [float(item['price']['value']) for item in all_items if 'price' in item and 'value' in item['price']]
    
    if prices:
        min_price = min(prices)
        max_price = max(prices)
        avg_price = sum(prices) / len(prices)
    else:
        min_price = max_price = avg_price = 'N/A'

    # Insert the sell-through rate and price stats at the top
    results_text.insert(tk.END, f"Sell-Through Rate: {str_percent:.2f}%\n\n")
    results_text.insert(tk.END, f"Min Price: ${min_price}\nMax Price: ${max_price}\nAverage Price: ${avg_price:.2f}\n\n")

    # Display sold items
    results_text.insert(tk.END, "=== SOLD ITEMS ===\n")
    for item in sold_items:
        title = item.get('title', 'No Title')
        price = item.get('price', {}).get('value', 'N/A')
        currency = item.get('price', {}).get('currency', '')
        condition = item.get('condition', 'Unknown')
        url = item.get('itemUrl', 'No URL')
        results_text.insert(tk.END, f"{title}\nPrice: {price} {currency}\nCondition: {condition}\nURL: {url}\n\n")

    # Display active listings
    results_text.insert(tk.END, "=== ACTIVE LISTINGS ===\n")
    for item in active_items:
        title = item.get('title', 'No Title')
        price = item.get('price', {}).get('value', 'N/A')
        currency = item.get('price', {}).get('currency', '')
        condition = item.get('condition', 'Unknown')
        url = item.get('itemUrl', 'No URL')
        results_text.insert(tk.END, f"{title}\nPrice: {price} {currency}\nCondition: {condition}\nURL: {url}\n\n")

# GUI setup
root = tk.Tk()
root.title("eBay Product Research Tool")

label_product = tk.Label(root, text="Enter Product Name:")
label_product.pack()

entry_product = tk.Entry(root, width=50)
entry_product.pack()

search_button = tk.Button(root, text="Search Listings", command=on_search)
search_button.pack()

results_text = tk.Text(root, height=25, width=80)
results_text.pack()

root.mainloop()
