document.addEventListener('DOMContentLoaded', () => {
    const petList = document.getElementById('pet-list');
    const searchInput = document.getElementById('search');
    const searchBtn = document.getElementById('search-btn');
    const addPetBtn = document.getElementById('add-pet-btn');
    const petForm = document.getElementById('pet-form');
    const petFormElement = document.getElementById('pet-form-element');
    const cancelBtn = document.getElementById('cancel-btn');
    const uploadImageBtn = document.getElementById('upload-image-btn');
    const petImageInput = document.getElementById('pet-image');

    function fetchPets(search = '') {
        fetch(`/api/pets?search=${search}`)
            .then(response => response.json())
            .then(pets => {
                petList.innerHTML = '';
                pets.forEach(pet => {
                    const petCard = createPetCard(pet);
                    petList.appendChild(petCard);
                });
            });
    }

    function createPetCard(pet) {
        const card = document.createElement('div');
        card.className = 'pet-card';
        card.innerHTML = `
            <img src="${pet.image_url || '/static/images/DC,WB.jpg'}" alt="${pet.hero_name}" class="pet-image">
            <h3>${pet.hero_name}</h3>
            <p>Real Name: ${pet.name}</p>
            <p>Species: ${pet.species}</p>
            <p>Breed: ${pet.breed || 'N/A'}</p>
            <p>Age: ${pet.age || 'N/A'}</p>
            <p>Gender: ${pet.gender || 'N/A'}</p>
            <p>Color: ${pet.color || 'N/A'}</p>
            <p>Superpower: ${pet.superpower}</p>
            <p>Hero Type: ${pet.hero_type}</p>
            <p>Hero Appearance: ${pet.hero_appearance || 'N/A'}</p>
            <button class="edit-btn" data-id="${pet.id}">Edit</button>
            <button class="delete-btn" data-id="${pet.id}">Delete</button>
            <button class="inventory-btn" data-id="${pet.id}">Manage Inventory</button>
        `;
        return card;
    }

    function showPetForm(pet = null) {
        const formTitle = petForm.querySelector('h2');
        formTitle.textContent = pet ? 'Edit Super Pet' : 'Add Super Pet';
        petFormElement.reset();

        if (pet) {
            document.getElementById('pet-id').value = pet.id;
            document.getElementById('name').value = pet.name;
            document.getElementById('hero_name').value = pet.hero_name;
            document.getElementById('species').value = pet.species;
            document.getElementById('breed').value = pet.breed || '';
            document.getElementById('age').value = pet.age || '';
            document.getElementById('gender').value = pet.gender || '';
            document.getElementById('color').value = pet.color || '';
            document.getElementById('superpower').value = pet.superpower;
            document.getElementById('hero_type').value = pet.hero_type;
            document.getElementById('hero_appearance').value = pet.hero_appearance || '';
        } else {
            document.getElementById('pet-id').value = '';
        }

        petForm.classList.remove('hidden');
    }

    searchBtn.addEventListener('click', () => {
        fetchPets(searchInput.value);
    });

    addPetBtn.addEventListener('click', () => {
        showPetForm();
    });

    cancelBtn.addEventListener('click', () => {
        petForm.classList.add('hidden');
    });

    uploadImageBtn.addEventListener('click', () => {
        petImageInput.click();
    });

    petImageInput.addEventListener('change', (e) => {
        if (e.target.files.length > 0) {
            uploadImageBtn.textContent = 'Image Selected';
        } else {
            uploadImageBtn.textContent = 'Upload Image';
        }
    });

    petList.addEventListener('click', (e) => {
        if (e.target.classList.contains('edit-btn')) {
            const petId = e.target.getAttribute('data-id');
            fetch(`/api/pets/${petId}`)
                .then(response => response.json())
                .then(pet => showPetForm(pet));
        } else if (e.target.classList.contains('delete-btn')) {
            const petId = e.target.getAttribute('data-id');
            if (confirm('Are you sure you want to delete this super pet?')) {
                fetch(`/api/pets/${petId}`, { method: 'DELETE' })
                    .then(() => fetchPets());
            }
        } else if (e.target.classList.contains('inventory-btn')) {
            const petId = e.target.getAttribute('data-id');
            showInventoryManagement(petId);
        }
    });

    petFormElement.addEventListener('submit', (e) => {
        e.preventDefault();
        const petId = document.getElementById('pet-id').value;
        const formData = new FormData(petFormElement);

        const method = petId ? 'PUT' : 'POST';
        const url = petId ? `/api/pets/${petId}` : '/api/pets';

        fetch(url, {
            method: method,
            body: formData
        })
        .then(response => response.json())
        .then(() => {
            fetchPets();
            petForm.classList.add('hidden');
        });
    });

    function showInventoryManagement(petId) {
        // Implement inventory management UI for the specific pet
        // This could be a modal or a separate page
        console.log(`Manage inventory for pet ${petId}`);
        // You can implement the inventory management UI here
        // For example, you could show a modal with inventory information
        // and allow the user to add/edit/delete inventory items for this pet
    }

    fetchPets();
});
