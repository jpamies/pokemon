// Simple language management for docs
class DocsI18n {
    constructor() {
        this.currentLanguage = 'ca';
        this.translations = {
            ca: {
                title: '📚 Centre de Descàrregues',
                subtitle: 'Guies Pokémon Educatives Multiidioma',
                statsTitle: '📊 Estadístiques del Projecte',
                backLink: '🏠 Tornar a l\'Aplicació',
                githubLink: '🐙 GitHub',
                stats: {
                    pdfs: 'PDFs Generats',
                    pokemon: 'Pokémon Complets',
                    languages: 'Idiomes',
                    generations: 'Generacions'
                },
                generations: [
                    { title: '🔴 Generació I - Kanto', desc: '151 Pokémon de la regió de Kanto (Bulbasaur - Mew)' },
                    { title: '🟡 Generació II - Johto', desc: '100 Pokémon de la regió de Johto (Chikorita - Celebi)' },
                    { title: '🟢 Generació III - Hoenn', desc: '135 Pokémon de la regió de Hoenn (Treecko - Deoxys)' },
                    { title: '🔵 Generació IV - Sinnoh', desc: '107 Pokémon de la regió de Sinnoh (Turtwig - Arceus)' },
                    { title: '⚫ Generació V - Unova', desc: '156 Pokémon de la regió d\'Unova (Snivy - Genesect)' },
                    { title: '🟣 Generació VI - Kalos', desc: '72 Pokémon de la regió de Kalos (Chespin - Volcanion)' },
                    { title: '🟠 Generació VII - Alola', desc: '88 Pokémon de la regió d\'Alola (Rowlet - Melmetal)' },
                    { title: '🔴 Generació VIII - Galar', desc: '96 Pokémon de la regió de Galar (Grookey - Enamorus)' },
                    { title: '🟡 Generació IX - Paldea', desc: '120 Pokémon de la regió de Paldea (Sprigatito - Pecharunt)' }
                ],
                buttons: { byId: 'Per ID', byColor: 'Per Color' }
            },
            es: {
                title: '📚 Centro de Descargas',
                subtitle: 'Guías Pokémon Educativas Multiidioma',
                statsTitle: '📊 Estadísticas del Proyecto',
                backLink: '🏠 Volver a la Aplicación',
                githubLink: '🐙 GitHub',
                stats: {
                    pdfs: 'PDFs Generados',
                    pokemon: 'Pokémon Completos',
                    languages: 'Idiomas',
                    generations: 'Generaciones'
                },
                generations: [
                    { title: '🔴 Generación I - Kanto', desc: '151 Pokémon de la región de Kanto (Bulbasaur - Mew)' },
                    { title: '🟡 Generación II - Johto', desc: '100 Pokémon de la región de Johto (Chikorita - Celebi)' },
                    { title: '🟢 Generación III - Hoenn', desc: '135 Pokémon de la región de Hoenn (Treecko - Deoxys)' },
                    { title: '🔵 Generación IV - Sinnoh', desc: '107 Pokémon de la región de Sinnoh (Turtwig - Arceus)' },
                    { title: '⚫ Generación V - Unova', desc: '156 Pokémon de la región de Unova (Snivy - Genesect)' },
                    { title: '🟣 Generación VI - Kalos', desc: '72 Pokémon de la región de Kalos (Chespin - Volcanion)' },
                    { title: '🟠 Generación VII - Alola', desc: '88 Pokémon de la región de Alola (Rowlet - Melmetal)' },
                    { title: '🔴 Generación VIII - Galar', desc: '96 Pokémon de la región de Galar (Grookey - Enamorus)' },
                    { title: '🟡 Generación IX - Paldea', desc: '120 Pokémon de la región de Paldea (Sprigatito - Pecharunt)' }
                ],
                buttons: { byId: 'Por ID', byColor: 'Por Color' }
            },
            en: {
                title: '📚 Download Center',
                subtitle: 'Multilingual Educational Pokémon Guides',
                statsTitle: '📊 Project Statistics',
                backLink: '🏠 Back to Application',
                githubLink: '🐙 GitHub',
                stats: {
                    pdfs: 'Generated PDFs',
                    pokemon: 'Complete Pokémon',
                    languages: 'Languages',
                    generations: 'Generations'
                },
                generations: [
                    { title: '🔴 Generation I - Kanto', desc: '151 Pokémon from the Kanto region (Bulbasaur - Mew)' },
                    { title: '🟡 Generation II - Johto', desc: '100 Pokémon from the Johto region (Chikorita - Celebi)' },
                    { title: '🟢 Generation III - Hoenn', desc: '135 Pokémon from the Hoenn region (Treecko - Deoxys)' },
                    { title: '🔵 Generation IV - Sinnoh', desc: '107 Pokémon from the Sinnoh region (Turtwig - Arceus)' },
                    { title: '⚫ Generation V - Unova', desc: '156 Pokémon from the Unova region (Snivy - Genesect)' },
                    { title: '🟣 Generation VI - Kalos', desc: '72 Pokémon from the Kalos region (Chespin - Volcanion)' },
                    { title: '🟠 Generation VII - Alola', desc: '88 Pokémon from the Alola region (Rowlet - Melmetal)' },
                    { title: '🔴 Generation VIII - Galar', desc: '96 Pokémon from the Galar region (Grookey - Enamorus)' },
                    { title: '🟡 Generation IX - Paldea', desc: '120 Pokémon from the Paldea region (Sprigatito - Pecharunt)' }
                ],
                buttons: { byId: 'By ID', byColor: 'By Color' }
            }
        };
        
        this.init();
    }
    
