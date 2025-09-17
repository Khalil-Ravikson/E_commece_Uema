// Current user ID (in a real app, this would come from authentication)
const userId = 1;

// Cart data
let cart = [];

// Fetch products from API
let products = [];

// Initialize the app
document.addEventListener('DOMContentLoaded', function() {
    AOS.init();
    feather.replace();

    fetch('/api/products/')
        .then(response => response.json())
        .then(data => {
            products = data.products;
            renderProducts();
        })
        .catch(error => console.error('Error fetching products:', error));

    fetch(`/api/cart/${userId}/`)
        .then(response => response.json())
        .then(data => {
            cart = data.cart || [];
            updateCart();
        })
        .catch(error => console.error('Error loading cart:', error));

    const mobileMenuButton = document.querySelector('.mobile-menu-button');
    const mobileMenu = document.querySelector('.mobile-menu');
    mobileMenuButton.addEventListener('click', () => mobileMenu.classList.toggle('hidden'));

    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            const href = this.getAttribute('href');
            if (href === '#cart' || this.getAttribute('onclick')) {
                return;
            }
            e.preventDefault();
            const targetElement = document.querySelector(href);
            if (targetElement) {
                targetElement.scrollIntoView({ behavior: 'smooth' });
                mobileMenu.classList.add('hidden');
            }
        });
    });

    // ======================================================================================
    // FIX RESPONSIVIDADE: Adiciona o evento de clique a TODOS os links do carrinho (desktop e mobile)
    // ======================================================================================
    document.querySelectorAll('a[href="#cart"]').forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault(); // Impede que o "#cart" apareça na URL
            openCart();
            mobileMenu.classList.add('hidden'); // Garante que o menu mobile feche
        });
    });

    document.getElementById('close-cart').addEventListener('click', closeCart);
    document.getElementById('checkout-btn').addEventListener('click', showCheckout);
    document.getElementById('checkout-form').addEventListener('submit', confirmOrder);
});

function renderProducts() {
    const productsContainer = document.querySelector('#products .grid');
    productsContainer.innerHTML = '';
    products.forEach(product => {
        const productCard = document.createElement('div');
        productCard.className = 'product-card bg-white rounded-lg shadow-md overflow-hidden transition-all';
        productCard.setAttribute('data-aos', 'fade-up');
        productCard.innerHTML = `
            <img src="${product.image}" alt="${product.name}" class="w-full h-48 object-cover">
            <div class="p-4">
                <h3 class="font-bold text-lg mb-2">${product.name}</h3>
                <p class="text-gray-600 text-sm mb-4">${product.description}</p>
                <div class="flex justify-between items-center">
                    <span class="font-bold text-lg">R$ ${product.price.toFixed(2).replace('.', ',')}</span>
                    <button class="add-to-cart bg-blue-500 text-white py-2 px-4 rounded-lg hover:bg-blue-600 transition duration-300" data-id="${product.id}">
                        Adicionar
                    </button>
                </div>
            </div>
        `;
        productsContainer.appendChild(productCard);
    });
    
    document.querySelectorAll('.add-to-cart').forEach(button => {
        button.addEventListener('click', function() {
            const productId = parseInt(this.getAttribute('data-id'));
            addToCart(productId);
        });
    });
}

function addToCart(productId) {
    fetch(`/api/cart/${userId}/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'X-CSRFToken': getCookie('csrftoken') },
        body: JSON.stringify({ product_id: productId, quantity: 1 })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            cart = data.cart;
            updateCart();
            showCartNotification();
        }
    })
    .catch(error => console.error('Error adding to cart:', error));
}

function updateCart() {
    const totalItems = cart.reduce((sum, item) => sum + item.quantity, 0);
    
    // ======================================================================================
    // FIX RESPONSIVIDADE: Atualiza TODOS os contadores (desktop e mobile) usando a classe
    // ======================================================================================
    document.querySelectorAll('.cart-counter').forEach(counter => {
        counter.textContent = totalItems;
    });

    const cartItemsContainer = document.getElementById('cart-items');
    const cartTotalElement = document.getElementById('cart-total');

    if (cart.length === 0) {
        cartItemsContainer.innerHTML = `<div class="text-center py-8 text-gray-500"><i data-feather="shopping-cart" class="mx-auto w-12 h-12 mb-4"></i><p>Seu carrinho está vazio</p></div>`;
        cartTotalElement.textContent = 'R$ 0,00';
    } else {
        let cartHTML = '';
        let total = 0;
        cart.forEach(item => {
            total += item.price * item.quantity;
            cartHTML += `
                <div class="cart-item flex items-center py-4 border-b">
                    <img src="${item.image}" alt="${item.name}" class="w-16 h-16 object-cover rounded">
                    <div class="ml-4 flex-1">
                        <h4 class="font-semibold">${item.name}</h4>
                        <p class="text-gray-600">R$ ${item.price.toFixed(2).replace('.', ',')}</p>
                    </div>
                    <div class="flex items-center">
                        <button class="decrease-quantity text-gray-500 px-2" data-id="${item.id}">-</button>
                        <span class="mx-2">${item.quantity}</span>
                        <button class="increase-quantity text-gray-500 px-2" data-id="${item.id}">+</button>
                        <button class="remove-item text-red-500 ml-4" data-id="${item.id}"><i data-feather="trash-2" class="w-4 h-4"></i></button>
                    </div>
                </div>
            `;
        });
        cartItemsContainer.innerHTML = cartHTML;
        cartTotalElement.textContent = `R$ ${total.toFixed(2).replace('.', ',')}`;
    }

    const checkoutTotalEl = document.getElementById('checkout-total');
    if (checkoutTotalEl) {
        const currentTotal = cart.reduce((sum, item) => sum + item.price * item.quantity, 0);
        checkoutTotalEl.textContent = `R$ ${currentTotal.toFixed(2).replace('.', ',')}`;
    }
    
    addCartItemListeners();
    feather.replace();
}

function addCartItemListeners() {
    document.querySelectorAll('.decrease-quantity').forEach(button => button.addEventListener('click', e => adjustQuantity(parseInt(e.currentTarget.dataset.id), -1)));
    document.querySelectorAll('.increase-quantity').forEach(button => button.addEventListener('click', e => adjustQuantity(parseInt(e.currentTarget.dataset.id), 1)));
    document.querySelectorAll('.remove-item').forEach(button => button.addEventListener('click', e => removeFromCart(parseInt(e.currentTarget.dataset.id))));
}

function adjustQuantity(productId, change) {
    const item = cart.find(item => item.id === productId);
    if (!item) return;
    const newQuantity = item.quantity + change;
    if (newQuantity <= 0) {
        removeFromCart(productId);
    } else {
        item.quantity = newQuantity;
        updateCart();
        fetch(`/api/cart/${userId}/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json', 'X-CSRFToken': getCookie('csrftoken') },
            body: JSON.stringify({ product_id: productId, quantity_change: change })
        })
        .then(response => response.json())
        .then(data => { if(data.success) cart = data.cart; else updateCart(); })
        .catch(error => console.error('Error adjusting quantity:', error));
    }
}

