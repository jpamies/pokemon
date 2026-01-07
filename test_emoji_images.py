#!/usr/bin/env python3
"""Prueba de emojis como imágenes con ReportLab"""
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor
import os

def test_emoji_images():
    """Prueba insertar emojis como imágenes pequeñas"""
    
    # Crear PDF
    c = canvas.Canvas('test_emoji_images.pdf', pagesize=A4)
    width, height = A4
    
    # Título
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 50, "Prueba de Emojis como Imágenes")
    
    y = height - 100
    
    # Probar diferentes emojis
    emoji_tests = [
        ('fire.png', 'Fuego', '#FF6B35'),
        ('water.png', 'Agua', '#4A90E2'),
        ('electric.png', 'Eléctrico', '#F8D030'),
        ('grass.png', 'Planta', '#7AC142')
    ]
    
    for emoji_file, type_name, color in emoji_tests:
        emoji_path = f'emoji_icons/{emoji_file}'
        
        if os.path.exists(emoji_path):
            # Dibujar badge de tipo (similar al actual)
            c.setFillColor(HexColor(color))
            c.roundRect(50, y, 100, 20, 5, fill=1)
            
            # Insertar emoji como imagen pequeña
            try:
                c.drawImage(emoji_path, 55, y + 2, width=16, height=16)
                print(f"✅ Emoji insertado: {emoji_file}")
            except Exception as e:
                print(f"❌ Error con {emoji_file}: {e}")
            
            # Texto del tipo
            c.setFillColor(HexColor('#ffffff'))
            c.setFont("Helvetica-Bold", 10)
            c.drawString(75, y + 6, type_name)
            
        else:
            print(f"❌ No encontrado: {emoji_path}")
        
        y -= 30
    
    c.save()
    print("✅ PDF generado: test_emoji_images.pdf")

if __name__ == "__main__":
    test_emoji_images()
