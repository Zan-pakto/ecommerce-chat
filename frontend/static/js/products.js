// Product state
let currentCategory = null;
let searchQuery = '';

// DOM Elements
const productList = document.getElementById('productList');

// Initialize products
async function initProducts() {
    await loadProducts();
}

// Load products
async function loadProducts() {
    try {
        let url = '/api/products';
        const params = new URLSearchParams();
        
        if (currentCategory) {
            params.append('category_id', currentCategory);
        }
        
        if (searchQuery) {
            params.append('search', searchQuery);
        }
        
        if (params.toString()) {
            url += '?' + params.toString();
        }
        
        const response = await fetch(url);
        const products = await response.json();
        
        displayProducts(products);
    } catch (error) {
        console.error('Error loading products:', error);
    }
}

// Display products
function displayProducts(products) {
    const productList = document.getElementById('productList');
    productList.innerHTML = '';

    if (products.length === 0) {
        productList.innerHTML = `
            <div class="col-12 text-center">
                <p class="text-light">No products found matching your search.</p>
            </div>
        `;
        return;
    }

    products.forEach(product => {
        const productCard = document.createElement('div');
        productCard.className = 'col-md-6 col-lg-4 mb-4';
        productCard.innerHTML = `
            <div class="card product-card h-100">
                <div class="product-image-container">
                    <div class="image-loading">
                        <div class="spinner-border text-primary" role="status">
                            <span class="visually-hidden">Loading...</span>
                        </div>
                    </div>
                    <img src="${product.image_url}" 
                         class="card-img-top" 
                         alt="${product.name}"
                         onload="this.parentElement.classList.add('loaded')"
                         onerror="this.src='/static/images/placeholder.jpg'; this.parentElement.classList.add('loaded')">
                </div>
                <div class="card-body">
                    <h5 class="card-title">${product.name}</h5>
                    <p class="card-text">${product.description}</p>
                    <div class="product-details">
                        <span class="price">$${product.price.toFixed(2)}</span>
                        <span class="stock ${product.stock > 0 ? 'in-stock' : 'out-of-stock'}">
                            ${product.stock > 0 ? `${product.stock} in stock` : 'Out of stock'}
                        </span>
                    </div>
                    <button class="btn btn-primary mt-3 w-100" onclick="addToCart(${product.id})">
                        Add to Cart
                    </button>
                </div>
            </div>
        `;
        productList.appendChild(productCard);
    });
}

// Load categories
async function loadCategories() {
    try {
        const response = await fetch('/api/categories');
        const categories = await response.json();
        
        const categoryList = document.getElementById('categoryList');
        if (categoryList) {
            categoryList.innerHTML = `
                <li class="nav-item">
                    <a class="nav-link ${!currentCategory ? 'active' : ''}" 
                       href="#" onclick="filterByCategory(null)">All Products</a>
                </li>
                ${categories.map(category => `
                    <li class="nav-item">
                        <a class="nav-link ${currentCategory === category.id ? 'active' : ''}" 
                           href="#" onclick="filterByCategory(${category.id})">${category.name}</a>
                    </li>
                `).join('')}
            `;
        }
    } catch (error) {
        console.error('Error loading categories:', error);
    }
}

// Filter by category
function filterByCategory(categoryId) {
    currentCategory = categoryId;
    loadProducts();
}

// Search products
function searchProducts(query) {
    searchQuery = query;
    loadProducts();
}

// Add to cart (placeholder function)
function addToCart(productId) {
    // TODO: Implement cart functionality
    alert('Product added to cart!');
}

// Initialize products when page loads
document.addEventListener('DOMContentLoaded', () => {
    initProducts();
    loadCategories();
}); 