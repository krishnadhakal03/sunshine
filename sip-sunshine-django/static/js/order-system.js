// Order Management JavaScript

document.addEventListener('DOMContentLoaded', function() {
    initializeOrderSystem();
});

function initializeOrderSystem() {
    // Order Type Toggle
    const orderTypeRadios = document.querySelectorAll('input[name="order_type"]');
    orderTypeRadios.forEach(radio => {
        radio.addEventListener('change', handleOrderTypeChange);
    });

    // Quantity Buttons
    const qtyMinusBtn = document.querySelector('.qty-btn-minus');
    const qtyPlusBtn = document.querySelector('.qty-btn-plus');
    const qtyInput = document.getElementById('quantity');

    if (qtyMinusBtn) qtyMinusBtn.addEventListener('click', decreaseQuantity);
    if (qtyPlusBtn) qtyPlusBtn.addEventListener('click', increaseQuantity);
    if (qtyInput) qtyInput.addEventListener('change', updateOrderSummary);

    // Create Order Button
    const createOrderBtn = document.getElementById('createOrderBtn');
    if (createOrderBtn) {
        createOrderBtn.addEventListener('click', handleCreateOrder);
    }

    // Modal shown event
    const orderModal = document.getElementById('orderModal');
    if (orderModal) {
        orderModal.addEventListener('show.bs.modal', function() {
            // Reset form when modal opens
            resetOrderForm();
        });
    }
}

/**
 * Handle order type change (Seated vs Online)
 */
function handleOrderTypeChange(e) {
    const orderType = e.target.value;
    const seatedFields = document.getElementById('seatedFields');
    const pickupFields = document.getElementById('pickupFields');
    const deliveryFields = document.getElementById('deliveryFields');
    const orderTypeInput = document.getElementById('orderTypeInput');

    // Update hidden input
    orderTypeInput.value = orderType;

    // Hide all fields first
    seatedFields.style.display = 'none';
    pickupFields.style.display = 'none';
    deliveryFields.style.display = 'none';

    // Show only the relevant fields
    if (orderType === 'seated') {
        seatedFields.style.display = 'flex';
        // Clear other fields
        document.getElementById('tableNumber').value = '';
    } else if (orderType === 'pickup') {
        pickupFields.style.display = 'flex';
    } else if (orderType === 'delivery') {
        deliveryFields.style.display = 'flex';
        // Clear seated field
        document.getElementById('tableNumber').value = '';
    }
}

/**
 * Decrease quantity
 */
function decreaseQuantity(e) {
    e.preventDefault();
    const qtyInput = document.getElementById('quantity');
    let current = parseInt(qtyInput.value) || 1;
    if (current > 1) {
        qtyInput.value = current - 1;
        updateOrderSummary();
    }
}

/**
 * Increase quantity
 */
function increaseQuantity(e) {
    e.preventDefault();
    const qtyInput = document.getElementById('quantity');
    let current = parseInt(qtyInput.value) || 1;
    if (current < 99) {
        qtyInput.value = current + 1;
        updateOrderSummary();
    }
}

/**
 * Update order summary totals
 */
function updateOrderSummary() {
    const itemPrice = parseFloat(document.getElementById('modalItemPrice').textContent) || 0;
    const quantity = parseInt(document.getElementById('quantity').value) || 1;
    const total = (itemPrice * quantity).toFixed(2);

    document.getElementById('summaryUnitPrice').textContent = itemPrice.toFixed(2);
    document.getElementById('summaryQty').textContent = quantity;
    document.getElementById('summaryTotal').textContent = total;
}

/**
 * Populate order modal with item details
 */
function showOrderModal(itemData) {
    // Auto-populate item information
    document.getElementById('itemName').value = itemData.name;
    document.getElementById('itemPrice').value = itemData.price;
    document.getElementById('modalItemName').textContent = itemData.name;
    document.getElementById('modalItemDesc').textContent = itemData.description;
    document.getElementById('modalItemPrice').textContent = itemData.price.toFixed(2);

    // Show image if available
    if (itemData.image) {
        const img = document.getElementById('modalItemImage');
        img.src = itemData.image;
        img.style.display = 'block';
    }

    // Reset form fields
    resetOrderForm();

    // Update summary
    updateOrderSummary();

    // Show modal using Bootstrap
    const modal = new bootstrap.Modal(document.getElementById('orderModal'));
    modal.show();
}

