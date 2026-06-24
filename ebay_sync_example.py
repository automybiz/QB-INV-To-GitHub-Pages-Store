import json
import os
import urllib.request
import urllib.parse
import urllib.error
import base64

# SET YOUR DEFAULT EBAY STORE URL HERE
EBAY_STORE_URL = "https://www.ebay.com/str/europartswestllc"

# --- EBAY API CONFIGURATION ---
# Helper to parse a local .env file without external dependencies like python-dotenv
def load_dotenv():
    if os.path.exists('.env'):
        with open('.env', 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    if '=' in line:
                        key, val = line.split('=', 1)
                        os.environ[key.strip()] = val.strip()

# Load environment variables
load_dotenv()

EBAY_APP_ID = os.environ.get("EBAY_APP_ID")
EBAY_DEV_ID = os.environ.get("EBAY_DEV_ID")
EBAY_CERT_ID = os.environ.get("EBAY_CERT_ID")
EBAY_SELLER_ID = os.environ.get("EBAY_SELLER_ID", "europartswestcom")
EBAY_ENV = os.environ.get("EBAY_ENV", "production").lower()

def get_oauth_token():
    """Dynamically authenticates with eBay and obtains a 2-hour Application Access Token."""
    if not EBAY_APP_ID or not EBAY_CERT_ID:
        print("Missing EBAY_APP_ID or EBAY_CERT_ID. Cannot authenticate.")
        return None

    # Determine auth endpoint
    if EBAY_ENV == "sandbox":
        url = "https://api.sandbox.ebay.com/identity/v1/oauth2/token"
    else:
        url = "https://api.ebay.com/identity/v1/oauth2/token"

    # Base64 encode the Client ID (App ID) and Client Secret (Cert ID)
    credentials = f"{EBAY_APP_ID}:{EBAY_CERT_ID}"
    encoded_credentials = base64.b64encode(credentials.encode()).decode()

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": f"Basic {encoded_credentials}"
    }

    data = urllib.parse.urlencode({
        "grant_type": "client_credentials",
        "scope": "https://api.ebay.com/oauth/api_scope"
    }).encode("utf-8")

    req = urllib.request.Request(url, data=data, headers=headers, method="POST")
    try:
        print(f"Requesting fresh OAuth token from eBay ({EBAY_ENV})...")
        with urllib.request.urlopen(req) as response:
            res_data = json.loads(response.read().decode())
            return res_data.get("access_token")
    except urllib.error.HTTPError as e:
        print(f"Authentication failed: {e.code} - {e.reason}")
        try:
            print("Response Details:", e.read().decode())
        except Exception:
            pass
        return None
    except Exception as e:
        print(f"Error requesting OAuth token: {e}")
        return None

def fetch_ebay_data(access_token):
    """Fetches public store listings for the configured seller using the eBay Buy Browse API."""
    if not access_token:
        print("No access token provided. Falling back to mock data or exiting.")
        return None

    # Determine search endpoint
    if EBAY_ENV == "sandbox":
        base_url = "https://api.sandbox.ebay.com/buy/browse/v1/item_summary/search"
    else:
        base_url = "https://api.ebay.com/buy/browse/v1/item_summary/search"

    print(f"Syncing live listings for eBay seller: '{EBAY_SELLER_ID}'...")

    ebay_items = []
    # Set filters and paginate through all active items (max limit 200 per page)
    # Using category_ids=6028 (Motors Parts & Accessories parent category) allows retrieving all products without keywords
    params = {
        "filter": f"sellers:{{{EBAY_SELLER_ID}}}",
        "category_ids": "6028",
        "limit": "100"
    }
    
    url = f"{base_url}?{urllib.parse.urlencode(params)}"
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "X-EBAY-C-MARKETPLACE-ID": "EBAY_US"
    }

    page_count = 1
    while url:
        print(f"Fetching page {page_count}...")
        req = urllib.request.Request(url, headers=headers, method="GET")
        try:
            with urllib.request.urlopen(req) as response:
                res_data = json.loads(response.read().decode())
                summaries = res_data.get("itemSummaries", [])
                ebay_items.extend(summaries)
                
                # Check for next page URL
                url = res_data.get("next")
                if url:
                    page_count += 1
                else:
                    break
        except urllib.error.HTTPError as e:
            print(f"API request failed on page {page_count}: {e.code} - {e.reason}")
            try:
                print("Error response details:", e.read().decode())
            except Exception:
                pass
            break
        except Exception as e:
            print(f"Error fetching page {page_count}: {e}")
            break

    print(f"Successfully retrieved {len(ebay_items)} items from eBay API.")
    return ebay_items

