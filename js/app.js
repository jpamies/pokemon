class PokemonGuide {
    constructor() {
        this.currentPokemonId = 1;
        this.maxPokemonId = 151; // First generation
        this.isUppercase = true; // Default to uppercase for accessibility
        this.apiEndpoint = 'https://graphql.pokeapi.co/v1beta2';
        this.cache = new Map();
        
        this.initializeApp();
    }

    async initializeApp() {
        // Wait for i18n to load
        await new Promise(resolve => {
            const checkI18n = () => {
                if (window.i18n && Object.keys(window.i18n.translations).length > 0) {
                    resolve();
                } else {
                    setTimeout(checkI18n, 100);
                }
            };
            checkI18n();
        });

        this.setupEventListeners();
        this.initializeFromStorage();
        this.applyAccessibilityMode();
        await this.loadPokemon(this.currentPokemonId);
    }

    setupEventListeners() {
        // Language selector
        document.getElementById('language-selector').addEventListener('change', (e) => {
            window.i18n.setLanguage(e.target.value);
            this.displayCurrentPokemon(); // Refresh display with new language
        });

        // Accessibility toggle
        document.getElementById('accessibility-toggle').addEventListener('click', () => {
            this.toggleAccessibilityMode();
        });

        // Navigation buttons
        document.getElementById('prev-btn').addEventListener('click', () => {
            this.navigatePokemon(-1);
        });

        document.getElementById('next-btn').addEventListener('click', () => {
            this.navigatePokemon(1);
        });

        document.getElementById('home-btn').addEventListener('click', () => {
            this.goHome();
        });

        // Retry button
        document.getElementById('retry-btn').addEventListener('click', () => {
            this.hideError();
            this.loadPokemon(this.currentPokemonId);
        });

        // Keyboard navigation
        document.addEventListener('keydown', (e) => {
            if (e.key === 'ArrowLeft') this.navigatePokemon(-1);
            if (e.key === 'ArrowRight') this.navigatePokemon(1);
            if (e.key === 'Home') this.goHome();
        });
    }

    initializeFromStorage() {
        // Load saved language
        window.i18n.initializeFromStorage();
        
        // Load saved Pokemon ID
        const savedId = localStorage.getItem('pokemon-guide-current-id');
        if (savedId && savedId >= 1 && savedId <= this.maxPokemonId) {
            this.currentPokemonId = parseInt(savedId);
        }

        // Load accessibility preference
        const savedAccessibility = localStorage.getItem('pokemon-guide-uppercase');
        if (savedAccessibility !== null) {
            this.isUppercase = savedAccessibility === 'true';
        }
    }

    toggleAccessibilityMode() {
        this.isUppercase = !this.isUppercase;
        this.applyAccessibilityMode();
        localStorage.setItem('pokemon-guide-uppercase', this.isUppercase.toString());
    }

    applyAccessibilityMode() {
        const body = document.body;
        const toggleText = document.getElementById('accessibility-text');
        
        if (this.isUppercase) {
            body.classList.add('uppercase');
            toggleText.textContent = 'Aa';
        } else {
            body.classList.remove('uppercase');
            toggleText.textContent = 'AA';
        }
    }

    async loadPokemon(id) {
        this.showLoading();
        
        try {
            const pokemon = await this.fetchPokemon(id);
            this.currentPokemon = pokemon;
            this.displayCurrentPokemon();
            this.updateNavigation();
            this.updateCounter();
            
            // Save current ID
            localStorage.setItem('pokemon-guide-current-id', id.toString());
            
        } catch (error) {
            console.error('Error loading Pokemon:', error);
            this.showError();
        } finally {
            this.hideLoading();
        }
    }

    async fetchPokemon(id) {
        const cacheKey = `pokemon_${id}`;
        
        // Check cache first
        if (this.cache.has(cacheKey)) {
            return this.cache.get(cacheKey);
        }

        const query = `
            query GetPokemon($id: Int!) {
                pokemon(where: {id: {_eq: $id}}) {
                    id
                    name
                    height
                    weight
                    pokemon_species {
                        pokemon_species_names(where: {language_id: {_in: [6, 7, 9]}}) {
                            name
                            language_id
                        }
                    }
                    pokemon_types {
                        type {
                            name
                            type_names(where: {language_id: {_in: [6, 7, 9]}}) {
                                name
                                language_id
                            }
                        }
                    }
                    pokemon_sprites {
                        sprites
                    }
                }
            }
        `;

        const response = await fetch(this.apiEndpoint, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ query, variables: { id } })
        });

        const data = await response.json();
        
        if (data.errors) {
            throw new Error(data.errors[0].message);
        }
        
        const pokemonData = data.data.pokemon[0];

        if (!pokemonData) {
            throw new Error('Pokemon not found');
        }

        // Process the data
        const pokemon = this.processPokemonData(pokemonData);
        
        // Cache the result
        this.cache.set(cacheKey, pokemon);
        
        return pokemon;
    }

    processPokemonData(data) {
        const sprites = JSON.parse(data.pokemon_sprites[0]?.sprites || '{}');
        
        return {
            id: data.id,
            name: this.extractNames(data.pokemon_species[0]?.pokemon_species_names || []),
            image: sprites.front_default || `https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/${data.id}.png`,
            height: data.height,
            weight: data.weight,
            types: data.pokemon_types.map(typeData => ({
                name: typeData.type.name,
                translations: this.extractNames(typeData.type.type_names || [])
            }))
        };
    }

    extractNames(nameArray) {
        const names = { ca: '', es: '', en: '' };
        const languageMap = { 6: 'ca', 7: 'es', 9: 'en' };
        
        nameArray.forEach(item => {
            const lang = languageMap[item.language_id];
            if (lang) {
                names[lang] = item.name;
            }
        });
        
        return names;
    }

    displayCurrentPokemon() {
        if (!this.currentPokemon) return;

        const pokemon = this.currentPokemon;
        const currentLang = window.i18n.currentLanguage;

        // Update image
        const img = document.getElementById('pokemon-image');
        img.src = pokemon.image;
        img.alt = pokemon.name[currentLang] || pokemon.name.en || 'Pokemon';

        // Update name
        document.getElementById('pokemon-name').textContent = 
            pokemon.name[currentLang] || pokemon.name.en || `Pokemon #${pokemon.id}`;

        // Update types
        const typesContainer = document.getElementById('pokemon-types');
        typesContainer.innerHTML = '';
        
        pokemon.types.forEach(type => {
            const badge = document.createElement('span');
            badge.className = 'type-badge';
            badge.textContent = window.i18n.t(`types.${type.name}`) || type.translations[currentLang] || type.name;
            badge.style.backgroundColor = window.i18n.getTypeColor(type.name);
            typesContainer.appendChild(badge);
        });

        // Update stats
        document.getElementById('pokemon-height').textContent = window.i18n.formatHeight(pokemon.height);
        document.getElementById('pokemon-weight').textContent = window.i18n.formatWeight(pokemon.weight);
        document.getElementById('pokemon-number').textContent = `#${pokemon.id.toString().padStart(3, '0')}`;
    }

    updateNavigation() {
        const prevBtn = document.getElementById('prev-btn');
        const nextBtn = document.getElementById('next-btn');
        
        prevBtn.disabled = this.currentPokemonId <= 1;
        nextBtn.disabled = this.currentPokemonId >= this.maxPokemonId;
    }

    updateCounter() {
        const counter = document.getElementById('counter-text');
        counter.textContent = `${this.currentPokemonId} ${window.i18n.t('counter')} ${this.maxPokemonId}`;
    }

    async navigatePokemon(direction) {
        const newId = this.currentPokemonId + direction;
        if (newId >= 1 && newId <= this.maxPokemonId) {
            this.currentPokemonId = newId;
            await this.loadPokemon(this.currentPokemonId);
        }
    }

    async goHome() {
        this.currentPokemonId = 1;
        await this.loadPokemon(this.currentPokemonId);
    }

    showLoading() {
        document.getElementById('loading').classList.remove('hidden');
        document.getElementById('pokemon-container').style.opacity = '0.5';
    }

    hideLoading() {
        document.getElementById('loading').classList.add('hidden');
        document.getElementById('pokemon-container').style.opacity = '1';
    }

    showError() {
        document.getElementById('error-message').classList.remove('hidden');
    }

    hideError() {
        document.getElementById('error-message').classList.add('hidden');
    }
}

// Initialize the app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new PokemonGuide();
});
