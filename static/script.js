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
            return `<div class="admin-catalog-card" data-name=${item.name}>
            <p>${item.name}</p>
            <p>${item.category}</p>
            <p>${item.price}</p>
            <p>${item.description}</p>
            <img src="${item.image}" alt="${item.name}">
            </div>`
        }).join('');
    }


    async function addItem() {
        const  data = {
            name: addItemForm.name.value,
            image: addItemForm.image.value,
            category: addItemForm.category.value,
            price: addItemForm.price.value,
            description: addItemForm.description.value
        }

        const response = await fetch("/api/add_admin_catalog", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data)
        });

        const result = await response.json();
        if (response.ok) {
            notificationBar.textContent = result.success;
        }
    }

    if (addItemForm) {
        addItemForm.addEventListener("submit", async (event) => {
            event.preventDefault();
            await addItem();
        });
    }


    if (adminCatalog) {
        renderAdminCatalog();
        return;
    }

});