    init() {
        // Get language from URL or localStorage
        const urlParams = new URLSearchParams(window.location.search);
        const urlLang = urlParams.get('lang');
        
        if (urlLang && ['ca', 'es', 'en'].includes(urlLang)) {
            this.currentLanguage = urlLang;
        } else {
            const storedLang = localStorage.getItem('pokemon-guide-language');
            if (storedLang && ['ca', 'es', 'en'].includes(storedLang)) {
                this.currentLanguage = storedLang;
            }
        }
        
        this.updateContent();
        this.setupLanguageButtons();
    }
    
    setLanguage(lang) {
        this.currentLanguage = lang;
        localStorage.setItem('pokemon-guide-language', lang);
        this.updateContent();
        this.updateLanguageButtons();
    }
    
    updateContent() {
        const t = this.translations[this.currentLanguage];
        
        // Update title and subtitle
        document.querySelector('.docs-title').textContent = t.title;
        document.querySelector('.docs-subtitle').textContent = t.subtitle;
        document.querySelector('.stats h3').textContent = t.statsTitle;
        
        // Update links
        const backLinks = document.querySelectorAll('.back-link');
        backLinks[0].innerHTML = t.backLink;
        backLinks[1].innerHTML = t.githubLink;
        
        // Update stats labels
        const statItems = document.querySelectorAll('.stat-item span:last-child');
        statItems[0].textContent = t.stats.pdfs;
        statItems[1].textContent = t.stats.pokemon;
        statItems[2].textContent = t.stats.languages;
        statItems[3].textContent = t.stats.generations;
        
        // Update generation cards
        const cards = document.querySelectorAll('.pdf-card');
        const langSuffix = this.currentLanguage === 'ca' ? '' : `_${this.currentLanguage}`;
        const generations = ['i_kanto', 'ii_johto', 'iii_hoenn', 'iv_sinnoh', 'v_unova', 'vi_kalos', 'vii_alola', 'viii_galar', 'ix_paldea'];
        
        cards.forEach((card, index) => {
            if (t.generations[index]) {
                card.querySelector('.pdf-title').textContent = t.generations[index].title;
                card.querySelector('.pdf-description').textContent = t.generations[index].desc;
                
                const links = card.querySelectorAll('.pdf-link');
                if (links[0]) {
                    links[0].innerHTML = `📥 ${t.buttons.byId}`;
                    links[0].href = `pdf/${generations[index]}_by_id${langSuffix}.pdf`;
                }
                if (links[1]) {
                    links[1].innerHTML = `🎨 ${t.buttons.byColor}`;
                    links[1].href = `pdf/${generations[index]}_by_color${langSuffix}.pdf`;
                }
            }
        });
        
        // Update complete guides links
        const completeByIdLink = document.querySelector('.complete-by-id');
        const completeByColorLink = document.querySelector('.complete-by-color');
        if (completeByIdLink) {
            completeByIdLink.href = `pdf/pokemon_complet${langSuffix}.pdf`;
        }
        if (completeByColorLink) {
            completeByColorLink.href = `pdf/pokemon_complet${langSuffix}_by_color.pdf`;
        }
        
        // Update document language
        document.documentElement.lang = this.currentLanguage;
    }
    
    setupLanguageButtons() {
        document.querySelectorAll('.lang-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                e.preventDefault();
                const lang = btn.dataset.lang;
                this.setLanguage(lang);
            });
        });
        
        this.updateLanguageButtons();
    }
    
    updateLanguageButtons() {
        document.querySelectorAll('.lang-btn').forEach(btn => {
            btn.classList.toggle('active', btn.dataset.lang === this.currentLanguage);
        });
    }
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new DocsI18n();
});
