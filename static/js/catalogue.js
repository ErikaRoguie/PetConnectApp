document.addEventListener('DOMContentLoaded', () => {
    const catalogueSearch = document.getElementById('catalogue-search');
    const catalogueSort = document.getElementById('catalogue-sort');
    const catalogueList = document.getElementById('catalogue-list');

    let pets = [];

    function fetchPets() {
        fetch('/api/pets')
            .then(response => response.json())
            .then(data => {
                pets = data;
                renderPets();
            });
    }

    function renderPets() {
        const filteredPets = filterPets(pets);
        const sortedPets = sortPets(filteredPets);

        catalogueList.innerHTML = '';
        sortedPets.forEach(pet => {
            const petCard = createPetCard(pet);
            catalogueList.appendChild(petCard);
        });
    }

    function filterPets(petsToFilter) {
        const searchTerm = catalogueSearch.value.toLowerCase();
        return petsToFilter.filter(pet => 
            pet.hero_name.toLowerCase().includes(searchTerm) ||
            pet.superpower.toLowerCase().includes(searchTerm)
        );
    }

    function sortPets(petsToSort) {
        const sortBy = catalogueSort.value;
        return petsToSort.sort((a, b) => a[sortBy].localeCompare(b[sortBy]));
    }

    function createPetCard(pet) {
        const card = document.createElement('div');
        card.className = 'pet-card';
        card.innerHTML = `
            <img src="${pet.image_url || '/static/images/DC,WB.jpg'}" alt="${pet.hero_name}" class="pet-image">
            <h3>${pet.hero_name}</h3>
            <p>Superpower: ${pet.superpower}</p>
            <a href="/pets#${pet.id}" class="btn">View Details</a>
        `;
        return card;
    }

    catalogueSearch.addEventListener('input', renderPets);
    catalogueSort.addEventListener('change', renderPets);

    fetchPets();
});