/**
 * Reset order form to defaults
 */
function resetOrderForm() {
    const form = document.getElementById('orderForm');
    if (form) form.reset();

    // Reset to seated type
    document.getElementById('orderSeated').checked = true;
    document.getElementById('orderTypeInput').value = 'seated';

    // Hide all type-specific fields
    document.getElementById('seatedFields').style.display = 'none';
    document.getElementById('pickupFields').style.display = 'none';
    document.getElementById('deliveryFields').style.display = 'none';
    
    // Show only seated fields (default)
    document.getElementById('seatedFields').style.display = 'flex';

    // Reset quantity
    document.getElementById('quantity').value = '1';

    // Clear error
    const errorDiv = document.getElementById('orderError');
    if (errorDiv) {
        errorDiv.style.display = 'none';
        errorDiv.textContent = '';
    }

    updateOrderSummary();
}

/**
 * Validate form based on order type
 */
function validateOrderForm() {
    const errors = [];
    const orderType = document.getElementById('orderTypeInput').value;
    const guestName = document.getElementById('guestName').value.trim();
    const guestPhone = document.getElementById('guestPhone').value.trim();

    // Required fields for all types
    if (!guestName) {
        errors.push('Guest name is required');
    }

    if (!guestPhone) {
        errors.push('Phone number is required');
    }

    if (orderType === 'seated') {
        const tableNumber = document.getElementById('tableNumber').value;
        if (!tableNumber) {
            errors.push('Table number is required for dine-in orders');
        }
    } else if (orderType === 'pickup') {
        // No additional required fields (pickup time can be empty = ASAP)
    } else if (orderType === 'delivery') {
        const email = document.getElementById('guestEmail').value.trim();
        const address = document.getElementById('deliveryAddress').value.trim();
        const city = document.getElementById('deliveryCity').value.trim();
        const postal = document.getElementById('deliveryPostalCode').value.trim();

        if (!address) errors.push('Delivery address is required');
        if (!city) errors.push('City is required');
        if (!postal) errors.push('Postal code is required');

        // Email is optional, but validate if provided
        if (email && !isValidEmail(email)) {
            errors.push('Please enter a valid email address');
        }
    }

    return errors;
}

/**
 * Simple email validation
 */
function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

/**
 * Handle create order submission
 */
function handleCreateOrder(e) {
    e.preventDefault();

    // Get CSRF token
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    // Validate form
    const errors = validateOrderForm();
    const errorDiv = document.getElementById('orderError');

    if (errors.length > 0) {
        errorDiv.style.display = 'block';
        errorDiv.innerHTML = '<strong>Please fix the following errors:</strong><ul>' +
            errors.map(e => `<li>${e}</li>`).join('') +
            '</ul>';
        window.scrollTo(0, errorDiv.offsetTop - 100);
        return;
    }

    errorDiv.style.display = 'none';

    // Prepare JSON data for API
    const orderType = document.getElementById('orderTypeInput').value;

    // Common fields
    let orderData = {
        order_type: orderType,
        guest_name: document.getElementById('guestName').value,
        guest_phone: document.getElementById('guestPhone').value,
        payment_method: 'cash',  // Default to cash
        special_requests: document.getElementById('specialInstructions').value,
        items: [
            {
                id: 1,  // Will be set from menu if available
                name: document.getElementById('itemName').value,
                price: parseFloat(document.getElementById('itemPrice').value),
                quantity: parseInt(document.getElementById('quantity').value)
            }
        ]
    };

    // Order type specific fields
    if (orderType === 'seated') {
        const tableNumber = document.getElementById('tableNumber').value;
        if (tableNumber) {
            orderData.table_number = parseInt(tableNumber);
        }
    } else if (orderType === 'pickup') {
        const pickupTime = document.getElementById('preferredPickupTime').value;
        if (pickupTime) {
            orderData.preferred_pickup_time = pickupTime;
        }
    } else if (orderType === 'delivery') {
        orderData.guest_email = document.getElementById('guestEmail').value || '';
        orderData.delivery_address = document.getElementById('deliveryAddress').value;
        orderData.delivery_city = document.getElementById('deliveryCity').value;
        orderData.delivery_postal_code = document.getElementById('deliveryPostalCode').value;
        orderData.delivery_country = document.getElementById('deliveryCountry').value || '';
    }

    // Submit via AJAX to API
    const createOrderBtn = document.getElementById('createOrderBtn');
    const originalText = createOrderBtn.innerHTML;
    createOrderBtn.disabled = true;
    createOrderBtn.innerHTML = '⏳ Creating...';

    fetch('/api/orders/create/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        },
        body: JSON.stringify(orderData)
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Show confirmation modal
            document.getElementById('confirmOrderId').textContent = data.order_id;
            
            // Hide order modal
            try {
                const orderModal = bootstrap.Modal.getInstance(document.getElementById('orderModal'));
                if (orderModal) {
                    orderModal.hide();
                }
            } catch (e) {
                // Fallback
                const modal = document.getElementById('orderModal');
                if (modal) {
                    modal.classList.remove('show');
                    modal.style.display = 'none';
                }
            }

            // Show confirmation modal
            try {
                const confirmationModal = new bootstrap.Modal(document.getElementById('confirmationModal'));
                confirmationModal.show();
            } catch (e) {
                console.error('Confirmation modal error:', e);
            }

            // Reset form after brief delay
            setTimeout(() => {
                resetOrderForm();
            }, 1000);
        } else {
            throw new Error(data.message || 'Failed to create order');
        }
    })
    .catch(error => {
        errorDiv.style.display = 'block';
        errorDiv.innerHTML = `<strong>Error:</strong> ${error.message}`;
        window.scrollTo(0, errorDiv.offsetTop - 100);
    })
    .finally(() => {
        createOrderBtn.disabled = false;
        createOrderBtn.innerHTML = originalText;
    });
}

