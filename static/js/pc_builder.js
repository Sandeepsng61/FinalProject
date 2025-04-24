document.addEventListener('DOMContentLoaded', function() {
    // DOM elements
    const componentCards = document.querySelectorAll('.component-card');
    const componentSearchInputs = document.querySelectorAll('.component-search');
    const selectComponentButtons = document.querySelectorAll('.select-component');
    const resetBuilderButton = document.getElementById('reset-builder');
    const addAllToCartButton = document.getElementById('add-all-to-cart');
    const selectedComponentsList = document.getElementById('selected-components-list');
    const noComponentsSelected = document.getElementById('no-components-selected');
    const componentsSummary = document.getElementById('components-summary');
    const estimatedWattage = document.getElementById('estimated-wattage');
    const totalPrice = document.getElementById('total-price');
    const compatibilityWarning = document.getElementById('compatibility-warning');
    const compatibilityMessage = document.getElementById('compatibility-message');
    const addToCartModal = new bootstrap.Modal(document.getElementById('add-to-cart-modal'));
    const confirmAddToCart = document.getElementById('confirm-add-to-cart');
    
    // Store selected components
    let selectedComponents = {};
    let totalPriceValue = 0;
    
    // Format currency
    const formatter = new Intl.NumberFormat('en-IN', {
        style: 'currency',
        currency: 'INR',
        minimumFractionDigits: 2
    });
    
    // Initialize PC builder
    function initPCBuilder() {
        // Component search functionality
        componentSearchInputs.forEach(input => {
            input.addEventListener('input', filterComponents);
        });
        
        // Component selection
        selectComponentButtons.forEach(button => {
            button.addEventListener('click', selectComponent);
        });
        
        // Reset builder
        if (resetBuilderButton) {
            resetBuilderButton.addEventListener('click', resetBuilder);
        }
        
        // Add all to cart
        if (addAllToCartButton) {
            addAllToCartButton.addEventListener('click', showAddToCartModal);
        }
        
        // Confirm add to cart
        if (confirmAddToCart) {
            confirmAddToCart.addEventListener('click', addAllToCart);
        }
    }
    
    // Filter components based on search input
    function filterComponents() {
        const category = this.dataset.category;
        const searchValue = this.value.toLowerCase();
        const componentOptions = document.querySelectorAll(`#${category}-components .component-option`);
        const noComponentsMessage = this.closest('.collapse').querySelector('.no-components-message');
        
        let visibleCount = 0;
        
        componentOptions.forEach(option => {
            const componentTitle = option.querySelector('.card-title').textContent.toLowerCase();
            const visible = componentTitle.includes(searchValue);
            
            option.style.display = visible ? '' : 'none';
            if (visible) visibleCount++;
        });
        
        // Show/hide no components message
        if (visibleCount === 0) {
            noComponentsMessage.classList.remove('d-none');
        } else {
            noComponentsMessage.classList.add('d-none');
        }
    }
    
    // Select a component
    function selectComponent(e) {
        e.preventDefault();
        
        const category = this.dataset.category;
        const componentId = this.dataset.id;
        const componentName = this.dataset.name;
        const componentPrice = parseFloat(this.dataset.price);
        
        // Update selected components object
        selectedComponents[category] = {
            id: componentId,
            name: componentName,
            price: componentPrice
        };
        
        // Update UI
        document.getElementById(`${category}-name`).textContent = componentName;
        
        // Update summary UI
        updateSummary();
        
        // Check compatibility
        checkCompatibility();
        
        // Close the component options panel
        const collapse = bootstrap.Collapse.getInstance(document.getElementById(`${category}-options`));
        if (collapse) {
            collapse.hide();
        }
    }
    
    // Update build summary
    function updateSummary() {
        // Calculate total price
        totalPriceValue = 0;
        let hasComponents = false;
        
        // Clear existing items
        selectedComponentsList.innerHTML = '';
        
        // Add selected components to list
        for (const category in selectedComponents) {
            if (selectedComponents[category]) {
                hasComponents = true;
                totalPriceValue += selectedComponents[category].price;
                
                // Create list item
                const listItem = document.createElement('li');
                listItem.className = 'list-group-item d-flex justify-content-between align-items-center';
                
                const categorySpan = document.createElement('span');
                categorySpan.className = 'text-capitalize';
                categorySpan.textContent = category;
                
                const infoDiv = document.createElement('div');
                infoDiv.className = 'd-flex flex-column align-items-end';
                
                const nameSpan = document.createElement('span');
                nameSpan.textContent = selectedComponents[category].name;
                
                const priceSpan = document.createElement('small');
                priceSpan.className = 'text-muted';
                priceSpan.textContent = formatter.format(selectedComponents[category].price);
                
                infoDiv.appendChild(nameSpan);
                infoDiv.appendChild(priceSpan);
                
                listItem.appendChild(categorySpan);
                listItem.appendChild(infoDiv);
                
                selectedComponentsList.appendChild(listItem);
            }
        }
        
        // Update total price
        totalPrice.textContent = formatter.format(totalPriceValue);
        
        // Show/hide empty state
        if (hasComponents) {
            noComponentsSelected.classList.add('d-none');
            componentsSummary.classList.remove('d-none');
        } else {
            noComponentsSelected.classList.remove('d-none');
            componentsSummary.classList.add('d-none');
        }
        
        // Enable/disable add to cart button
        if (addAllToCartButton) {
            addAllToCartButton.disabled = !hasComponents;
        }
    }
    
    // Check component compatibility
    function checkCompatibility() {
        // Only check if we have at least 2 components
        if (Object.keys(selectedComponents).length < 2) {
            compatibilityWarning.classList.add('d-none');
            return;
        }
        
        // Get component IDs
        const componentIds = {};
        for (const category in selectedComponents) {
            if (selectedComponents[category]) {
                componentIds[category] = selectedComponents[category].id;
            }
        }
        
        // Make API call to check compatibility
        fetch('/api/check-compatibility', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(componentIds)
        })
        .then(response => response.json())
        .then(data => {
            // Update UI based on compatibility
            if (!data.compatible) {
                compatibilityWarning.classList.remove('d-none');
                compatibilityMessage.textContent = data.issues.join(' ');
            } else {
                compatibilityWarning.classList.add('d-none');
            }
            
            // Update estimated wattage
            if (data.estimated_wattage) {
                estimatedWattage.textContent = `${data.estimated_wattage}W`;
            }
        })
        .catch(error => {
            console.error('Error checking compatibility:', error);
        });
    }
    
    // Reset PC builder
    function resetBuilder() {
        if (confirm('Are you sure you want to reset your build? All selected components will be cleared.')) {
            // Clear selected components
            selectedComponents = {};
            
            // Reset UI
            document.querySelectorAll('.component-name').forEach(el => {
                el.textContent = 'No component selected';
            });
            
            // Reset summary
            updateSummary();
            
            // Hide compatibility warning
            compatibilityWarning.classList.add('d-none');
            
            // Reset estimated wattage
            estimatedWattage.textContent = '0W';
        }
    }
    
    // Show add to cart modal
    function showAddToCartModal() {
        addToCartModal.show();
    }
    
    // Add all components to cart
    function addAllToCart() {
        // Create form to send selected components
        const form = document.createElement('form');
        form.method = 'POST';
        form.action = '/add-all-to-cart';
        
        // Add selected component IDs to form
        for (const category in selectedComponents) {
            if (selectedComponents[category]) {
                const input = document.createElement('input');
                input.type = 'hidden';
                input.name = `components[${category}]`;
                input.value = selectedComponents[category].id;
                form.appendChild(input);
            }
        }
        
        // Add form to document and submit
        document.body.appendChild(form);
        form.submit();
    }
    
    // Initialize
    initPCBuilder();
});
