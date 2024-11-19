document.addEventListener('DOMContentLoaded', () => {
    const inventoryList = document.getElementById('inventory-list');
    const inventoryForm = document.getElementById('inventory-form');
    const inventoryFormElement = document.getElementById('inventory-form-element');
    const addInventoryBtn = document.getElementById('add-inventory-btn');
    const cancelBtn = document.getElementById('cancel-btn');

    function fetchInventory() {
        fetch('/api/inventory')
            .then(response => response.json())
            .then(items => {
                inventoryList.innerHTML = '';
                items.forEach(item => {
                    const itemElement = createInventoryItemElement(item);
                    inventoryList.appendChild(itemElement);
                });
            });
    }

    function createInventoryItemElement(item) {
        const element = document.createElement('div');
        element.className = 'inventory-item';
        element.innerHTML = `
            <p>Pet ID: ${item.pet_id}</p>
            <p>Quantity: ${item.quantity}</p>
            <p>Is Premade: ${item.is_premade ? 'Yes' : 'No'}</p>
            <button class="edit-btn" data-id="${item.id}">Edit</button>
            <button class="delete-btn" data-id="${item.id}">Delete</button>
        `;
        return element;
    }

    function showInventoryForm(item = null) {
        const formTitle = inventoryForm.querySelector('h2');
        formTitle.textContent = item ? 'Edit Inventory Item' : 'Add Inventory Item';
        inventoryFormElement.reset();

        if (item) {
            document.getElementById('item-id').value = item.id;
            document.getElementById('pet-id').value = item.pet_id;
            document.getElementById('quantity').value = item.quantity;
            document.getElementById('is-premade').checked = item.is_premade;
        } else {
            document.getElementById('item-id').value = '';
        }

        inventoryForm.classList.remove('hidden');
    }

    addInventoryBtn.addEventListener('click', () => {
        showInventoryForm();
    });

    cancelBtn.addEventListener('click', () => {
        inventoryForm.classList.add('hidden');
    });

    inventoryList.addEventListener('click', (e) => {
        if (e.target.classList.contains('edit-btn')) {
            const itemId = e.target.getAttribute('data-id');
            fetch(`/api/inventory/${itemId}`)
                .then(response => response.json())
                .then(item => showInventoryForm(item));
        } else if (e.target.classList.contains('delete-btn')) {
            const itemId = e.target.getAttribute('data-id');
            if (confirm('Are you sure you want to delete this inventory item?')) {
                fetch(`/api/inventory/${itemId}`, { method: 'DELETE' })
                    .then(() => fetchInventory());
            }
        }
    });

    inventoryFormElement.addEventListener('submit', (e) => {
        e.preventDefault();
        const itemId = document.getElementById('item-id').value;
        const formData = new FormData(inventoryFormElement);
        const data = Object.fromEntries(formData.entries());
        data.is_premade = data.is_premade === 'on';

        const method = itemId ? 'PUT' : 'POST';
        const url = itemId ? `/api/inventory/${itemId}` : '/api/inventory';

        fetch(url, {
            method: method,
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
        })
        .then(response => response.json())
        .then(() => {
            fetchInventory();
            inventoryForm.classList.add('hidden');
        });
    });

    fetchInventory();
});
