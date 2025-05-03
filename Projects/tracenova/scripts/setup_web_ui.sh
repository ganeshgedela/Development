#!/bin/bash

set -e

PROJECT_NAME="web_ui"

echo "🔧 Cleaning existing project..."
rm -rf $PROJECT_NAME

echo "🚀 Creating new Vite + React + TS project..."
npm create vite@latest $PROJECT_NAME -- --template react-ts
cd $PROJECT_NAME

echo "📦 Installing base dependencies..."
npm install

echo "🎨 Installing Tailwind CSS..."
npm install -D tailwindcss@3.4.1 postcss@8.4.38 autoprefixer@10.4.19

echo "⚙️ Initializing Tailwind config..."
npx tailwindcss init -p || ./node_modules/.bin/tailwindcss init -p

echo "🛠️ Updating tailwind.config.js..."
cat > tailwind.config.js <<EOL
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}"
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
EOL

echo "🎨 Adding Tailwind directives to src/index.css..."
cat > src/index.css <<EOL
@tailwind base;
@tailwind components;
@tailwind utilities;
EOL

echo "✅ Tailwind CSS setup complete!"
echo "Run with: cd $PROJECT_NAME && npm run dev"