def sync():
    # 1. Authenticate & Fetch data
    access_token = None
    new_ebay_items = []
    
    if EBAY_APP_ID and EBAY_APP_ID != "YOUR_APP_ID_HERE":
        access_token = get_oauth_token()
        if access_token:
            new_ebay_items = fetch_ebay_data(access_token)
            
    # Fallback/Demo path if credentials are still placeholder
    if not access_token or not new_ebay_items:
        print("\n--- WARNING: RUNNING WITH RECOVERY MOCK DATA ---")
        print("To fetch real products, please ensure your .env file is populated with active keys.")
        print("Continuing with premium Porsche mock items...\n")
        new_ebay_items = [
            {
                "itemId": "110552431872",
                "title": "Porsche 911 (991) LED Headlight Assembly - Right", 
                "price": {"value": "1450.00"}, 
                "itemWebUrl": EBAY_STORE_URL,
                "image": {"imageUrl": "https://images.unsplash.com/photo-1506469717960-433cebe3f181?auto=format&fit=crop&q=80&w=400"}
            },
            {
                "itemId": "110552431873",
                "title": "Porsche 911 GT3 Carbon Fiber Rear Wing Spoiler", 
                "price": {"value": "3895.00"}, 
                "itemWebUrl": EBAY_STORE_URL,
                "image": {"imageUrl": "https://images.unsplash.com/photo-1614162692292-7ac56d7f7f1e?auto=format&fit=crop&q=80&w=400"}
            },
            {
                "itemId": "110552431874",
                "title": "Porsche Cayenne Sport Steering Wheel - Alcantara", 
                "price": {"value": "925.00"}, 
                "itemWebUrl": EBAY_STORE_URL,
                "image": {"imageUrl": "https://images.unsplash.com/photo-1611859328053-3cbc9f9399f4?auto=format&fit=crop&q=80&w=400"}
            },
            {
                "itemId": "110552431875",
                "title": "Porsche 911 (997) Carrera S Front Bumper Cover", 
                "price": {"value": "1150.00"}, 
                "itemWebUrl": EBAY_STORE_URL,
                "image": {"imageUrl": "https://images.unsplash.com/photo-1503376780353-7e6692767b70?auto=format&fit=crop&q=80&w=400"}
            }
        ]
    
    # 2. Read existing products.json
    existing_products = []
    if os.path.exists('products.json'):
        try:
            with open('products.json', 'r') as f:
                existing_products = json.load(f)
        except Exception as e:
            print(f"Error reading products.json: {e}")
            existing_products = []

    # 3. Filter out OLD eBay entries
    other_source_products = [p for p in existing_products if p.get('source') != 'eBay']
    
    # 4. Format eBay products
    formatted_ebay_products = []
    for item in new_ebay_items:
        item_id = item.get('itemId', '')
        if '|' in item_id:
            # Parse clean legacy ID from REST itemId structure (e.g., 'v1|110552431872|0' -> '110552431872')
            legacy_id = item_id.split('|')[1]
        else:
            legacy_id = item_id
            
        sku = f"EB-{legacy_id}"
        price_dict = item.get('price', {})
        price_val = float(price_dict.get('value', 0.0))
        
        image_dict = item.get('image', {})
        image_url = image_dict.get('imageUrl', 'https://images.unsplash.com/photo-1503376780353-7e6692767b70?auto=format&fit=crop&q=80&w=400')
        
        formatted_ebay_products.append({
            "id": sku,
            "title": item.get('title', ''),
            "price": price_val,
            "image": image_url, 
            "sku": sku,
            "source": "eBay",
            "url": item.get('itemWebUrl', EBAY_STORE_URL)
        })

    # 5. Combine and save
    final_products = other_source_products + formatted_ebay_products
    
    with open('products.json', 'w') as f:
        json.dump(final_products, f, indent=4)
    
    print(f"\nSync Complete: Added/Updated {len(formatted_ebay_products)} eBay items from EuroPartsWest.")
    print(f"Preserved {len(other_source_products)} items from QuickBooks.")

if __name__ == "__main__":
    sync()
