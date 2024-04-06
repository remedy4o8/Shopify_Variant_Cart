import requests
from urllib.parse import urlparse
import webbrowser

# URL of the JSON file
url = ""

def print_product_details(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        # Check if 'products' is empty or not present
        if not data.get('products'):  # This checks if 'products' is empty or not present
            print("No products found. Exiting script.")
            return

        # Process each product
        for product in data['products']:
            product_title = product.get('title')
            print(f"Product Title: {product_title}")

            for variant in product.get('variants', []):
                variant_id = variant.get('id')
                price = variant.get('price')
                size = variant.get('option1')
                color = variant.get('option2')
                print(f"    Variant ID: {variant_id}, Price: {price}, Size: {size}, Color: {color}")

    except requests.RequestException as e:
        print(f"Error fetching data: {e}")
        return

    # Parse the domain from the provided URL
    parsed_url = urlparse(url)
    shop_url = f"{parsed_url.scheme}://{parsed_url.netloc}"

    cart_items = []
    while True:
        # Prompt the user to enter the variant ID
        user_variant_id = input("Enter the Variant ID you want to add to the cart: ")
        cart_items.append(f"{user_variant_id}:1")

        # Ask if the user wants to add more variants
        add_more = input("Do you want to add more variants? (yes/no): ")
        if add_more.lower() != 'yes':
            break

    # Construct the cart URL
    cart_url = f"{shop_url}/cart/" + ','.join(cart_items)+"?discount=LSVIP"
    print(f"URL to add the selected variants to the cart: {cart_url}")

    # Ask the user if they want to open the URL in Chrome
    open_in_chrome = input("Do you want to open the cart in Chrome? (yes/no): ")
    if open_in_chrome.lower() == 'yes':
        # Open the URL in Chrome (or default browser)
        webbrowser.open_new(cart_url)



print_product_details(url)
