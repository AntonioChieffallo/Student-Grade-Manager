#!/bin/bash

# Student Grade Manager - Build Script
# This script compiles the C++ code to WebAssembly using Emscripten

set -e  # Exit on error

echo "🎓 Building Student Grade Manager WebAssembly Module..."

# Check if Emscripten is installed
if ! command -v emcc &> /dev/null; then
    echo "❌ Error: Emscripten (emcc) is not installed or not in PATH"
    echo "Please install Emscripten first:"
    echo "1. Download and install from: https://emscripten.org/docs/getting_started/downloads.html"
    echo "2. Run: source <emsdk_directory>/emsdk_env.sh"
    exit 1
fi

echo "✅ Emscripten found: $(emcc --version | head -n1)"

# Create build directory
echo "📁 Creating build directory..."
mkdir -p build
mkdir -p js

# Compile C++ to WebAssembly
echo "🔨 Compiling C++ to WebAssembly..."

emcc src/grade_manager.cpp \
    -o js/grade_manager.js \
    -s WASM=1 \
    -s EXPORTED_RUNTIME_METHODS='["ccall", "cwrap"]' \
    -s ALLOW_MEMORY_GROWTH=1 \
    -s MODULARIZE=1 \
    -s EXPORT_NAME="createGradeManagerModule" \
    -s USE_ES6_IMPORT_META=0 \
    -s ENVIRONMENT='web' \
    -s EXPORTED_FUNCTIONS='["_main"]' \
    --bind \
    -O3 \
    --closure 1 \
    -s ASSERTIONS=0 \
    -s DISABLE_EXCEPTION_CATCHING=1

# Check if compilation was successful
if [ $? -eq 0 ]; then
    echo "✅ Compilation successful!"
    echo "📦 Generated files:"
    echo "   - js/grade_manager.js (JavaScript glue code)"
    echo "   - js/grade_manager.wasm (WebAssembly binary)"
    
    # Display file sizes
    echo "📊 File sizes:"
    if [ -f "js/grade_manager.js" ]; then
        echo "   - grade_manager.js: $(du -h js/grade_manager.js | cut -f1)"
    fi
    if [ -f "js/grade_manager.wasm" ]; then
        echo "   - grade_manager.wasm: $(du -h js/grade_manager.wasm | cut -f1)"
    fi
    
    echo "🎉 Build completed successfully!"
    echo "🚀 You can now open index.html in a web browser"
    echo "   Note: Due to CORS restrictions, you may need to serve the files from a local web server"
    echo "   Quick server options:"
    echo "   - Python 3: python -m http.server 8000"
    echo "   - Python 2: python -m SimpleHTTPServer 8000"
    echo "   - Node.js: npx http-server"
    echo "   - PHP: php -S localhost:8000"
    
else
    echo "❌ Compilation failed!"
    exit 1
fi