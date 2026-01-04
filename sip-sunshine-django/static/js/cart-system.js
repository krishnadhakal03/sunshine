/**
 * Shopping Cart System
 * Handles client-side cart management with localStorage backup
 */

const CART_STORAGE_KEY = 'sip_sunshine_cart';
const CART_API_URL = '/api/cart/';

class ShoppingCart {
    constructor() {
        this.items = this.loadFromStorage();
        this.init();
    }

    /**
     * Initialize cart system
     */
    init() {
        this.syncWithServer();
        this.updateCartUI();
        this.setupEventListeners();
    }

    /**
     * Load cart from localStorage
     */
    loadFromStorage() {
        try {
            const stored = localStorage.getItem(CART_STORAGE_KEY);
            return stored ? JSON.parse(stored) : [];
        } catch (error) {
            console.error('Error loading cart from storage:', error);
            return [];
        }
    }

    /**
     * Save cart to localStorage
     */
    saveToStorage() {
        try {
            localStorage.setItem(CART_STORAGE_KEY, JSON.stringify(this.items));
        } catch (error) {
            console.error('Error saving cart to storage:', error);
        }
    }

    /**
     * Add item to cart
     * @param {Object} itemData - Item data {id, name, price, description, image, category}
     * @param {Number} quantity - Quantity to add (default 1)
     */
    addToCart(itemData, quantity = 1) {
        if (!itemData.id || !itemData.name || !itemData.price) {
            console.error('Invalid item data:', itemData);
            return false;
        }

        // Check if item already exists
        const existingItem = this.items.find(item => item.id === itemData.id);
        
        if (existingItem) {
            // Update quantity
            existingItem.quantity = (existingItem.quantity || 1) + quantity;
        } else {
            // Add new item
            this.items.push({
                id: itemData.id,
                name: itemData.name,
                price: parseFloat(itemData.price),
                description: itemData.description || '',
                image: itemData.image || '',
                category: itemData.category || '',
                quantity: quantity,
                special_instructions: ''
            });
        }

        this.saveToStorage();
        this.updateCartUI();
        this.showNotification(`${itemData.name} added to cart!`);
        return true;
    }

    /**
     * Remove item from cart
     * @param {String} itemId - Item ID to remove
     */
    removeFromCart(itemId) {
        this.items = this.items.filter(item => item.id !== itemId);
        this.saveToStorage();
        this.updateCartUI();
        this.showNotification('Item removed from cart');
    }

    /**
     * Update item quantity
     * @param {String} itemId - Item ID
     * @param {Number} quantity - New quantity
     */
    updateQuantity(itemId, quantity) {
        const item = this.items.find(item => item.id === itemId);
        
        if (item) {
            if (quantity <= 0) {
                this.removeFromCart(itemId);
            } else {
                item.quantity = parseInt(quantity);
                this.saveToStorage();
                this.updateCartUI();
            }
        }
    }

    /**
     * Update special instructions for item
     * @param {String} itemId - Item ID
     * @param {String} instructions - Special instructions
     */
    updateSpecialInstructions(itemId, instructions) {
        const item = this.items.find(item => item.id === itemId);
        if (item) {
            item.special_instructions = instructions;
            this.saveToStorage();
        }
    }

    /**
     * Get cart total
     * @returns {Number} Total price
     */
    getTotal() {
        return this.items.reduce((total, item) => {
            return total + (item.price * item.quantity);
        }, 0).toFixed(2);
    }

    /**
     * Get item count
     * @returns {Number} Total items count
     */
    getItemCount() {
        return this.items.reduce((count, item) => count + item.quantity, 0);
    }

    /**
     * Clear entire cart
     */
    clearCart() {
        if (confirm('Clear entire cart?')) {
            this.items = [];
            this.saveToStorage();
            this.updateCartUI();
            this.showNotification('Cart cleared');
        }
    }

    /**
     * Get cart items
     * @returns {Array} Cart items
     */
    getItems() {
        return [...this.items];
    }

    /**
     * Update cart UI elements
     */
    updateCartUI() {
        // Update cart badge
        const cartBadge = document.getElementById('cartItemCount');
        if (cartBadge) {
            const count = this.getItemCount();
            cartBadge.textContent = count;
            cartBadge.style.display = count > 0 ? 'flex' : 'none';
        }

        // Update cart modal if open
        this.displayCartModal();
    }

