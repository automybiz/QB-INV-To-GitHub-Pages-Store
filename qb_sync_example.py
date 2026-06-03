import json
import os

# Conceptual QuickBooks Sync Script
# This runs locally on the machine with QuickBooks installed.

def fetch_quickbooks_data():
    # In a real scenario, you would use the QB SDK (QBXML)
    # For this demo, we use high-quality Porsche-related mock data
    print("Querying QuickBooks ItemInventory...")
    
    qb_items = [
        {
            "FullName": "911 Carrera Brake Pads (Set)", 
            "SalesPrice": 245.99, 
            "Name": "P-911-BK",
            "Image": "https://images.unsplash.com/photo-1486006396193-c81d3afd0a3a?auto=format&fit=crop&q=80&w=400"
        },
        {
            "FullName": "Porsche Synthetic Oil Filter", 
            "SalesPrice": 32.50, 
            "Name": "P-OIL-FL",
            "Image": "https://images.unsplash.com/photo-1580273916550-e323be2ae537?auto=format&fit=crop&q=80&w=400"
        },
        {
            "FullName": "911 GT3 Spark Plug - High Perf", 
            "SalesPrice": 18.75, 
            "Name": "P-GT3-SP",
            "Image": "https://images.unsplash.com/photo-1635773107091-24097471923e?auto=format&fit=crop&q=80&w=400"
        },
    ]
    return qb_items

def sync():
    # 1. Fetch data from QB
    new_qb_items = fetch_quickbooks_data()
    
    # 2. Read existing products.json
    existing_products = []
    if os.path.exists('products.json'):
        try:
            with open('products.json', 'r') as f:
                existing_products = json.load(f)
        except Exception as e:
            print(f"Error reading products.json: {e}")
            existing_products = []

    # 3. Filter out OLD QuickBooks entries (keep eBay or other sources)
    # This is the "Merge" logic that prevents overwriting other sources
    other_source_products = [p for p in existing_products if p.get('source') != 'QuickBooks']
    
    # 4. Format new QB items
    formatted_qb_products = []
    for item in new_qb_items:
        sku = item['Name']
        formatted_qb_products.append({
            "id": f"QB-{sku}",
            "title": item['FullName'],
            "price": item['SalesPrice'],
            "image": item['Image'], 
            "sku": sku,
            "source": "QuickBooks",
            "url": "#"
        })

    # 5. Combine and save
    final_products = other_source_products + formatted_qb_products
    
    with open('products.json', 'w') as f:
        json.dump(final_products, f, indent=4)
    
    print(f"Sync Complete: Added/Updated {len(formatted_qb_products)} QuickBooks items.")
    print(f"Preserved {len(other_source_products)} items from other sources.")

if __name__ == "__main__":
    sync()
