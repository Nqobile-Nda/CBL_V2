document.addEventListener('DOMContentLoaded', async () => {
    const notificationBar = document.querySelector(".notification-bar");
    const addItemForm = document.getElementById("add-item-form");
    const adminCatalog = document.getElementById("admin-catalog");
    const editItemForm = document.getElementById("edit-item-form");
    
    async function loadCatalog() {
        const response = await fetch("/api/catalog");
        return await response.json();
    }
    
    async function renderAdminCatalog() {
        const catalog = await loadCatalog();
        adminCatalog.innerHTML = catalog.map(item => {
            return `<div class="admin-catalog-card" data-item-id="${item.item_id}">
                <p>${item.name}</p>
                <p>${item.category}</p>
                <p>${item.price}</p>
                <p>${item.description}</p>
                <img src="${item.image}" alt="${item.name}">
                <button class="edit-btn" type="button" data-item-id="${item.item_id}">Edit</button>
            </div>`;
        }).join('');
        attachEditListeners();
    }
    
    function attachEditListeners() {
        const editButtons = adminCatalog.querySelectorAll('.edit-btn');
        editButtons.forEach(button => {
            button.addEventListener('click', (event) => {
                const itemId = event.target.getAttribute('data-item-id');
                window.location.href = `/edit_admin_catalog/${itemId}`;
            });
        });
    }
    
    async function handleAddItem(event) {
        event.preventDefault();
        const formData = new FormData();
        formData.append('name', addItemForm.name.value);
        formData.append('category', addItemForm.category.value);
        formData.append('price', addItemForm.price.value);
        formData.append('description', addItemForm.description.value);
        
        const fileInput = addItemForm.image;
        if (fileInput && fileInput.files && fileInput.files[0]) {
            formData.append('image', fileInput.files[0]);
        }
        
        const response = await fetch("/api/add_admin_catalog", { method: "POST", body: formData });
        const result = await response.json();
        if (response.ok) {
            notificationBar.textContent = result.success;
            addItemForm.reset();
        } else {
            notificationBar.textContent = result.error || 'Failed to add item';
        }
    }
    
    // Python ? JS: Fetch item for edit
    async function loadEditItem(itemId) {
        const response = await fetch(`/api/edit_admin_catalog/${itemId}`);
        if (!response.ok) {
            notificationBar.textContent = 'Item not found';
            return null;
        }
        return await response.json();
    }
    
    // JS ? HTML: Populate edit form
    async function populateEditForm() {
        const itemId = window.location.pathname.split('/').pop();
        const item = await loadEditItem(itemId);
        if (item) {
            document.getElementById("edit-id").value = item.item_id;
            document.getElementById("edit-name").value = item.name;
            document.getElementById("edit-category").value = item.category;
            document.getElementById("edit-price").value = item.price;
            document.getElementById("edit-description").value = item.description;
        }
    }
    
    async function handleEditItem(event) {
        event.preventDefault();
        const itemId = document.getElementById("edit-id").value;
        const formData = new FormData();
        formData.append('name', document.getElementById("edit-name").value);
        formData.append('category', document.getElementById("edit-category").value);
        formData.append('price', document.getElementById("edit-price").value);
        formData.append('description', document.getElementById("edit-description").value);
        
        const fileInput = document.getElementById("edit-image");
        if (fileInput && fileInput.files && fileInput.files[0]) {
            formData.append('image', fileInput.files[0]);
        }
        
        const response = await fetch(`/api/edit_admin_catalog/${itemId}`, { method: "POST", body: formData });
        const result = await response.json();
        if (response.ok) {
            notificationBar.textContent = result.success;
        } else {
            notificationBar.textContent = result.error || 'Failed to update item';
        }
    }
    
    if (addItemForm) {
        addItemForm.addEventListener("submit", handleAddItem);
    }
    if (adminCatalog) {
        renderAdminCatalog();
    }
    if (editItemForm) {
        populateEditForm();
        editItemForm.addEventListener("submit", handleEditItem);
    }
});