    /**
     * Display cart in modal
     */
    displayCartModal() {
        const cartItemsContainer = document.getElementById('cartItems');
        if (!cartItemsContainer) return;

        if (this.items.length === 0) {
            cartItemsContainer.innerHTML = `
                <div style="text-align: center; padding: 40px; color: #999;">
                    <p style="font-size: 48px; margin-bottom: 20px;">🛒</p>
                    <p style="font-size: 18px;">Your cart is empty</p>
                    <p style="font-size: 14px;">Add items from the menu to get started</p>
                </div>
            `;
            return;
        }

        let html = '<div class="cart-items-list">';
        
        this.items.forEach(item => {
            const subtotal = (item.price * item.quantity).toFixed(2);
            html += `
                <div class="cart-item" style="display: flex; gap: 15px; padding: 15px; border-bottom: 1px solid #e0e0e0; align-items: flex-start;">
                    ${item.image ? `<img src="${item.image}" alt="${item.name}" style="width: 80px; height: 80px; object-fit: cover; border-radius: 6px;">` : ''}
                    <div style="flex: 1;">
                        <h5 style="margin: 0 0 5px 0; font-weight: 600;">${item.name}</h5>
                        <p style="margin: 0 0 10px 0; font-size: 13px; color: #666;">${item.description}</p>
                        <div style="display: flex; gap: 10px; align-items: center; margin-bottom: 8px;">
                            <button class="qty-btn" onclick="cart.updateQuantity('${item.id}', ${item.quantity - 1})" style="width: 30px; height: 30px; border: 1px solid #e0e0e0; background: white; border-radius: 4px; cursor: pointer;">−</button>
                            <span style="min-width: 30px; text-align: center; font-weight: 600;">${item.quantity}</span>
                            <button class="qty-btn" onclick="cart.updateQuantity('${item.id}', ${item.quantity + 1})" style="width: 30px; height: 30px; border: 1px solid #e0e0e0; background: white; border-radius: 4px; cursor: pointer;">+</button>
                            <span style="flex: 1; text-align: right; color: #f34949; font-weight: 700; font-size: 16px;">€${subtotal}</span>
                        </div>
                        <div style="display: flex; gap: 10px;">
                            <input type="text" placeholder="Special instructions..." value="${item.special_instructions}" onchange="cart.updateSpecialInstructions('${item.id}', this.value)" style="flex: 1; padding: 6px 8px; border: 1px solid #e0e0e0; border-radius: 4px; font-size: 12px;">
                            <button onclick="cart.removeFromCart('${item.id}')" style="background: #dc3545; color: white; border: none; border-radius: 4px; padding: 6px 12px; cursor: pointer; font-size: 12px;">Remove</button>
                        </div>
                    </div>
                </div>
            `;
        });

        html += '</div>';
        cartItemsContainer.innerHTML = html;

        // Update cart summary
        this.updateCartSummary();
    }

    /**
     * Update cart summary (total, tax, etc.)
     */
    updateCartSummary() {
        const subtotal = parseFloat(this.getTotal());
        const tax = (subtotal * 0.21).toFixed(2);
        const total = (subtotal + parseFloat(tax)).toFixed(2);

        const summaryElement = document.getElementById('cartSummary');
        if (summaryElement) {
            summaryElement.innerHTML = `
                <div style="background: #f8f9fa; padding: 15px; border-radius: 8px; border: 1px solid #e0e0e0;">
                    <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
                        <span style="color: #666;">Subtotal:</span>
                        <span style="font-weight: 600;">€${subtotal.toFixed(2)}</span>
                    </div>
                    <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
                        <span style="color: #666;">Tax (21%):</span>
                        <span style="font-weight: 600;">€${tax}</span>
                    </div>
                    <div style="border-top: 1px solid #dee2e6; padding-top: 8px; display: flex; justify-content: space-between;">
                        <span style="font-weight: 700; font-size: 16px;">Total:</span>
                        <span style="color: #f34949; font-weight: 700; font-size: 18px;">€${total}</span>
                    </div>
                </div>
            `;
        }
    }

