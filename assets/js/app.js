document.addEventListener('DOMContentLoaded', () => {
    const productGrid = document.getElementById('productGrid');
    const searchInput = document.getElementById('productSearch');
    const themeToggle = document.getElementById('themeToggle');
    const themeIcon = document.getElementById('themeIcon');
    let allProducts = [];

    // Theme logic
    const getPreferredTheme = () => {
        const savedTheme = localStorage.getItem('theme');
        if (savedTheme) return savedTheme;
        return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
    };

    const setTheme = (theme) => {
        document.documentElement.setAttribute('data-theme', theme);
        localStorage.setItem('theme', theme);
        updateIcon(theme);
        updateTooltip(theme);
    };

    const updateIcon = (theme) => {
        if (theme === 'dark') {
            themeIcon.innerHTML = '<circle cx="12" cy="12" r="5"></circle><line x1="12" y1="1" x2="12" y2="3"></line><line x1="12" y1="21" x2="12" y2="23"></line><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"></line><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"></line><line x1="1" y1="12" x2="3" y2="12"></line><line x1="21" y1="12" x2="23" y2="12"></line><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"></line><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"></line>';
        } else {
            themeIcon.innerHTML = '<path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path>';
        }
    };

    const updateTooltip = (theme) => {
        themeToggle.title = theme === 'dark' ? 'Switch to Light Mode' : 'Switch to Dark Mode';
    };

    themeToggle.addEventListener('click', () => {
        const currentTheme = document.documentElement.getAttribute('data-theme');
        const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
        setTheme(newTheme);
    });

    // Initialize theme
    setTheme(getPreferredTheme());

    // Fetch products from JSON
    fetch('products.json')
        .then(response => response.json())
        .then(data => {
            allProducts = data;
            displayProducts(allProducts);
        })
        .catch(error => {
            console.error('Error loading products:', error);
            productGrid.innerHTML = '<p class="error">Failed to load products. Please try again later.</p>';
        });

    // Display products in the grid
    function displayProducts(products) {
        if (products.length === 0) {
            productGrid.innerHTML = '<p class="no-results">No products found.</p>';
            return;
        }

        productGrid.innerHTML = products.map(product => `
            <div class="product-card">
                <img src="${product.image}" alt="${product.title}" class="product-img">
                <div class="product-info">
                    <h3 class="product-title">${product.title}</h3>
                    <p class="product-price">$${product.price.toFixed(2)}</p>
                    <div class="product-meta">
                        <span>SKU: ${product.sku}</span><br>
                        <span>Source: ${product.source}</span>
                    </div>
                    <a href="${product.url}" class="btn" style="width: 100%; text-align: center;" target="_blank">View Details</a>
                </div>
            </div>
        `).join('');
    }

    // Search functionality
    searchInput.addEventListener('input', (e) => {
        const searchTerm = e.target.value.toLowerCase();
        const filteredProducts = allProducts.filter(product => 
            product.title.toLowerCase().includes(searchTerm) || 
            product.sku.toLowerCase().includes(searchTerm)
        );
        displayProducts(filteredProducts);
    });
});
