# Student Grade Manager - Makefile
# Build system for compiling C++ to WebAssembly

# Compiler and flags
EMCC = emcc
SRC_DIR = src
BUILD_DIR = build
JS_DIR = js
TARGET = $(JS_DIR)/grade_manager

# Source files
SOURCES = $(SRC_DIR)/grade_manager.cpp

# Emscripten compilation flags
EMCC_FLAGS = -s WASM=1 \
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

# Default target
all: check-emcc build

# Check if Emscripten is available
check-emcc:
	@echo "🔍 Checking for Emscripten..."
	@which $(EMCC) > /dev/null || (echo "❌ Error: Emscripten not found. Please install Emscripten and run 'source emsdk_env.sh'" && exit 1)
	@echo "✅ Emscripten found: $$($(EMCC) --version | head -n1)"

# Create necessary directories
$(JS_DIR):
	@echo "📁 Creating directories..."
	@mkdir -p $(JS_DIR)
	@mkdir -p $(BUILD_DIR)

# Build target
build: $(JS_DIR) $(TARGET).js

$(TARGET).js: $(SOURCES)
	@echo "🔨 Compiling C++ to WebAssembly..."
	$(EMCC) $(SOURCES) -o $(TARGET).js $(EMCC_FLAGS)
	@echo "✅ Build completed successfully!"
	@echo "Generated files:"
	@echo "  - $(TARGET).js"
	@echo "  - $(TARGET).wasm"

# Clean build artifacts
clean:
	@echo "🧹 Cleaning build artifacts..."
	@rm -rf $(BUILD_DIR)
	@rm -f $(JS_DIR)/grade_manager.js $(JS_DIR)/grade_manager.wasm
	@echo "✅ Clean completed"

# Development build (with debug symbols)
debug: EMCC_FLAGS = -s WASM=1 \
					-s EXPORTED_RUNTIME_METHODS='["ccall", "cwrap"]' \
					-s ALLOW_MEMORY_GROWTH=1 \
					-s MODULARIZE=1 \
					-s EXPORT_NAME="createGradeManagerModule" \
					-s USE_ES6_IMPORT_META=0 \
					-s ENVIRONMENT='web' \
					-s EXPORTED_FUNCTIONS='["_main"]' \
					--bind \
					-O0 \
					-g \
					-s ASSERTIONS=1 \
					-s SAFE_HEAP=1
debug: build
	@echo "🐛 Debug build completed with debugging symbols"

# Install dependencies (if using npm for development server)
install:
	@echo "📦 Installing development dependencies..."
	@npm init -y > /dev/null 2>&1 || true
	@npm install --save-dev http-server > /dev/null 2>&1 || echo "Optional: install http-server globally with 'npm install -g http-server'"

# Serve the application locally
serve:
	@echo "🚀 Starting development server..."
	@echo "Open http://localhost:8000 in your browser"
	@which http-server > /dev/null && http-server -p 8000 || \
	which python3 > /dev/null && python3 -m http.server 8000 || \
	which python > /dev/null && python -m SimpleHTTPServer 8000 || \
	echo "No suitable server found. Please install http-server or Python"

# Help target
help:
	@echo "📖 Student Grade Manager - Build Help"
	@echo ""
	@echo "Available targets:"
	@echo "  all (default) - Build the WebAssembly module"
	@echo "  build         - Build the WebAssembly module"
	@echo "  debug         - Build with debug symbols"
	@echo "  clean         - Remove build artifacts"
	@echo "  serve         - Start a local development server"
	@echo "  install       - Install development dependencies"
	@echo "  help          - Show this help message"
	@echo ""
	@echo "Requirements:"
	@echo "  - Emscripten SDK installed and activated"
	@echo "  - Run 'source <emsdk_path>/emsdk_env.sh' before building"

.PHONY: all build debug clean serve install help check-emcc