    /**
     * Setup event listeners
     */
    setupEventListeners() {
        // Cart icon click
        const cartIcon = document.getElementById('cartIcon');
        if (cartIcon) {
            cartIcon.addEventListener('click', () => this.openCartModal());
        }

        // Menu item add to cart buttons
        document.addEventListener('click', (e) => {
            const trigger = e.target.closest('[data-add-to-cart]');
            if (!trigger) return;

            const itemId = trigger.getAttribute('data-item-id');
            const itemName = trigger.getAttribute('data-item-name');
            const itemPrice = trigger.getAttribute('data-item-price');
            const itemDesc = trigger.getAttribute('data-item-desc') || '';
            const itemImage = trigger.getAttribute('data-item-image') || '';
            const itemCategory = trigger.getAttribute('data-item-category') || '';

            const ok = this.addToCart({
                id: itemId,
                name: itemName,
                price: itemPrice,
                description: itemDesc,
                image: itemImage,
                category: itemCategory
            });

            if (ok && trigger.hasAttribute('data-open-cart')) {
                this.openCartModal();
            }
        });
    }

    /**
     * Open cart modal
     */
    openCartModal() {
        const cartModal = document.getElementById('cartModal');
        if (cartModal) {
            cartModal.classList.add('show');
            cartModal.style.display = 'block';
            cartModal.setAttribute('aria-hidden', 'false');
            document.body.classList.add('modal-open');
            document.body.style.overflow = 'hidden';

            // Add a backdrop (Bootstrap-like) for better UX
            if (!document.getElementById('cartModalBackdrop')) {
                const backdrop = document.createElement('div');
                backdrop.className = 'modal-backdrop show';
                backdrop.id = 'cartModalBackdrop';
                backdrop.addEventListener('click', () => this.closeCartModal());
                document.body.appendChild(backdrop);
            }
        }
    }

    /**
     * Close cart modal
     */
    closeCartModal() {
        const cartModal = document.getElementById('cartModal');
        if (cartModal) {
            cartModal.classList.remove('show');
            cartModal.style.display = 'none';
            cartModal.setAttribute('aria-hidden', 'true');
            document.body.classList.remove('modal-open');
            document.body.style.overflow = '';

            const backdrop = document.getElementById('cartModalBackdrop');
            if (backdrop) backdrop.remove();
        }
    }

    /**
     * Proceed to checkout
     */
    proceedToCheckout() {
        if (this.items.length === 0) {
            this.showNotification('Cart is empty', 'error');
            return;
        }
        
        // Store cart data in sessionStorage for checkout
        sessionStorage.setItem('checkout_cart', JSON.stringify(this.items));
        sessionStorage.setItem('checkout_subtotal', this.getTotal());
        
        // Redirect to checkout
        window.location.href = '/checkout/';
    }

    /**
     * Sync cart with server
     */
    syncWithServer() {
        // This can be used to backup cart to database for logged-in users
        // Implement when needed
    }

    /**
     * Show notification
     * @param {String} message - Message to show
     * @param {String} type - Notification type (success, error, info)
     */
    showNotification(message, type = 'success') {
        const notification = document.createElement('div');
        notification.style.cssText = `
            position: fixed;
            bottom: 20px;
            right: 20px;
            background: ${type === 'error' ? '#dc3545' : '#28a745'};
            color: white;
            padding: 15px 20px;
            border-radius: 6px;
            z-index: 10000;
            animation: slideIn 0.3s ease;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        `;
        notification.textContent = message;
        document.body.appendChild(notification);

        setTimeout(() => {
            notification.style.animation = 'slideOut 0.3s ease';
            setTimeout(() => notification.remove(), 300);
        }, 3000);
    }
}

// Global cart instance
let cart;

// Initialize cart when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    cart = new ShoppingCart();
});

// Add CSS animations
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from {
            transform: translateX(400px);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }

    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(400px);
            opacity: 0;
        }
    }

    .qty-btn:hover {
        background: #f8f9fa !important;
    }

    .cart-item:hover {
        background: #f8f9fa;
    }
`;
document.head.appendChild(style);
