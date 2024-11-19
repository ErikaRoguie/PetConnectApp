document.addEventListener('DOMContentLoaded', () => {
    const petList = document.getElementById('pet-list');
    const searchInput = document.getElementById('search');
    const searchBtn = document.getElementById('search-btn');
    const addPetBtn = document.getElementById('add-pet-btn');
    const petForm = document.getElementById('pet-form');
    const petFormElement = document.getElementById('pet-form-element');
    const uploadImageBtn = document.getElementById('upload-image-btn');
    const petImageInput = document.getElementById('pet-image');
    
    // Form step elements
    const step1 = document.getElementById('step1');
    const step2 = document.getElementById('step2');
    const nextStepBtn = document.getElementById('next-step-btn');
    const prevStepBtn = document.getElementById('prev-step-btn');
    const stepIndicators = document.querySelectorAll('.step');
    const speciesSelect = document.getElementById('species');
    const breedSelect = document.getElementById('breed');

    // Breed options for each species
    const breedsBySpecies = {
        'Dog': [
            'Labrador Retriever',
            'German Shepherd',
            'Golden Retriever',
            'French Bulldog',
            'Poodle',
            'Beagle',
            'Rottweiler',
            'Siberian Husky',
            'Boxer',
            'Other'
        ],
        'Cat': [
            'Siamese',
            'Persian',
            'Maine Coon',
            'British Shorthair',
            'Ragdoll',
            'Bengal',
            'Sphynx',
            'American Shorthair',
            'Russian Blue',
            'Other'
        ],
        'Bird': [
            'Parakeet',
            'Cockatiel',
            'Canary',
            'Parrot',
            'Cockatoo',
            'Finch',
            'Lovebird',
            'Conure',
            'African Grey',
            'Other'
        ],
        'Rabbit': [
            'Holland Lop',
            'Dutch',
            'Rex',
            'Mini Lop',
            'Netherland Dwarf',
            'English Angora',
            'Lionhead',
            'French Lop',
            'Flemish Giant',
            'Other'
        ],
        'Hamster': [
            'Syrian',
            'Dwarf Campbell',
            'Dwarf Winter White',
            'Roborovski',
            'Chinese',
            'Other'
        ]
    };

    // Update breed options based on selected species
    function updateBreedOptions(species) {
        breedSelect.innerHTML = '<option value="">Select Breed</option>';
        
        if (species) {
            const breeds = breedsBySpecies[species] || ['Other'];
            breeds.forEach(breed => {
                const option = document.createElement('option');
                option.value = breed;
                option.textContent = breed;
                breedSelect.appendChild(option);
            });
            breedSelect.required = true;
        } else {
            breedSelect.required = false;
        }
    }

    // Event listener for species selection
    speciesSelect.addEventListener('change', (e) => {
        updateBreedOptions(e.target.value);
    });

    function showStep(stepNumber) {
        // Update step indicators
        stepIndicators.forEach(indicator => {
            if (parseInt(indicator.dataset.step) <= stepNumber) {
                indicator.classList.add('active');
            } else {
                indicator.classList.remove('active');
            }
        });

        // Show/hide appropriate step
        if (stepNumber === 1) {
            step1.classList.remove('hidden');
            step2.classList.add('hidden');
        } else {
            step1.classList.add('hidden');
            step2.classList.remove('hidden');
        }
    }

    function validateStep1() {
        const required = ['name', 'species', 'breed'];
        let valid = true;
        required.forEach(field => {
            const input = document.getElementById(field);
            if (!input.value.trim()) {
                valid = false;
                input.classList.add('invalid');
            } else {
                input.classList.remove('invalid');
            }
        });
        return valid;
    }

    nextStepBtn.addEventListener('click', () => {
        if (validateStep1()) {
            showStep(2);
        } else {
            alert('Please fill in all required fields in Step 1');
        }
    });

    prevStepBtn.addEventListener('click', () => {
        showStep(1);
    });

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
        formTitle.textContent = pet ? 'Edit Super Pet' : 'Create Your Super Pet';
        petFormElement.reset();
        showStep(1); // Always start at step 1

        if (pet) {
            document.getElementById('pet-id').value = pet.id;
            document.getElementById('name').value = pet.name;
            document.getElementById('hero_name').value = pet.hero_name;
            document.getElementById('species').value = pet.species;
            updateBreedOptions(pet.species);
            document.getElementById('breed').value = pet.breed || '';
            document.getElementById('age').value = pet.age || '';
            document.getElementById('gender').value = pet.gender || '';
            document.getElementById('color').value = pet.color || '';
            document.getElementById('superpower').value = pet.superpower;
            document.getElementById('hero_type').value = pet.hero_type;
            document.getElementById('hero_appearance').value = pet.hero_appearance || '';
        } else {
            document.getElementById('pet-id').value = '';
            updateBreedOptions(''); // Reset breed options
        }

        petForm.classList.remove('hidden');
    }

    searchBtn.addEventListener('click', () => {
        fetchPets(searchInput.value);
    });

    addPetBtn.addEventListener('click', () => {
        showPetForm();
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
        console.log(`Manage inventory for pet ${petId}`);
    }

    fetchPets();
});
