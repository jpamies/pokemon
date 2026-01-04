#!/bin/bash

# Deploy script for Pokemon Guide GitHub Pages
echo "🚀 Deploying Pokemon Guide to GitHub Pages..."

# Check if we're in a git repository
if [ ! -d ".git" ]; then
    echo "❌ Not in a git repository. Initializing..."
    git init
    git remote add origin https://github.com/jordipb/pokeAPI.git
fi

# Add all files
echo "📁 Adding files..."
git add .

# Commit changes
echo "💾 Committing changes..."
git commit -m "🎉 Deploy Pokemon Guide v3.0.0 with Catalan PDFs

✨ Features:
- 📚 Complete Pokemon PDFs in Catalan (Gen I-V)
- 🌍 Professional translations by Kiro AI
- 🎨 Horizontal card design with colors
- 📱 GitHub Pages hosting
- 🔄 Multiple sorting options (ID & Color)

📊 Stats:
- 649 Pokemon translated (Gen I-V)
- 10 PDFs generated
- Responsive landing page
- Ready for GitHub Pages deployment"

# Push to GitHub
echo "🌐 Pushing to GitHub..."
git branch -M main
git push -u origin main

echo "✅ Deployment complete!"
echo ""
echo "🎯 Your Pokemon Guide is now available at:"
echo "   📱 Web App: https://jordipb.github.io/pokeAPI/"
echo "   📚 PDFs: https://jordipb.github.io/pokeAPI/docs/"
echo ""
echo "📋 Next steps:"
echo "   1. Enable GitHub Pages in repository settings"
echo "   2. Set source to 'Deploy from a branch'"
echo "   3. Select 'main' branch and '/ (root)' folder"
echo "   4. Wait 5-10 minutes for deployment"
echo ""
echo "🎉 Happy Pokemon learning!"
