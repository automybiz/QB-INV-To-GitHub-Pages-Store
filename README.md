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
QuickBooks is your "Source of Truth." To sync it with this website:

#### **Strategy A: QuickBooks Desktop (Recommended for Parts Stores)**
1.  **Local Sync Script:** Run a small Python or Node.js script on the computer where QuickBooks is installed.
    *   *Note: I've included a template called `qb_sync_example.py` in this repo. You only need to install Python if you intend to use this automation script.*
2.  **SDK Access:** The script uses the [QuickBooks SDK (QBXML)](https://developer.intuit.com/app/developer/qbdesktop/docs/get-started) to pull `ItemInventory` queries.
3.  **JSON Export:** The script converts the results into the `products.json` format.
4.  **Auto-Push:** The script then runs `git add products.json`, `git commit`, and `git push` to update the website instantly.

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
*   You can use a **GitHub Action** (free) to automatically fetch your eBay listings once a day.
*   The Action would run a script that calls the eBay Browse/Finding API, formats the data, and updates `products.json` directly in the repository.
*   This keeps your website perfectly in sync with eBay without you doing anything.

---

## 🛠️ Customization

*   **Colors:** Edit `assets/css/styles.css` and change the `--primary` variable to match your branding.
*   **Logo/Hero:** Replace the text in `index.html` and the background image URL in the CSS.

## 🧪 Testing the Sync Script (Optional)
I included `qb_sync_example.py` as a blueprint for your automation. 
*   **If you see a prompt to install Python:** You only need to do this if you want to run the automation script on your machine.
*   **To run the mock sync:**
    1. Install Python from [python.org](https://python.org).
    2. Open your terminal in this folder.
    3. Run `python qb_sync_example.py`.
    4. Watch `products.json` update automatically!

## 💡 Why this approach?
*   **Zero Hosting Cost:** GitHub Pages is completely free.
*   **Blazing Fast:** Static files load instantly compared to heavy WordPress or Shopify sites.
*   **Secure:** No database to hack, no plugins to update.
*   **Scalable:** Can handle thousands of products and millions of visitors.
