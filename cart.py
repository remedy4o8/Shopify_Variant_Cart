import requests
from urllib.parse import urlparse, quote
import subprocess
import sys

def fetch_data(url):
    """
    Fetch data from the given URL and return the JSON response.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching data: {e}")
        return None

def display_product_details(data):
    """
    Display product details from the provided data.
    """
    if not data.get('products'):
        print("No products found. Exiting script.")
        return

    for product in data['products']:
        product_title = product.get('title')
        print(f"Product Title: {product_title}")

        for variant in product.get('variants', []):
            variant_id = variant.get('id')
            price = variant.get('price')
            size = variant.get('option1')
            color = variant.get('option2')
            print(f"    Variant ID: {variant_id}, Price: {price}, Size: {size}, Color: {color}")

def get_cart_url(parsed_url, cart_items):
    """
    Construct and return the cart URL with the selected items and discount code.
    """
    shop_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
    cart_items_encoded = ','.join([quote(f"{item}:1") for item in cart_items])  # Ensure each part is URL-encoded
    cart_url = f"{shop_url}/cart/{cart_items_encoded}?discount=LSVIP"
    return cart_url

def handle_cart_interaction(parsed_url):
    """
    Handle user interaction for adding items to the cart and return the cart URL.
    """
    cart_items = []
    while True:
        user_variant_id = input("Enter the Variant ID you want to add to the cart: ")
        cart_items.append(user_variant_id.strip())

        add_more = input("Do you want to add more variants? (yes/no): ").lower()
        if add_more != 'yes':
            break

    return get_cart_url(parsed_url, cart_items)

def open_cart_url(cart_url):
    """
    Automatically opens the cart URL in a browser's incognito mode without user input.
    """
    # Open the browser in incognito mode
    if sys.platform == 'win32':
        # Windows
        subprocess.Popen(['start', 'chrome', '--incognito', cart_url], shell=True)
    elif sys.platform == 'darwin':
        # macOS
        subprocess.Popen(['open', '-na', 'Google Chrome', '--args', '--incognito', cart_url])
    elif sys.platform == 'linux' or sys.platform == 'linux2':
        # Linux
        subprocess.Popen(['google-chrome', '--incognito', cart_url])
    else:
        # If not recognized or supported, just open without incognito
        webbrowser.open_new(cart_url)

def main(url):
    """
    Main function to orchestrate the fetching, displaying, and interaction with the product details.
    """
    data = fetch_data(url)
    if data:
        display_product_details(data)
        parsed_url = urlparse(url)
        cart_url = handle_cart_interaction(parsed_url)
        print(f"URL to add the selected variants to the cart: {cart_url}")
        open_cart_url(cart_url)

# URL of the JSON file
url = "https://littlesleepies.com/collections/vip-early-access/products.json"

main(url)
