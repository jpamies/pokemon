/**
 * Pokemon Cache System for Web Application
 * Shares cache with Python PDF generator
 */

class PokemonCache {
    constructor() {
        this.cachePrefix = 'pokemon_cache_';
        this.imageCachePrefix = 'pokemon_image_';
    }

    /**
     * Get cached Pokemon data
     */
    getPokemonData(pokemonId) {
        try {
            const cached = localStorage.getItem(this.cachePrefix + pokemonId);
            return cached ? JSON.parse(cached) : null;
        } catch (e) {
            console.warn('Error reading Pokemon cache:', e);
            return null;
        }
    }

    /**
     * Cache Pokemon data
     */
    setPokemonData(pokemonId, data) {
        try {
            localStorage.setItem(this.cachePrefix + pokemonId, JSON.stringify(data));
        } catch (e) {
            console.warn('Error saving Pokemon cache:', e);
        }
    }

    /**
     * Get cached image URL (base64 or blob URL)
     */
    getCachedImage(imageUrl) {
        try {
            const hash = this.hashString(imageUrl);
            return localStorage.getItem(this.imageCachePrefix + hash);
        } catch (e) {
            console.warn('Error reading image cache:', e);
            return null;
        }
    }

    /**
     * Cache image as base64
     */
    async setCachedImage(imageUrl, imageElement) {
        try {
            const hash = this.hashString(imageUrl);
            
            // Convert image to base64
            const canvas = document.createElement('canvas');
            const ctx = canvas.getContext('2d');
            canvas.width = imageElement.naturalWidth;
            canvas.height = imageElement.naturalHeight;
            ctx.drawImage(imageElement, 0, 0);
            
            const base64 = canvas.toDataURL('image/png');
            localStorage.setItem(this.imageCachePrefix + hash, base64);
        } catch (e) {
            console.warn('Error caching image:', e);
        }
    }

    /**
     * Simple hash function for URLs
     */
    hashString(str) {
        let hash = 0;
        for (let i = 0; i < str.length; i++) {
            const char = str.charCodeAt(i);
            hash = ((hash << 5) - hash) + char;
            hash = hash & hash; // Convert to 32-bit integer
        }
        return Math.abs(hash).toString(16);
    }

    /**
     * Clear all cache
     */
    clearCache() {
        const keys = Object.keys(localStorage);
        keys.forEach(key => {
            if (key.startsWith(this.cachePrefix) || key.startsWith(this.imageCachePrefix)) {
                localStorage.removeItem(key);
            }
        });
    }

    /**
     * Get cache size info
     */
    getCacheInfo() {
        const keys = Object.keys(localStorage);
        let dataCount = 0;
        let imageCount = 0;
        
        keys.forEach(key => {
            if (key.startsWith(this.cachePrefix)) dataCount++;
            if (key.startsWith(this.imageCachePrefix)) imageCount++;
        });
        
        return { dataCount, imageCount };
    }
}

// Export for use in other modules
window.PokemonCache = PokemonCache;