function removeFromCart(productId) {
    cart = cart.filter(item => item.id !== productId);
    updateCart();
    fetch(`/api/cart/${userId}/`, {
        method: 'DELETE',
        headers: { 'Content-Type': 'application/json', 'X-CSRFToken': getCookie('csrftoken') },
        body: JSON.stringify({ product_id: productId })
    })
    .then(response => response.json())
    .then(data => { if(data.success) cart = data.cart; else updateCart(); })
    .catch(error => console.error('Error removing from cart:', error));
}

function openCart() {
    document.getElementById('cart-modal').classList.remove('hidden');
    document.body.style.overflow = 'hidden';
}

function closeCart() {
    document.getElementById('cart-modal').classList.add('hidden');
    document.body.style.overflow = 'auto';
}

function showCartNotification() {
    const notification = document.createElement('div');
    notification.className = 'fixed bottom-4 right-4 bg-green-500 text-white px-4 py-2 rounded-lg shadow-lg flex items-center';
    notification.innerHTML = `<i data-feather="check-circle" class="mr-2"></i> Produto adicionado ao carrinho!`;
    document.body.appendChild(notification);
    feather.replace();
    setTimeout(() => {
        notification.classList.add('opacity-0', 'transition-opacity', 'duration-300');
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

function showCheckout() {
    closeCart();
    ['nav', 'footer'].forEach(tag => document.querySelector(tag).classList.add('hidden'));
    document.querySelectorAll('section').forEach(section => section.classList.add('hidden'));
    document.getElementById('checkout').classList.remove('hidden');
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

function returnToHome() {
    document.getElementById('order-confirmation').classList.add('hidden');
    ['nav', 'footer'].forEach(tag => document.querySelector(tag).classList.remove('hidden'));
    ['home', 'products', 'about'].forEach(id => document.getElementById(id).classList.remove('hidden'));
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

async function confirmOrder(e) {
    e.preventDefault();
    // (Restante da função confirmOrder, sem alterações)
    const form = e.target;
    const submitButton = form.querySelector('#confirm-order-btn');
    const formData = new FormData(form);
    const orderData = Object.fromEntries(formData.entries());

    if (!orderData.name || !orderData.email || !orderData.address) {
        showErrorNotification('Por favor, preencha todos os campos obrigatórios.');
        return;
    }

    const originalButtonText = submitButton.innerHTML;
    submitButton.disabled = true;
    submitButton.innerHTML = `<span class="spinner-border" role="status" aria-hidden="true"></span> Processando...`;

    try {
        const response = await fetch(`/api/checkout/${userId}/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json', 'X-CSRFToken': getCookie('csrftoken') },
            body: JSON.stringify(orderData)
        });
        const data = await response.json();
        if (!response.ok || !data.success) throw new Error(data.error || 'Não foi possível completar o pedido.');
        
        document.getElementById('checkout').classList.add('hidden');
        const confirmationSection = document.getElementById('order-confirmation');
        confirmationSection.querySelector('#confirmation-message').innerHTML = `Obrigado por sua compra, <strong>${orderData.name}</strong>! <br> Seu pedido <strong>#${data.order_number}</strong> foi recebido.`;
        confirmationSection.classList.remove('hidden');
        
        cart = [];
        updateCart();
        form.reset();
        window.scrollTo({ top: 0, behavior: 'smooth' });
    } catch (error) {
        console.error('Erro durante o checkout:', error);
        showErrorNotification(error.message || 'Ocorreu um erro. Tente novamente.');
    } finally {
        submitButton.disabled = false;
        submitButton.innerHTML = originalButtonText;
    }
}

function showErrorNotification(message) {
    const notification = document.createElement('div');
    notification.className = 'fixed bottom-4 right-4 bg-red-500 text-white px-4 py-2 rounded-lg shadow-lg flex items-center';
    notification.innerHTML = `<i data-feather="x-circle" class="mr-2"></i><span>${message}</span>`;
    document.body.appendChild(notification);
    feather.replace();
    setTimeout(() => {
        notification.classList.add('opacity-0', 'transition-opacity', 'duration-300');
        setTimeout(() => notification.remove(), 300);
    }, 4000);
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}