/**
 * Close the confirmation modal
 */
function closeConfirmationModal() {
    const confirmationModal = document.getElementById('confirmationModal');
    if (!confirmationModal) return;
    
    try {
        // Try using Bootstrap 5 API if available
        if (typeof bootstrap !== 'undefined' && bootstrap.Modal) {
            try {
                const bsModal = bootstrap.Modal.getInstance(confirmationModal);
                if (bsModal) {
                    bsModal.hide();
                    return;
                }
            } catch (e) {
                // Bootstrap API failed, use fallback
            }
        }
    } catch (e) {
        console.warn('Bootstrap not available, using manual hide');
    }
    
    // Fallback: manually hide the modal
    confirmationModal.classList.remove('show');
    confirmationModal.style.display = 'none';
    confirmationModal.setAttribute('aria-hidden', 'true');
    
    // Remove modal backdrop
    const backdrop = document.querySelector('.modal-backdrop');
    if (backdrop) {
        backdrop.remove();
    }
    
    // Remove body overflow hidden class
    document.body.classList.remove('modal-open');
    document.body.style.overflow = 'auto';
}

/**
 * Close the order modal
 */
function closeOrderModal() {
    const orderModal = document.getElementById('orderModal');
    if (!orderModal) return;
    
    try {
        // Try using Bootstrap 5 API if available
        if (typeof bootstrap !== 'undefined' && bootstrap.Modal) {
            try {
                const bsModal = bootstrap.Modal.getInstance(orderModal);
                if (bsModal) {
                    bsModal.hide();
                    return;
                }
            } catch (e) {
                // Bootstrap API failed, use fallback
            }
        }
    } catch (e) {
        console.warn('Bootstrap not available, using manual hide');
    }
    
    // Fallback: manually hide the modal
    orderModal.classList.remove('show');
    orderModal.style.display = 'none';
    orderModal.setAttribute('aria-hidden', 'true');
    
    // Remove modal backdrop
    const backdrop = document.querySelector('.modal-backdrop');
    if (backdrop) {
        backdrop.remove();
    }
    
    // Remove body overflow hidden class
    document.body.classList.remove('modal-open');
    document.body.style.overflow = 'auto';
    
    // Reset the form
    resetOrderForm();
}

/**
 * Expose functions globally for menu page buttons
 */
window.showOrderModal = showOrderModal;
window.closeConfirmationModal = closeConfirmationModal;
window.closeOrderModal = closeOrderModal;
