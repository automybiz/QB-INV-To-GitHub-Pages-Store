document.addEventListener('DOMContentLoaded', () => {
    const productGrid = document.getElementById('productGrid');
    const searchInput = document.getElementById('productSearch');
    let allProducts = [];

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
