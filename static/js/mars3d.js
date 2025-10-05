// --- 1. Basic Setup ---
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
const renderer = new THREE.WebGLRenderer({ antialias: true });

renderer.setSize(window.innerWidth, window.innerHeight);
document.body.appendChild(renderer.domElement);

// --- 2. Controls and Camera Position ---
const controls = new THREE.OrbitControls(camera, renderer.domElement);
camera.position.z = 2;

// --- 3. Lighting ---
const ambientLight = new THREE.AmbientLight(0xffffff, 0.5); // Soft white light
scene.add(ambientLight);

const pointLight = new THREE.PointLight(0xffffff, 1);
pointLight.position.set(5, 5, 5);
scene.add(pointLight);

// ------------------------------------------------------------------
// 🚀 4. Load Textures (Displacement Map Added) 🚀
// ------------------------------------------------------------------
const textureLoader = new THREE.TextureLoader();

// 1. Load the visible color texture (Original code, ensure file path is correct)
const marsTexture = textureLoader.load('static/maptextures/8k_mars.jpg'); 

// 2. Load the 4K Grayscale Displacement Map 
const displacementMap = textureLoader.load('static/maptextures/marsHeightMap.png');

// --- 5. Create the Mars Mesh (Sphere) ---

// ⚠️ IMPORTANT: Increase segments for better detail! 
// 256, 256 gives much better results with a 4K map than 64, 64.
const geometry = new THREE.SphereGeometry(1, 256, 256); 

const material = new THREE.MeshStandardMaterial({
    map: marsTexture,
    
    // -----------------------------------------------------
    // 🌟 DISPLACEMENT MAP CONFIGURATION 🌟
    // -----------------------------------------------------
    displacementMap: displacementMap, 
    
    // This value controls how "tall" the mountains are. 
    // Start with a small value relative to your radius (1).
    displacementScale: 0.08, 
    
    // Adjusts the overall position. Helps center the displaced mesh.
    displacementBias: 0.10, 
    // For Mars, we'll keep the bias 0.0 for now, but you can adjust it to 
    // center the planet if the entire sphere seems inflated.
});

const mars = new THREE.Mesh(geometry, material);
scene.add(mars);

// --- 6. Animation Loop ---
function animate() {
    requestAnimationFrame(animate);

    // Optional: slowly rotate the planet
    mars.rotation.y += 0.001; 

    controls.update(); // only required if controls.enableDamping is set to true
    renderer.render(scene, camera);
}

animate();

// --- 7. Handle Window Resize ---
window.addEventListener('resize', () => {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
});

//TIMELINE SCRIPT BELOWW!!
// 4. Initialization Script
    window.onload = function() {
        // Point the function to the Flask route that serves the JSON data
        var url = "{{ url_for('/marsTimelineData') }}"; 
        
        // Configuration Options (optional, but good for style)
        var options = {
          font: 'Default', // You can change this to a web font you've loaded
          hash_bookmark: true, // Allows deep-linking to specific events
          initial_zoom: 2,
          timenav_position: 'bottom'
        }

        // Create the timeline
        window.timeline = new TL.Timeline('timeline-embed', url, options);
    }
