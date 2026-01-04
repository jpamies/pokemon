const PDFDocument = require('pdfkit');
const fs = require('fs');
const https = require('https');

// Create PDF directory if it doesn't exist
if (!fs.existsSync('./pdf')) {
    fs.mkdirSync('./pdf');
}

// Pokemon data structure
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
    'flying': '🦅',
    'psychic': '🔮',
    'bug': '🐛',
    'rock': '🗿',
    'ghost': '👻',
    'dragon': '🐉',
    'dark': '🌙',
    'steel': '⚙️',
    'fairy': '🧚'
};

const typeColors = {
    'normal': '#A8A878',
    'fire': '#F08030',
    'water': '#6890F0',
    'electric': '#F8D030',
    'grass': '#78C850',
    'ice': '#98D8D8',
    'fighting': '#C03028',
    'poison': '#A040A0',
    'ground': '#E0C068',
    'flying': '#A890F0',
    'psychic': '#F85888',
    'bug': '#A8B820',
    'rock': '#B8A038',
    'ghost': '#705898',
    'dragon': '#7038F8',
    'dark': '#705848',
    'steel': '#B8B8D0',
    'fairy': '#EE99AC'
};

async function fetchPokemon(id) {
    return new Promise((resolve, reject) => {
        https.get(`https://pokeapi.co/api/v2/pokemon/${id}`, (res) => {
            let data = '';
            res.on('data', chunk => data += chunk);
            res.on('end', () => {
                try {
                    const pokemon = JSON.parse(data);
                    resolve({
                        id: pokemon.id,
                        name: pokemon.name,
                        height: pokemon.height,
                        weight: pokemon.weight,
                        types: pokemon.types.map(t => t.type.name),
                        image: pokemon.sprites.front_default
                    });
                } catch (error) {
                    reject(error);
                }
            });
        }).on('error', reject);
    });
}

async function downloadImage(url) {
    return new Promise((resolve, reject) => {
        if (!url) {
            resolve(null);
            return;
        }
        
        https.get(url, (res) => {
            const chunks = [];
            res.on('data', chunk => chunks.push(chunk));
            res.on('end', () => resolve(Buffer.concat(chunks)));
        }).on('error', reject);
    });
}

function getGenerationFromId(id) {
    if (id <= 151) return 'Gen I - Kanto';
    if (id <= 251) return 'Gen II - Johto';
    if (id <= 386) return 'Gen III - Hoenn';
    if (id <= 493) return 'Gen IV - Sinnoh';
    if (id <= 649) return 'Gen V - Unova';
    if (id <= 721) return 'Gen VI - Kalos';
    if (id <= 809) return 'Gen VII - Alola';
    if (id <= 905) return 'Gen VIII - Galar';
    return 'Gen IX - Paldea';
}

async function generatePDF() {
    console.log('Generating Pokemon PDF...');
    
    const doc = new PDFDocument({ 
        layout: 'landscape',
        size: 'A4',
        margins: { top: 20, bottom: 20, left: 20, right: 20 }
    });
    
    const stream = fs.createWriteStream('./pdf/pokemon-guide-sample.pdf');
    doc.pipe(stream);
    
    // Title
    doc.fontSize(24)
       .fillColor('#e74c3c')
       .text('Guia Pokémon per a Nens', { align: 'center' });
    
    doc.fontSize(14)
       .fillColor('#7f8c8d')
       .text('Primeros 20 Pokémon - Versión de Prueba', { align: 'center' });
    
    doc.moveDown(2);
    
    const cardWidth = 180;
    const cardHeight = 240;
    const cardsPerRow = 4;
    const marginX = 20;
    const marginY = 100;
    const spacingX = 10;
    const spacingY = 15;
    
    for (let i = 1; i <= 20; i++) {
        console.log(`Processing Pokemon #${i}...`);
        
        try {
            const pokemon = await fetchPokemon(i);
            const imageBuffer = await downloadImage(pokemon.image);
            
            const row = Math.floor((i - 1) / cardsPerRow);
            const col = (i - 1) % cardsPerRow;
            
            const x = marginX + col * (cardWidth + spacingX);
            const y = marginY + row * (cardHeight + spacingY);
            
            // Check if we need a new page
            if (y + cardHeight > doc.page.height - 20) {
                doc.addPage();
                const newRow = Math.floor((i - 1) / cardsPerRow) % 2;
                const newY = marginY + newRow * (cardHeight + spacingY);
                
                // Recalculate position for new page
                drawPokemonCard(doc, pokemon, imageBuffer, x, newY, cardWidth, cardHeight);
            } else {
                drawPokemonCard(doc, pokemon, imageBuffer, x, y, cardWidth, cardHeight);
            }
            
        } catch (error) {
            console.error(`Error processing Pokemon #${i}:`, error);
        }
    }
    
    doc.end();
    
    stream.on('finish', () => {
        console.log('PDF generated successfully: ./pdf/pokemon-guide-sample.pdf');
    });
}

function drawPokemonCard(doc, pokemon, imageBuffer, x, y, width, height) {
    // Card border
    doc.rect(x, y, width, height)
       .strokeColor('#e74c3c')
       .lineWidth(2)
       .stroke();
    
    // Pokemon image
    if (imageBuffer) {
        try {
            doc.image(imageBuffer, x + 10, y + 10, { width: 80, height: 80 });
        } catch (error) {
            console.log(`Could not add image for ${pokemon.name}`);
        }
    }
    
    // Pokemon number and name
    doc.fontSize(16)
       .fillColor('#2c3e50')
       .font('Helvetica-Bold')
       .text(`#${pokemon.id.toString().padStart(3, '0')}`, x + 100, y + 15);
    
    doc.fontSize(14)
       .text(pokemon.name.toUpperCase(), x + 100, y + 35);
    
    // Types with colors
    let typeY = y + 60;
    pokemon.types.forEach((type, index) => {
        const typeColor = typeColors[type] || '#95a5a6';
        const typeIcon = typeIcons[type] || '❓';
        
        doc.rect(x + 100 + (index * 70), typeY, 65, 20)
           .fillColor(typeColor)
           .fill();
        
        doc.fontSize(10)
           .fillColor('white')
           .font('Helvetica-Bold')
           .text(`${typeIcon} ${type.toUpperCase()}`, x + 102 + (index * 70), typeY + 5);
    });
    
    // Stats
    doc.fontSize(10)
       .fillColor('#34495e')
       .font('Helvetica')
       .text(`Altura: ${(pokemon.height / 10).toFixed(1)} m`, x + 10, y + 100)
       .text(`Peso: ${(pokemon.weight / 10).toFixed(1)} kg`, x + 10, y + 115)
       .text(getGenerationFromId(pokemon.id), x + 10, y + 130);
}

// Run the generator
generatePDF().catch(console.error);
