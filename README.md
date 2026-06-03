# EuroPartsWest Store Mirror

This is a lightweight, high-performance store front designed to be hosted for free on **GitHub Pages**. It populates product data from a single `products.json` file, allowing you to mirror inventory from QuickBooks, eBay, or both.

## 💻 Local Development & Testing

Due to browser security (CORS), the product list will not load if you open `index.html` directly from your file system (`file://`).

**To test locally:**
1.  Open the project folder in **VS Code**.
2.  Install the **Live Server** extension.
3.  Right-click `index.html` and select **Open with Live Server**.

## 🚀 How to Launch on GitHub Pages (Free Hosting)

1.  Create a new repository on GitHub (e.g., `euro-parts-store`).
2.  Upload these files to the repository.
3.  Go to **Settings > Pages**.
4.  Under "Build and deployment", set "Source" to **Deploy from a branch**.
5.  Select the `main` branch and `/ (root)` folder. Click **Save**.
6.  Your site will be live at `https://your-username.github.io/euro-parts-store/`.
7.  **Custom Domain:** In the same Pages settings, you can add `EuroPartsWest.com`. You will need to update your DNS settings (A records and CNAME) at your domain registrar (e.g., GoDaddy, Namecheap).

---

## 📦 How to Populate Products

This website uses `products.json` as its database. You can update this file in two ways:

### 1. From QuickBooks (Automated Sync)
QuickBooks is your primary inventory management tool. To sync it with this website:

#### **Strategy A: QuickBooks Desktop**
1.  **Local Sync Script:** Run the included `qb_sync_example.py` on the computer where QuickBooks is installed.
2.  **Merge-Aware:** This script is designed to update only the "QuickBooks" products in `products.json`, preserving any data from eBay or other sources.
3.  **Auto-Push:** You can uncomment the Git lines in the script to have it automatically push updates to your live site.

#### **Strategy B: QuickBooks Online**
1.  **API Integration:** Use a GitHub Action or a small middleware server to pull data from the QuickBooks Online API.
2.  **Scheduled Updates:** Set the sync to run every hour or every day to keep the site current.

---

### 🖼️ How to Associate Images
QuickBooks is great for numbers, but poor for images. **Do not try to store image data inside QuickBooks.** Instead, use one of these two professional methods:

#### **Method 1: The "Naming Convention" (Easiest)**
*   Name your image files exactly like your QuickBooks **Part Number** or **SKU**.
*   *Example:* If your QB Part Number is `BK-12345`, save your image as `assets/img/products/BK-12345.jpg`.
*   The website script can then automatically "predict" the image URL based on the SKU.

#### **Method 2: Custom Fields**
*   In QuickBooks, create a **Custom Field** named `ImageURL`.
*   Paste the link to the image (from Imgur, AWS, or your eBay store) into that field.
*   Your sync script will pull this URL and put it into `products.json`.

### 2. Mirroring eBay Store (Automated)
To sync your eBay store alongside your QuickBooks inventory:

1.  **eBay Sync Script:** Run the included `ebay_sync_example.py`.
2.  **GitHub Actions:** You can set this script to run automatically every night using GitHub Actions. It will pull your latest eBay listings and merge them into `products.json`.
3.  **Cross-Source Preservation:** Like the QB script, this script only touches "eBay" source items, leaving your QuickBooks data untouched.

---

## 🛠️ Customization

*   **Colors:** Edit `assets/css/styles.css` and change the `--primary` variable to match your branding.
*   **Logo/Hero:** Replace the text in `index.html` and the background image URL in the CSS.

## 🧪 Testing the Sync Scripts
I've included two blueprints for your automation: `qb_sync_example.py` and `ebay_sync_example.py`.

1.  **Install Python:** From [python.org](https://python.org).
2.  **Run QuickBooks Sync:**
    ```bash
    python qb_sync_example.py
    ```
3.  **Run eBay Sync:**
    ```bash
    python ebay_sync_example.py
    ```
4.  **Observe Results:** Open `products.json` or refresh your local web server. You will see both sources successfully merged into a single storefront.

## 💡 Why this approach?
*   **Zero Hosting Cost:** GitHub Pages is completely free.
*   **Blazing Fast:** Static files load instantly compared to heavy WordPress or Shopify sites.
*   **Secure:** No database to hack, no plugins to update.
*   **Scalable:** Can handle thousands of products and millions of visitors.
