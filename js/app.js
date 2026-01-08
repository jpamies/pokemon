class PokemonGuide {
    constructor() {
        this.currentPokemonId = 1;
        this.maxPokemonId = 1025; // All Pokemon generations
        this.isUppercase = true; // Default to uppercase for accessibility
        this.isAdvancedMode = false; // New advanced mode toggle
        this.apiEndpoint = 'https://pokeapi.co/api/v2';
        this.cache = new Map();
        this.pokemonCache = new PokemonCache(); // Use new cache system
        this.pokemonDatabase = null; // Consolidated Pokemon database
        
        // Detect base path for subdirectories
        this.basePath = './';
        
        this.initializeApp();
        
        // Start preloading images in background
        this.preloadImages();
    }

    async initializeApp() {
        // Load consolidated Pokemon database
        await this.loadPokemonDatabase();
        
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

    async loadPokemonDatabase() {
        try {
            // Load individual Pokemon data files from data/ folder
            this.pokemonDatabase = {};
            console.log('Pokemon database initialized for individual file loading');
        } catch (error) {
            console.warn('Could not initialize Pokemon database:', error);
            this.pokemonDatabase = {};
        }
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

        // PDF export button
        document.getElementById('pdf-export').addEventListener('click', () => {
            this.exportToPDF();
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
        // Check URL for language parameter first
        const urlParams = new URLSearchParams(window.location.search);
        const urlLang = urlParams.get('lang');
        
        let savedLanguage = 'ca'; // Default
        
        // Priority: URL param > localStorage
        if (urlLang && ['ca', 'es', 'en'].includes(urlLang)) {
            savedLanguage = urlLang;
        } else {
            const storedLang = localStorage.getItem('pokemon-guide-language');
            if (storedLang && ['ca', 'es', 'en'].includes(storedLang)) {
                savedLanguage = storedLang;
            }
        }
        
        window.i18n.setLanguage(savedLanguage);
        
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
        // Check memory cache first
        const cacheKey = `pokemon_${id}`;
        if (this.cache.has(cacheKey)) {
            return this.cache.get(cacheKey);
        }

        try {
            // Load from local JSON file
            const paddedId = id.toString().padStart(4, '0');
            const response = await fetch(`${this.basePath}data/pokemon_${paddedId}.json`);
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const pokemonData = await response.json();
            
            // Convert to the format expected by the app
            const pokemon = {
                id: pokemonData.id,
                name: pokemonData.names || { en: pokemonData.name, es: pokemonData.name, ca: pokemonData.name },
                image: pokemonData.images?.official_artwork || `https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/${id}.png`,
                height: pokemonData.height,
                weight: pokemonData.weight,
                generation: `generation-${this.getGenerationRoman(pokemonData.generation)}`,
                region: this.getRegionFromGeneration(pokemonData.generation),
                evolutionChain: this.convertEvolutionChain(pokemonData.evolution || [], id),
                evolutionStage: this.getEvolutionStage(pokemonData.evolution || [], id),
                description: pokemonData.descriptions?.[window.i18n?.currentLanguage || 'en'] || pokemonData.descriptions?.en || '',
                color: pokemonData.color || 'unknown',
                habitat: 'unknown', // Not available in simplified data
                isLegendary: pokemonData.is_legendary || false,
                isMythical: pokemonData.is_mythical || false,
                types: (pokemonData.types || []).map(typeName => ({
                    name: typeName,
                    translations: {}
                })),
                stats: this.convertStats(pokemonData.stats || {}),
                abilities: (pokemonData.abilities || []).map(ability => ({
                    name: ability.name,
                    translations: { en: ability.name, es: ability.name, ca: ability.name },
                    isHidden: ability.is_hidden || false
                }))
            };
            
            // Cache the result
            this.cache.set(cacheKey, pokemon);
            
            return pokemon;
            
        } catch (error) {
            console.error(`Error loading Pokemon ${id}:`, error);
            throw error;
        }
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

    async processPokemonData(pokemonData, speciesData, generationData, evolutionData, abilitiesWithTranslations) {
        const evolutionChain = this.parseEvolutionChain(evolutionData.chain, pokemonData.name);
        
        return {
            id: pokemonData.id,
            name: this.extractNames(speciesData.names || []),
            image: `https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/${pokemonData.id}.png`,
            height: pokemonData.height,
            weight: pokemonData.weight,
            generation: speciesData.generation?.name || 'generation-i',
            region: generationData.main_region?.name || 'kanto',
            evolutionChain: evolutionChain.chain,
            evolutionStage: evolutionChain.currentStage,
            description: await this.extractDescription(speciesData.flavor_text_entries || [], pokemonData.id),
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

    async updateDescription(pokemonId) {
        const currentLang = window.i18n?.currentLanguage || 'en';
        let description = '';
        
        // Load description from individual JSON files in data/ folder
        try {
            const paddedId = pokemonId.toString().padStart(4, '0');
            const response = await fetch(`${this.basePath}data/pokemon_${paddedId}.json`);
            if (response.ok) {
                const pokemonData = await response.json();
                description = pokemonData.descriptions?.[currentLang] || pokemonData.description_catalan || pokemonData.description;
            }
        } catch (error) {
            console.warn(`Could not load description for Pokemon ${pokemonId}:`, error);
        }
        
        if (!description && this.currentPokemon) {
            // Fallback to cached description
            description = this.currentPokemon.description;
        }
        
        document.getElementById('pokemon-description').textContent = description || 'No description available.';
    }

    async getCatalanDescription(pokemonId) {
        // Load Pokemon data from individual JSON files in data/ folder
        try {
            const paddedId = pokemonId.toString().padStart(4, '0');
            const response = await fetch(`${this.basePath}data/pokemon_${paddedId}.json`);
            if (response.ok) {
                const pokemonData = await response.json();
                return pokemonData.descriptions?.ca || pokemonData.description_catalan || pokemonData.description || null;
            }
        } catch (error) {
            console.warn(`Could not load data for Pokemon ${pokemonId}:`, error);
        }
        return null;
    }

    async extractDescription(flavorTextEntries, pokemonId) {
        const currentLang = window.i18n?.currentLanguage || 'en';
        
        // For Catalan, use Pokemon data files with Bedrock translations
        if (currentLang === 'ca') {
            const catalanDescription = await this.getCatalanDescription(pokemonId);
            if (catalanDescription) {
                return catalanDescription;
            }
        }
        
        let targetLang = currentLang;
        
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

    getGenerationRoman(genNumber) {
        const romans = ['i', 'ii', 'iii', 'iv', 'v', 'vi', 'vii', 'viii', 'ix'];
        return romans[genNumber - 1] || 'i';
    }

    getRegionFromGeneration(genNumber) {
        const regions = ['kanto', 'johto', 'hoenn', 'sinnoh', 'unova', 'kalos', 'alola', 'galar', 'paldea'];
        return regions[genNumber - 1] || 'kanto';
    }

    convertEvolutionChain(evolutionArray, currentId) {
        return evolutionArray.map((evo, index) => ({
            name: evo.name,
            id: evo.id,
            stage: index + 1,
            level: null // Level info not available in simplified data
        }));
    }

    getEvolutionStage(evolutionArray, currentId) {
        const index = evolutionArray.findIndex(evo => evo.id === currentId);
        return index >= 0 ? index + 1 : 1;
    }

    convertStats(statsObj) {
        return [
            { name: 'hp', value: statsObj.hp || 0 },
            { name: 'attack', value: statsObj.attack || 0 },
            { name: 'defense', value: statsObj.defense || 0 },
            { name: 'special-attack', value: statsObj['special-attack'] || 0 },
            { name: 'special-defense', value: statsObj['special-defense'] || 0 },
            { name: 'speed', value: statsObj.speed || 0 }
        ];
    }

    translateColor(color) {
        const colors = {
            'black': { ca: 'Negre', es: 'Negro', en: 'Black', hex: '#2c2c2c' },
            'blue': { ca: 'Blau', es: 'Azul', en: 'Blue', hex: '#3b82f6' },
            'brown': { ca: 'Marró', es: 'Marrón', en: 'Brown', hex: '#8b4513' },
            'gray': { ca: 'Gris', es: 'Gris', en: 'Gray', hex: '#6b7280' },
            'green': { ca: 'Verd', es: 'Verde', en: 'Green', hex: '#22c55e' },
            'pink': { ca: 'Rosa', es: 'Rosa', en: 'Pink', hex: '#ec4899' },
            'purple': { ca: 'Morat', es: 'Morado', en: 'Purple', hex: '#a855f7' },
            'red': { ca: 'Vermell', es: 'Rojo', en: 'Red', hex: '#ef4444' },
            'white': { ca: 'Blanc', es: 'Blanco', en: 'White', hex: '#f8fafc' },
            'yellow': { ca: 'Groc', es: 'Amarillo', en: 'Yellow', hex: '#eab308' }
        };
        
        const currentLang = window.i18n.currentLanguage;
        const colorData = colors[color] || { ca: 'Desconegut', es: 'Desconocido', en: 'Unknown', hex: '#9ca3af' };
        return {
            name: colorData[currentLang] || colorData.en || color,
            hex: colorData.hex
        };
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
        // Create img element for PNG emoji
        const img = document.createElement('img');
        img.src = `${this.basePath}docs/emoji_icons/${typeName}.png`;
        img.alt = typeName;
        img.className = 'type-emoji';
        img.style.width = '16px';
        img.style.height = '16px';
        img.style.verticalAlign = 'middle';
        
        // Fallback to text emoji if image fails
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
        
        img.onerror = () => {
            img.style.display = 'none';
            const span = document.createElement('span');
            span.textContent = typeIcons[typeName] || '❓';
            img.parentNode.replaceChild(span, img);
        };
        
        return img;
    }

    getTypeIconText(typeName) {
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
            
            const icon = this.getTypeIcon(type.name);
            
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

        // Update description - reload for current language
        this.updateDescription(pokemon.id);

        // Update details
        const colorData = this.translateColor(pokemon.color);
        document.getElementById('pokemon-color').innerHTML = `<span class="color-box" style="background-color: ${colorData.hex}"></span> ${colorData.name}`;
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
            img.src = `https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/${evolution.id}.png`;
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
        const currentLang = window.i18n?.currentLanguage || 'en';
        const translations = window.i18n?.translations[currentLang]?.stats;
        
        if (translations && translations[statName]) {
            return translations[statName];
        }
        
        // Fallback to English abbreviations
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
        
        // Crear elementos sin cargar imágenes inmediatamente
        for (let i = 1; i <= this.maxPokemonId; i++) {
            const pokemonItem = document.createElement('div');
            pokemonItem.className = 'pokemon-list-item';
            pokemonItem.style.cursor = 'pointer';
            
            const img = document.createElement('img');
            img.alt = `Pokemon #${i}`;
            img.className = 'pokemon-list-image';
            img.style.backgroundColor = '#f0f0f0';
            // No cargar imagen inmediatamente
            img.dataset.src = `https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/${i}.png`;
            
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
        
        // Cargar imágenes progresivamente después de crear todos los elementos
        this.loadImagesProgressively();
    }

    async loadImagesProgressively() {
        const images = document.querySelectorAll('.pokemon-list-image[data-src]');
        const batchSize = 20; // Cargar en lotes pequeños
        const delay = 100; // Delay entre lotes
        
        for (let i = 0; i < images.length; i += batchSize) {
            const batch = Array.from(images).slice(i, i + batchSize);
            
            // Cargar lote actual
            batch.forEach(img => {
                if (img.dataset.src) {
                    img.src = img.dataset.src;
                    delete img.dataset.src;
                }
            });
            
            // Esperar antes del siguiente lote
            if (i + batchSize < images.length) {
                await new Promise(resolve => setTimeout(resolve, delay));
            }
        }
    }

    async preloadImages() {
        console.log('Starting image preload...');
        const batchSize = 50; // Preload in batches to avoid overwhelming the browser
        
        for (let start = 1; start <= this.maxPokemonId; start += batchSize) {
            const end = Math.min(start + batchSize - 1, this.maxPokemonId);
            
            // Preload batch
            const promises = [];
            for (let i = start; i <= end; i++) {
                promises.push(this.preloadImage(i));
            }
            
            await Promise.allSettled(promises);
            console.log(`Preloaded images ${start}-${end}`);
            
            // Small delay between batches to not block UI
            await new Promise(resolve => setTimeout(resolve, 100));
        }
        
        console.log('Image preload completed');
    }

    preloadImage(pokemonId) {
        return new Promise((resolve) => {
            const img = new Image();
            img.onload = () => resolve();
            img.onerror = () => resolve(); // Continue even if image fails
            img.src = `https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/${pokemonId}.png`;
        });
    }

    async exportToPDF() {
        this.showLoading();
        
        try {
            const { jsPDF } = window.jspdf;
            const pdf = new jsPDF('landscape', 'mm', 'a4'); // Horizontal A4
            
            const pageWidth = 297; // A4 landscape width
            const pageHeight = 210; // A4 landscape height
            const margin = 10;
            const cardWidth = 65;
            const cardHeight = 85;
            const cardsPerRow = 4;
            const cardsPerCol = 2;
            const cardsPerPage = cardsPerRow * cardsPerCol; // 8 cards per page
            
            let currentPage = 1;
            let cardCount = 0;
            
            // Title on first page
            pdf.setFontSize(20);
            pdf.text('Guia Pokémon per a Nens - Tots els Pokémon', pageWidth / 2, 15, { align: 'center' });
            
            for (let pokemonId = 1; pokemonId <= this.maxPokemonId; pokemonId++) {
                const pokemon = await this.fetchPokemon(pokemonId);
                
                if (cardCount > 0 && cardCount % cardsPerPage === 0) {
                    pdf.addPage('landscape');
                    currentPage++;
                }
                
                const row = Math.floor((cardCount % cardsPerPage) / cardsPerRow);
                const col = (cardCount % cardsPerPage) % cardsPerRow;
                
                const x = margin + col * (cardWidth + 5);
                const y = 25 + row * (cardHeight + 5);
                
                // Draw card border
                pdf.setDrawColor(231, 76, 60);
                pdf.setLineWidth(1);
                pdf.rect(x, y, cardWidth, cardHeight);
                
                // Pokemon image (placeholder - would need base64 conversion for actual images)
                pdf.setFillColor(240, 240, 240);
                pdf.rect(x + 5, y + 5, 25, 25, 'F');
                
                // Pokemon info
                pdf.setFontSize(10);
                pdf.setFont(undefined, 'bold');
                pdf.text(`#${pokemonId.toString().padStart(3, '0')}`, x + 35, y + 12);
                const pokemonName = (pokemon.name[window.i18n.currentLanguage] || pokemon.name.en || `Pokemon #${pokemonId}`).toUpperCase();
                pdf.text(pokemonName, x + 35, y + 18);
                
                // Types
                pdf.setFontSize(8);
                pdf.setFont(undefined, 'normal');
                const types = pokemon.types.map(type => this.getTypeIconText(type.name) + ' ' + (window.i18n.t(`types.${type.name}`) || type.name)).join(' ');
                pdf.text(types, x + 35, y + 24);
                
                // Stats (simplified)
                pdf.setFontSize(7);
                pdf.text(`Altura: ${(pokemon.height / 10).toFixed(1)}m`, x + 5, y + 40);
                pdf.text(`Peso: ${(pokemon.weight / 10).toFixed(1)}kg`, x + 5, y + 45);
                
                // Generation
                const generation = this.getGenerationFromId(pokemonId);
                pdf.text(`Gen ${generation.num} - ${generation.region}`, x + 5, y + 50);
                
                cardCount++;
                
                // Update progress
                if (pokemonId % 50 === 0) {
                    console.log(`PDF Progress: ${pokemonId}/${this.maxPokemonId}`);
                }
            }
            
            // Save PDF
            pdf.save('pokemon-guide-complete.pdf');
            
        } catch (error) {
            console.error('Error generating PDF:', error);
            alert('Error generant el PDF. Prova-ho més tard.');
        }
        
        this.hideLoading();
    }

    getGenerationFromId(pokemonId) {
        if (pokemonId <= 151) return { num: 'I', region: 'Kanto' };
        if (pokemonId <= 251) return { num: 'II', region: 'Johto' };
        if (pokemonId <= 386) return { num: 'III', region: 'Hoenn' };
        if (pokemonId <= 493) return { num: 'IV', region: 'Sinnoh' };
        if (pokemonId <= 649) return { num: 'V', region: 'Unova' };
        if (pokemonId <= 721) return { num: 'VI', region: 'Kalos' };
        if (pokemonId <= 809) return { num: 'VII', region: 'Alola' };
        if (pokemonId <= 905) return { num: 'VIII', region: 'Galar' };
        return { num: 'IX', region: 'Paldea' };
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

            // Load from local JSON file
            const paddedId = id.toString().padStart(4, '0');
            const response = await fetch(`${this.basePath}data/pokemon_${paddedId}.json`);
            
            if (response.ok) {
                const pokemonData = await response.json();
                const currentLang = window.i18n.currentLanguage;
                const names = pokemonData.names || { en: pokemonData.name, es: pokemonData.name, ca: pokemonData.name };
                nameElement.textContent = names[currentLang] || names.en || `Pokemon #${id}`;
            } else {
                nameElement.textContent = `Pokemon #${id}`;
            }
            
        } catch (error) {
            nameElement.textContent = `Pokemon #${id}`;
        }
    }
}

// Initialize the app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new PokemonGuide();
});
