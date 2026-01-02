class PokemonGuide {
    constructor() {
        this.currentPokemonId = 1;
        this.maxPokemonId = 151; // First generation
        this.isUppercase = true; // Default to uppercase for accessibility
        this.isAdvancedMode = false; // New advanced mode toggle
        this.apiEndpoint = 'https://pokeapi.co/api/v2';
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

        // Advanced mode toggle
        document.getElementById('advanced-toggle').addEventListener('click', () => {
            this.toggleAdvancedMode();
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

        // Load advanced mode preference
        const savedAdvancedMode = localStorage.getItem('pokemon-guide-advanced-mode');
        if (savedAdvancedMode !== null) {
            this.isAdvancedMode = savedAdvancedMode === 'true';
            const container = document.getElementById('pokemon-container');
            const toggleBtn = document.getElementById('advanced-toggle');
            
            if (this.isAdvancedMode) {
                container.classList.add('advanced-mode');
                toggleBtn.textContent = '📊';
                toggleBtn.title = 'Modo Simple';
            }
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

        // Fetch Pokemon data
        const pokemonResponse = await fetch(`${this.apiEndpoint}/pokemon/${id}`);
        if (!pokemonResponse.ok) {
            throw new Error(`HTTP error! status: ${pokemonResponse.status}`);
        }
        const pokemonData = await pokemonResponse.json();

        // Fetch Pokemon species data for names
        const speciesResponse = await fetch(pokemonData.species.url);
        if (!speciesResponse.ok) {
            throw new Error(`HTTP error! status: ${speciesResponse.status}`);
        }
        const speciesData = await speciesResponse.json();

        // Process the data
        const pokemon = this.processPokemonData(pokemonData, speciesData);
        
        // Cache the result
        this.cache.set(cacheKey, pokemon);
        
        return pokemon;
    }

    processPokemonData(pokemonData, speciesData) {
        return {
            id: pokemonData.id,
            name: this.extractNames(speciesData.names || []),
            image: pokemonData.sprites.front_default || `https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/${pokemonData.id}.png`,
            height: pokemonData.height,
            weight: pokemonData.weight,
            generation: speciesData.generation?.name || 'generation-i',
            types: pokemonData.types.map(typeData => ({
                name: typeData.type.name,
                translations: {} // Types will be translated via i18n
            })),
            stats: pokemonData.stats.map(stat => ({
                name: stat.stat.name,
                value: stat.base_stat
            })),
            abilities: pokemonData.abilities.map(ability => ({
                name: ability.ability.name,
                isHidden: ability.is_hidden
            }))
        };
    }

    extractNames(nameArray) {
        const names = { ca: '', es: '', en: '' };
        const languageMap = { 
            'ca': 'ca', 
            'es': 'es', 
            'en': 'en',
            'spanish': 'es',
            'english': 'en'
        };
        
        nameArray.forEach(item => {
            const lang = languageMap[item.language.name];
            if (lang) {
                names[lang] = item.name;
            }
        });
        
        return names;
    }

    getTypeIcon(typeName) {
        const typeIcons = {
            'normal': '⚪',
            'fire': '🔥',
            'water': '💧',
            'electric': '⚡',
            'grass': '🌿',
            'ice': '❄️',
            'fighting': '👊',
            'poison': '☠️',
            'ground': '🌍',
            'flying': '🪶',
            'psychic': '🔮',
            'bug': '🐛',
            'rock': '🪨',
            'ghost': '👻',
            'dragon': '🐉',
            'dark': '🌙',
            'steel': '⚙️',
            'fairy': '🧚'
        };
        
        return typeIcons[typeName] || '❓';
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

        // Update generation
        const genNumber = pokemon.generation.replace('generation-', '').toUpperCase();
        document.getElementById('pokemon-generation').textContent = `Gen ${genNumber}`;

        // Update types
        const typesContainer = document.getElementById('pokemon-types');
        typesContainer.innerHTML = '';
        
        pokemon.types.forEach(type => {
            const badge = document.createElement('span');
            badge.className = 'type-badge';
            
            const icon = document.createElement('span');
            icon.className = 'type-icon';
            icon.textContent = this.getTypeIcon(type.name);
            
            const text = document.createElement('span');
            text.textContent = window.i18n.t(`types.${type.name}`) || type.translations[currentLang] || type.name;
            
            badge.appendChild(icon);
            badge.appendChild(text);
            badge.style.backgroundColor = window.i18n.getTypeColor(type.name);
            typesContainer.appendChild(badge);
        });

        // Update basic info
        document.getElementById('pokemon-height').textContent = window.i18n.formatHeight(pokemon.height);
        document.getElementById('pokemon-weight').textContent = window.i18n.formatWeight(pokemon.weight);
        document.getElementById('pokemon-number').textContent = `#${pokemon.id.toString().padStart(3, '0')}`;

        // Update advanced info if in advanced mode
        if (this.isAdvancedMode) {
            this.displayAdvancedInfo(pokemon);
        }
    }

    displayAdvancedInfo(pokemon) {
        // Update stats
        const statsContainer = document.getElementById('pokemon-stats');
        statsContainer.innerHTML = '';
        
        pokemon.stats.forEach(stat => {
            const statDiv = document.createElement('div');
            statDiv.className = 'stat-item';
            
            const statName = document.createElement('span');
            statName.className = 'stat-name';
            statName.textContent = this.getStatName(stat.name);
            
            const statBar = document.createElement('div');
            statBar.className = 'stat-bar';
            
            const statFill = document.createElement('div');
            statFill.className = 'stat-fill';
            statFill.style.width = `${(stat.value / 255) * 100}%`;
            
            const statValue = document.createElement('span');
            statValue.className = 'stat-value';
            statValue.textContent = stat.value;
            
            statBar.appendChild(statFill);
            statDiv.appendChild(statName);
            statDiv.appendChild(statBar);
            statDiv.appendChild(statValue);
            statsContainer.appendChild(statDiv);
        });

        // Update abilities
        const abilitiesContainer = document.getElementById('pokemon-abilities');
        abilitiesContainer.innerHTML = '';
        
        pokemon.abilities.forEach(ability => {
            const abilityDiv = document.createElement('div');
            abilityDiv.className = `ability-item ${ability.isHidden ? 'hidden-ability' : ''}`;
            abilityDiv.textContent = ability.name.replace('-', ' ');
            abilitiesContainer.appendChild(abilityDiv);
        });
    }

    getStatName(statName) {
        const statNames = {
            'hp': 'HP',
            'attack': 'ATK',
            'defense': 'DEF',
            'special-attack': 'SP.ATK',
            'special-defense': 'SP.DEF',
            'speed': 'SPD'
        };
        return statNames[statName] || statName;
    }

    toggleAdvancedMode() {
        this.isAdvancedMode = !this.isAdvancedMode;
        const container = document.getElementById('pokemon-container');
        const toggleBtn = document.getElementById('advanced-toggle');
        
        if (this.isAdvancedMode) {
            container.classList.add('advanced-mode');
            toggleBtn.textContent = '📊';
            toggleBtn.title = 'Modo Simple';
        } else {
            container.classList.remove('advanced-mode');
            toggleBtn.textContent = '📋';
            toggleBtn.title = 'Modo Avanzado';
        }
        
        this.displayCurrentPokemon();
        localStorage.setItem('pokemon-guide-advanced-mode', this.isAdvancedMode.toString());
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
