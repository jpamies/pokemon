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

        document.getElementById('list-btn').addEventListener('click', () => {
            this.showPokemonList();
        });

        document.getElementById('close-list-btn').addEventListener('click', () => {
            this.hidePokemonList();
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

        // Fetch generation data for region name
        const generationResponse = await fetch(speciesData.generation.url);
        if (!generationResponse.ok) {
            throw new Error(`HTTP error! status: ${generationResponse.status}`);
        }
        const generationData = await generationResponse.json();

        // Fetch evolution chain data
        const evolutionResponse = await fetch(speciesData.evolution_chain.url);
        if (!evolutionResponse.ok) {
            throw new Error(`HTTP error! status: ${evolutionResponse.status}`);
        }
        const evolutionData = await evolutionResponse.json();

        // Fetch ability translations
        const abilitiesWithTranslations = await this.fetchAbilityTranslations(pokemonData.abilities);

        // Process the data
        const pokemon = this.processPokemonData(pokemonData, speciesData, generationData, evolutionData, abilitiesWithTranslations);
        
        // Cache the result
        this.cache.set(cacheKey, pokemon);
        
        return pokemon;
    }

    async fetchAbilityTranslations(abilities) {
        const translatedAbilities = [];
        
        for (const abilityData of abilities) {
            try {
                const abilityResponse = await fetch(abilityData.ability.url);
                const abilityDetails = await abilityResponse.json();
                
                const translations = this.extractNames(abilityDetails.names || []);
                
                translatedAbilities.push({
                    name: abilityData.ability.name,
                    translations: translations,
                    isHidden: abilityData.is_hidden
                });
            } catch (error) {
                // Fallback to original name if translation fails
                translatedAbilities.push({
                    name: abilityData.ability.name,
                    translations: { en: abilityData.ability.name, es: abilityData.ability.name, ca: abilityData.ability.name },
                    isHidden: abilityData.is_hidden
                });
            }
        }
        
        return translatedAbilities;
    }

    processPokemonData(pokemonData, speciesData, generationData, evolutionData, abilitiesWithTranslations) {
        const evolutionChain = this.parseEvolutionChain(evolutionData.chain, pokemonData.name);
        
        return {
            id: pokemonData.id,
            name: this.extractNames(speciesData.names || []),
            image: pokemonData.sprites.front_default || `https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/${pokemonData.id}.png`,
            height: pokemonData.height,
            weight: pokemonData.weight,
            generation: speciesData.generation?.name || 'generation-i',
            region: generationData.main_region?.name || 'kanto',
            evolutionChain: evolutionChain.chain,
            evolutionStage: evolutionChain.currentStage,
            description: this.extractDescription(speciesData.flavor_text_entries || []),
            color: speciesData.color?.name || 'unknown',
            habitat: speciesData.habitat?.name || 'unknown',
            isLegendary: speciesData.is_legendary || false,
            isMythical: speciesData.is_mythical || false,
            types: pokemonData.types.map(typeData => ({
                name: typeData.type.name,
                translations: {} // Types will be translated via i18n
            })),
            stats: pokemonData.stats.map(stat => ({
                name: stat.stat.name,
                value: stat.base_stat
            })),
            abilities: abilitiesWithTranslations
        };
    }

    extractDescription(flavorTextEntries) {
        const currentLang = window.i18n?.currentLanguage || 'en';
        let targetLang = currentLang;
        
        // For Catalan, use Spanish as fallback
        if (currentLang === 'ca') {
            targetLang = 'es';
        }
        
        // Find description in target language
        let description = flavorTextEntries.find(entry => entry.language.name === targetLang);
        
        // Fallback to English if not found
        if (!description) {
            description = flavorTextEntries.find(entry => entry.language.name === 'en');
        }
        
        if (description) {
            // Clean up the text (remove form feeds and extra spaces)
            return description.flavor_text.replace(/\f/g, ' ').replace(/\n/g, ' ').replace(/\s+/g, ' ').trim();
        }
        
        return '';
    }

    parseEvolutionChain(chain, currentPokemonName) {
        const evolutionChain = [];
        let currentStage = 0;
        
        const parseChain = (node, stage) => {
            const pokemonId = this.extractPokemonIdFromUrl(node.species.url);
            const evolution = {
                name: node.species.name,
                id: pokemonId,
                stage: stage,
                level: null
            };
            
            if (node.evolution_details && node.evolution_details.length > 0) {
                evolution.level = node.evolution_details[0].min_level;
            }
            
            evolutionChain.push(evolution);
            
            if (node.species.name === currentPokemonName) {
                currentStage = stage;
            }
            
            if (node.evolves_to && node.evolves_to.length > 0) {
                node.evolves_to.forEach(evolution => {
                    parseChain(evolution, stage + 1);
                });
            }
        };
        
        parseChain(chain, 1);
        
        return {
            chain: evolutionChain,
            currentStage: currentStage
        };
    }

    extractPokemonIdFromUrl(url) {
        const matches = url.match(/\/(\d+)\/$/);
        return matches ? parseInt(matches[1]) : 1;
    }

    translateColor(color) {
        const colors = {
            'black': { ca: 'Negre', es: 'Negro', en: 'Black' },
            'blue': { ca: 'Blau', es: 'Azul', en: 'Blue' },
            'brown': { ca: 'Marró', es: 'Marrón', en: 'Brown' },
            'gray': { ca: 'Gris', es: 'Gris', en: 'Gray' },
            'green': { ca: 'Verd', es: 'Verde', en: 'Green' },
            'pink': { ca: 'Rosa', es: 'Rosa', en: 'Pink' },
            'purple': { ca: 'Morat', es: 'Morado', en: 'Purple' },
            'red': { ca: 'Vermell', es: 'Rojo', en: 'Red' },
            'white': { ca: 'Blanc', es: 'Blanco', en: 'White' },
            'yellow': { ca: 'Groc', es: 'Amarillo', en: 'Yellow' }
        };
        
        const currentLang = window.i18n.currentLanguage;
        return colors[color]?.[currentLang] || colors[color]?.en || color;
    }

    translateHabitat(habitat) {
        const habitats = {
            'cave': { ca: 'Cova', es: 'Cueva', en: 'Cave' },
            'forest': { ca: 'Bosc', es: 'Bosque', en: 'Forest' },
            'grassland': { ca: 'Praderia', es: 'Pradera', en: 'Grassland' },
            'mountain': { ca: 'Muntanya', es: 'Montaña', en: 'Mountain' },
            'rare': { ca: 'Rar', es: 'Raro', en: 'Rare' },
            'rough-terrain': { ca: 'Terreny accidentat', es: 'Terreno accidentado', en: 'Rough terrain' },
            'sea': { ca: 'Mar', es: 'Mar', en: 'Sea' },
            'urban': { ca: 'Urbà', es: 'Urbano', en: 'Urban' },
            'waters-edge': { ca: 'Vora de l\'aigua', es: 'Orilla del agua', en: 'Waters edge' },
            'unknown': { ca: 'Desconegut', es: 'Desconocido', en: 'Unknown' }
        };
        
        const currentLang = window.i18n.currentLanguage;
        return habitats[habitat]?.[currentLang] || habitats[habitat]?.en || habitat;
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
        const regionName = pokemon.region.charAt(0).toUpperCase() + pokemon.region.slice(1);
        document.getElementById('pokemon-generation').textContent = `Gen ${genNumber} - ${regionName}`;

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

        // Update description
        document.getElementById('pokemon-description').textContent = pokemon.description || 'No hi ha descripció disponible.';

        // Update details
        document.getElementById('pokemon-color').textContent = this.translateColor(pokemon.color);
        document.getElementById('pokemon-habitat').textContent = this.translateHabitat(pokemon.habitat);

        // Update special status
        const specialContainer = document.getElementById('pokemon-special');
        specialContainer.innerHTML = '';
        
        if (pokemon.isLegendary) {
            const legendaryBadge = document.createElement('span');
            legendaryBadge.className = 'special-badge legendary';
            legendaryBadge.textContent = '👑 LLEGENDARI';
            specialContainer.appendChild(legendaryBadge);
        }
        
        if (pokemon.isMythical) {
            const mythicalBadge = document.createElement('span');
            mythicalBadge.className = 'special-badge mythical';
            mythicalBadge.textContent = '✨ MÍTIC';
            specialContainer.appendChild(mythicalBadge);
        }

        // Update advanced info if in advanced mode
        if (this.isAdvancedMode) {
            this.displayAdvancedInfo(pokemon);
        }

        // Always display evolution chain (both simple and advanced modes)
        this.displayEvolutionChain(pokemon);
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
            
            // Get translated name with intelligent fallback
            const currentLang = window.i18n.currentLanguage;
            let abilityName;
            
            if (currentLang === 'ca') {
                // For Catalan, use Spanish as fallback since it's not available in API
                abilityName = ability.translations.es || ability.translations.en || ability.name;
            } else {
                abilityName = ability.translations[currentLang] || ability.translations.en || ability.name;
            }
            
            // Replace hyphens with spaces
            abilityName = abilityName.replace('-', ' ');
            
            // Apply uppercase mode if enabled
            if (this.isUppercase) {
                abilityName = abilityName.toUpperCase();
            } else {
                // Capitalize first letter of each word
                abilityName = abilityName.split(' ').map(word => 
                    word.charAt(0).toUpperCase() + word.slice(1).toLowerCase()
                ).join(' ');
            }
            
            abilityDiv.textContent = abilityName;
            abilitiesContainer.appendChild(abilityDiv);
        });
    }

    displayEvolutionChain(pokemon) {
        const evolutionContainer = document.getElementById('pokemon-evolution');
        evolutionContainer.innerHTML = '';
        
        if (!pokemon.evolutionChain || pokemon.evolutionChain.length <= 1) {
            evolutionContainer.innerHTML = '<p class="no-evolution">Este Pokémon no evoluciona</p>';
            return;
        }
        
        const chainDiv = document.createElement('div');
        chainDiv.className = 'evolution-chain';
        
        pokemon.evolutionChain.forEach((evolution, index) => {
            const evolutionDiv = document.createElement('div');
            evolutionDiv.className = `evolution-item ${evolution.stage === pokemon.evolutionStage ? 'current' : ''}`;
            evolutionDiv.style.cursor = 'pointer';
            evolutionDiv.title = `Cambiar a ${evolution.name}`;
            
            // Add click event to change Pokemon
            evolutionDiv.addEventListener('click', () => {
                if (evolution.id !== pokemon.id) {
                    this.currentPokemonId = evolution.id;
                    this.loadPokemon(evolution.id);
                }
            });
            
            const img = document.createElement('img');
            img.src = `https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/${evolution.id}.png`;
            img.alt = evolution.name;
            img.className = 'evolution-image';
            
            const name = document.createElement('div');
            name.className = 'evolution-name';
            name.textContent = evolution.name.charAt(0).toUpperCase() + evolution.name.slice(1);
            
            const stage = document.createElement('div');
            stage.className = 'evolution-stage';
            stage.textContent = `Etapa ${evolution.stage}`;
            
            evolutionDiv.appendChild(img);
            evolutionDiv.appendChild(name);
            evolutionDiv.appendChild(stage);
            
            if (evolution.level && index > 0) {
                const levelInfo = document.createElement('div');
                levelInfo.className = 'evolution-level';
                levelInfo.textContent = `Nv. ${evolution.level}`;
                evolutionDiv.appendChild(levelInfo);
            }
            
            chainDiv.appendChild(evolutionDiv);
            
            // Add arrow between evolutions
            if (index < pokemon.evolutionChain.length - 1) {
                const arrow = document.createElement('div');
                arrow.className = 'evolution-arrow';
                arrow.textContent = '→';
                chainDiv.appendChild(arrow);
            }
        });
        
        evolutionContainer.appendChild(chainDiv);
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

    async showPokemonList() {
        const listContainer = document.getElementById('pokemon-list-container');
        const pokemonContainer = document.getElementById('pokemon-container');
        const navigation = document.querySelector('.navigation');
        const counter = document.querySelector('.pokemon-counter');
        
        // Hide main view
        pokemonContainer.classList.add('hidden');
        navigation.classList.add('hidden');
        counter.classList.add('hidden');
        
        // Show list view
        listContainer.classList.remove('hidden');
        
        // Generate list if not already done
        await this.generatePokemonList();
    }

    hidePokemonList() {
        const listContainer = document.getElementById('pokemon-list-container');
        const pokemonContainer = document.getElementById('pokemon-container');
        const navigation = document.querySelector('.navigation');
        const counter = document.querySelector('.pokemon-counter');
        
        // Show main view
        pokemonContainer.classList.remove('hidden');
        navigation.classList.remove('hidden');
        counter.classList.remove('hidden');
        
        // Hide list view
        listContainer.classList.add('hidden');
    }

    async generatePokemonList() {
        const grid = document.getElementById('pokemon-grid');
        
        // Only generate once
        if (grid.children.length > 0) return;
        
        this.showLoading();
        
        for (let i = 1; i <= this.maxPokemonId; i++) {
            const pokemonItem = document.createElement('div');
            pokemonItem.className = 'pokemon-list-item';
            pokemonItem.style.cursor = 'pointer';
            
            const img = document.createElement('img');
            img.src = `https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/${i}.png`;
            img.alt = `Pokemon #${i}`;
            img.className = 'pokemon-list-image';
            
            const id = document.createElement('div');
            id.className = 'pokemon-list-id';
            id.textContent = `#${i.toString().padStart(3, '0')}`;
            
            const name = document.createElement('div');
            name.className = 'pokemon-list-name';
            name.textContent = 'Carregant...';
            
            pokemonItem.appendChild(img);
            pokemonItem.appendChild(id);
            pokemonItem.appendChild(name);
            
            // Add click event
            pokemonItem.addEventListener('click', () => {
                this.currentPokemonId = i;
                this.hidePokemonList();
                this.loadPokemon(i);
            });
            
            grid.appendChild(pokemonItem);
            
            // Load name asynchronously
            this.loadPokemonName(i, name);
        }
        
        this.hideLoading();
    }

    async loadPokemonName(id, nameElement) {
        try {
            // Check cache first
            const cacheKey = `pokemon_${id}`;
            if (this.cache.has(cacheKey)) {
                const pokemon = this.cache.get(cacheKey);
                const currentLang = window.i18n.currentLanguage;
                nameElement.textContent = pokemon.name[currentLang] || pokemon.name.en || `Pokemon #${id}`;
                return;
            }

            // Fetch basic pokemon data for species URL
            const pokemonResponse = await fetch(`${this.apiEndpoint}/pokemon/${id}`);
            const pokemonData = await pokemonResponse.json();
            
            // Fetch species data for names
            const speciesResponse = await fetch(pokemonData.species.url);
            const speciesData = await speciesResponse.json();
            
            const names = this.extractNames(speciesData.names || []);
            const currentLang = window.i18n.currentLanguage;
            nameElement.textContent = names[currentLang] || names.en || `Pokemon #${id}`;
            
        } catch (error) {
            nameElement.textContent = `Pokemon #${id}`;
        }
    }
}

// Initialize the app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new PokemonGuide();
});
