import json
import os
import subprocess

# Conceptual QuickBooks Sync Script
# This would run locally on the machine with QuickBooks installed.

def fetch_quickbooks_data():
    # In a real scenario, you would use a library like 'win32com' to talk to the QB SDK
    # or export a report to CSV. For this example, we'll simulate the data.
    print("Querying QuickBooks ItemInventory...")
    
    # Mock data representing what you'd pull from QB
    qb_items = [
        {"FullName": "Brake Pad Set", "SalesPrice": 45.99, "Name": "BK-12345"},
        {"FullName": "Spark Plug", "SalesPrice": 8.75, "Name": "SP-5544"},
        {"FullName": "Serpentine Belt", "SalesPrice": 34.20, "Name": "SB-1122"},
    ]
    return qb_items

def sync():
    items = fetch_quickbooks_data()
    products = []

    for item in items:
        sku = item['Name']
        products.append({
            "id": f"EPW-{sku}",
            "title": item['FullName'],
            "price": item['SalesPrice'],
            # Method 1: Using the Naming Convention for images
            "image": f"assets/img/products/{sku}.jpg", 
            "sku": sku,
            "source": "QuickBooks",
            "url": "#"
        })

    # Write to the JSON file
    with open('products.json', 'w') as f:
        json.dump(products, f, indent=4)
    print("Updated products.json with latest QuickBooks data.")

    # Optional: Automatically push to GitHub
    # print("Pushing to GitHub...")
    # subprocess.run(["git", "add", "products.json"])
    # subprocess.run(["git", "commit", "-m", "Sync inventory from QuickBooks"])
    # subprocess.run(["git", "push"])

if __name__ == "__main__":
    sync()
