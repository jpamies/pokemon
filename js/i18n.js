class I18n {
    constructor() {
        this.currentLanguage = 'ca'; // Default to Catalan
        this.translations = {};
        this.loadTranslations();
    }

    async loadTranslations() {
        const languages = ['ca', 'es', 'en'];
        
        for (const lang of languages) {
            try {
                const response = await fetch(`translations/${lang}.json`);
                this.translations[lang] = await response.json();
            } catch (error) {
                console.error(`Failed to load ${lang} translations:`, error);
            }
        }
    }

    setLanguage(language) {
        if (this.translations[language]) {
            this.currentLanguage = language;
            this.updateUI();
            localStorage.setItem('pokemon-guide-language', language);
        }
    }

    t(key) {
        const keys = key.split('.');
        let value = this.translations[this.currentLanguage];
        
        for (const k of keys) {
            value = value?.[k];
        }
        
        return value || key.toUpperCase();
    }

    updateUI() {
        // Update all translatable elements
        const elements = {
            'loading-text': this.t('loading'),
            'prev-text': this.t('previous'),
            'next-text': this.t('next'),
            'home-text': this.t('home'),
            'height-label': this.t('height'),
            'weight-label': this.t('weight'),
            'number-label': this.t('number'),
            'error-text': this.t('error'),
            'retry-btn': this.t('retry')
        };

        for (const [id, text] of Object.entries(elements)) {
            const element = document.getElementById(id);
            if (element) {
                element.textContent = text;
            }
        }

        // Update HTML lang attribute
        document.documentElement.lang = this.currentLanguage;
        
        // Update language selector
        const selector = document.getElementById('language-selector');
        if (selector) {
            selector.value = this.currentLanguage;
        }
    }

    getTypeColor(type) {
        const typeColors = {
            normal: '#A8A878',
            fire: '#F08030',
            water: '#6890F0',
            electric: '#F8D030',
            grass: '#78C850',
            ice: '#98D8D8',
            fighting: '#C03028',
            poison: '#A040A0',
            ground: '#E0C068',
            flying: '#A890F0',
            psychic: '#F85888',
            bug: '#A8B820',
            rock: '#B8A038',
            ghost: '#705898',
            dragon: '#7038F8',
            dark: '#705848',
            steel: '#B8B8D0',
            fairy: '#EE99AC'
        };
        
        return typeColors[type] || '#68A090';
    }

    formatHeight(decimeters) {
        const meters = decimeters / 10;
        return `${meters.toFixed(1)}M`;
    }

    formatWeight(hectograms) {
        const kilograms = hectograms / 10;
        return `${kilograms.toFixed(1)}KG`;
    }

    initializeFromStorage() {
        const savedLanguage = localStorage.getItem('pokemon-guide-language');
        if (savedLanguage && this.translations[savedLanguage]) {
            this.currentLanguage = savedLanguage;
        }
    }
}

// Global i18n instance
window.i18n = new I18n();
