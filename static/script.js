document.addEventListener('DOMContentLoaded', async () => {

    const notificationBar = document.querySelector(".notification-bar");

    const addItemForm = document.getElementById("add-item-form");
    const addItemFormButton = document.getElementById("add-item-form-button");

    async function loadCatalog() {
        const response = await fetch("/api/catalog");
        const catalog = await response.json()
        return catalog;
    }

    const adminCatalog = document.getElementById("admin-catalog");

    async function renderAdminCatalog() {
        const catalog = await loadCatalog();

        adminCatalog.innerHTML = catalog.map(item => {
            return `<div class="admin-catalog-card">
            <p>${item.name}</p>
            <p>${item.category}</p>
            <p>${item.price}</p>
            <p>${item.description}</p>
            <img src="${item.image}" alt="${item.name}">
            <button type="button">Edit</button>
            </div>`
        }).join('');
    }


    async function addItem() {
        const formData = new FormData();
        formData.append('name', addItemForm.name.value);
        formData.append('category', addItemForm.category.value);
        formData.append('price', addItemForm.price.value);
        formData.append('description', addItemForm.description.value);

        const fileInput = addItemForm.image;
        if (fileInput && fileInput.files && fileInput.files[0]) {
            formData.append('image', fileInput.files[0]);
        }

        const response = await fetch("/api/add_admin_catalog", {
            method: "POST",
            body: formData
        });

        const result = await response.json();
        if (response.ok) {
            notificationBar.textContent = result.success;
        } else {
            notificationBar.textContent = result.error || 'Failed to add item';
        }
    }

    const editItemForm = document.getElementById("edit-item-form");

    if (adminCatalog) {
    renderAdminCatalog();
    return;
    }

    if (addItemForm) {
        addItemForm.addEventListener("submit", async (event) => {
            event.preventDefault();
            await addItem();
        });
    }
});