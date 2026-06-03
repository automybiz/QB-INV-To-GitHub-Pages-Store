# EuroPartsWest Store Mirror

This is a lightweight, high-performance store front designed to be hosted for free on **GitHub Pages**. It populates product data from a single `products.json` file, allowing you to mirror inventory from QuickBooks, eBay, or both.

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

### 1. From QuickBooks (Manual or Automated)
*   **Manual:** Export your QuickBooks inventory to Excel/CSV. Convert that CSV to JSON format matching the structure in `products.json`.
*   **Automated:** Use a small Python script (which can run on your local PC) that uses the QuickBooks SDK to read your database and overwrite the `products.json` file, then automatically `git push` it to GitHub.

### 2. Mirroring eBay Store (Automated)
*   You can use a **GitHub Action** (free) to automatically fetch your eBay listings once a day.
*   The Action would run a script that calls the eBay Browse/Finding API, formats the data, and updates `products.json` directly in the repository.
*   This keeps your website perfectly in sync with eBay without you doing anything.

---

## 🛠️ Customization

*   **Colors:** Edit `assets/css/styles.css` and change the `--primary` variable to match your branding.
*   **Logo/Hero:** Replace the text in `index.html` and the background image URL in the CSS.

## 💡 Why this approach?
*   **Zero Hosting Cost:** GitHub Pages is completely free.
*   **Blazing Fast:** Static files load instantly compared to heavy WordPress or Shopify sites.
*   **Secure:** No database to hack, no plugins to update.
*   **Scalable:** Can handle thousands of products and millions of visitors.
