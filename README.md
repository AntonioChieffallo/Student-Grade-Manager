# 🎓 Student Grade Manager

A modern web application for managing student grades and calculating GPA, built with C++ WebAssembly backend and HTML/CSS/JavaScript frontend.

## ✨ Features

- **📚 Course Management**: Add and remove courses with credit hours
- **📊 Grade Tracking**: Input grades for each course (0-100 scale)
- **🎯 GPA Calculation**: Automatic GPA calculation using standard 4.0 scale
- **📱 Responsive Design**: Modern, mobile-friendly interface
- **⚡ High Performance**: C++ backend compiled to WebAssembly for fast calculations
- **🚀 Easy Deployment**: Ready for GitHub Pages deployment

## 🏗️ Architecture

This application uses a unique architecture combining:

- **Backend**: C++ code compiled to WebAssembly using Emscripten
- **Frontend**: HTML5, CSS3, and vanilla JavaScript
- **Integration**: JavaScript bindings to communicate with WASM module

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   HTML/CSS      │    │   JavaScript     │    │   C++ (WASM)    │
│   User Interface│◄──►│   Glue Code      │◄──►│   Grade Logic   │
│                 │    │                  │    │                 │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

## 🚀 Quick Start

### Prerequisites

1. **Emscripten SDK** (for building the WebAssembly module)
   ```bash
   # Install Emscripten
   git clone https://github.com/emscripten-core/emsdk.git
   cd emsdk
   ./emsdk install latest
   ./emsdk activate latest
   source ./emsdk_env.sh
   ```

2. **Web Server** (for local development)
   - Python: `python -m http.server 8000`
   - Node.js: `npx http-server`
   - Any other local web server

### Building the Application

#### Option 1: Using the Build Script
```bash
# Make the script executable
chmod +x build.sh

# Build the WebAssembly module
./build.sh
```

#### Option 2: Using Make
```bash
# Build the application
make

# Or build with debug symbols
make debug

# Start development server
make serve
```

#### Option 3: Manual Build
```bash
# Create directories
mkdir -p js build

# Compile C++ to WebAssembly
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
    -O3
```

### Running the Application

1. **Build the WebAssembly module** (see above)
2. **Start a local web server** in the project directory
3. **Open** `http://localhost:8000` in your browser

> **Note**: Due to CORS restrictions, you cannot open `index.html` directly in the browser. You must serve it through a web server.

## 📁 Project Structure

```
Student-Grade-Manager/
├── src/
│   └── grade_manager.cpp      # C++ backend logic
├── js/
│   ├── app.js                 # Frontend JavaScript application
│   ├── grade_manager.js       # WebAssembly loader (generated)
│   └── grade_manager.wasm     # WebAssembly binary (generated)
├── index.html                 # Main HTML interface
├── styles.css                 # CSS styles
├── build.sh                   # Build script
├── Makefile                   # Alternative build system
└── README.md                  # This file
```

## 🎮 Usage

### Adding Courses
1. Enter course name (e.g., "Math 101")
2. Enter credit hours (1-6)
3. Click "Add Course"

### Adding Grades
1. Select a course from the dropdown
2. Enter grade (0-100)
3. Click "Add Grade"

### Viewing Results
- **GPA** is automatically calculated and displayed
- **Course averages** are shown for each course
- **Letter grades** are displayed using standard scale

### Managing Data
- **Remove courses** individually using the remove button
- **Clear all data** using the "Clear All Data" button
- **Refresh** the interface using the "Refresh Data" button

## 🎯 Grading Scale

The application uses the standard 4.0 GPA scale:

| Letter Grade | GPA Points | Percentage Range |
|--------------|------------|------------------|
| A+           | 4.0        | 97-100           |
| A            | 3.7        | 93-96            |
| A-           | 3.3        | 90-92            |
| B+           | 3.0        | 87-89            |
| B            | 2.7        | 83-86            |
| B-           | 2.3        | 80-82            |
| C+           | 2.0        | 77-79            |
| C            | 1.7        | 73-76            |
| C-           | 1.3        | 70-72            |
| D+           | 1.0        | 67-69            |
| D            | 0.7        | 65-66            |
| F            | 0.0        | 0-64             |

## 🌐 GitHub Pages Deployment

### Automatic Deployment

1. **Push your code** to the `main` branch
2. **Go to repository Settings** → Pages
3. **Select source**: Deploy from a branch
4. **Choose branch**: `main` / `root`
5. **Save** and wait for deployment

### Manual Deployment

1. **Build the project** locally:
   ```bash
   ./build.sh
   ```

2. **Commit the generated files**:
   ```bash
   git add js/grade_manager.js js/grade_manager.wasm
   git commit -m "Add WebAssembly build artifacts"
   git push origin main
   ```

3. **Enable GitHub Pages** in repository settings

### GitHub Actions (Optional)

Create `.github/workflows/build-and-deploy.yml`:

```yaml
name: Build and Deploy to GitHub Pages

on:
  push:
    branches: [ main ]

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest
    
    steps:
    - name: Checkout
      uses: actions/checkout@v3
      
    - name: Setup Emscripten
      uses: mymindstorm/setup-emsdk@v11
      
    - name: Build WebAssembly
      run: |
        ./build.sh
        
    - name: Deploy to GitHub Pages
      uses: peaceiris/actions-gh-pages@v3
      with:
        github_token: ${{ secrets.GITHUB_TOKEN }}
        publish_dir: ./
```

## 🛠️ Development

### Mock Mode

For development without Emscripten, you can use the JavaScript fallback:

```
http://localhost:8000/?mock=true
```

This uses a pure JavaScript implementation for testing the UI.

### Debug Build

Build with debugging symbols and assertions:

```bash
make debug
```

### Development Server

Start a local development server:

```bash
make serve
# or
python -m http.server 8000
# or  
npx http-server
```

## 🧪 Testing

The application includes built-in error handling and validation:

- **Input validation** for grades (0-100) and credits (1-6)
- **Course name validation** (non-empty strings)
- **WebAssembly availability detection**
- **Fallback to JavaScript implementation** when WASM is unavailable

## 🔧 Troubleshooting

### Common Issues

1. **"WebAssembly module not loaded"**
   - Ensure you've built the WASM module: `./build.sh`
   - Check that `js/grade_manager.js` and `js/grade_manager.wasm` exist
   - Use a web server, not file:// protocol

2. **"Emscripten not found"**
   - Install Emscripten SDK
   - Run `source <emsdk_path>/emsdk_env.sh`

3. **CORS errors**
   - Use a local web server instead of opening files directly
   - Check browser console for specific error messages

4. **Build fails**
   - Ensure Emscripten is properly installed and activated
   - Check that all source files exist
   - Try a debug build: `make debug`

### Browser Compatibility

- **Chrome/Edge**: Full support
- **Firefox**: Full support  
- **Safari**: Full support (Safari 11+)
- **Mobile browsers**: Responsive design works on all modern mobile browsers

## 📚 Educational Value

This project demonstrates:

- **WebAssembly integration** with C++ and JavaScript
- **Modern web development** with vanilla JavaScript
- **Responsive design** principles
- **Build systems** and deployment automation
- **Software architecture** with clear separation of concerns

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🙏 Acknowledgments

- **Emscripten team** for the amazing WebAssembly compiler
- **Web standards community** for modern web APIs
- **Educational institutions** that inspire tools like this

---

**Happy Learning! 🎓**
