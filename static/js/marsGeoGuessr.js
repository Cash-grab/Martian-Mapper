// --- Initialize the Mars map with Leaflet and Mars tile layer ---
var map = L.map('map', {
    center: [0, 0],
    zoom: 2,
    minZoom: 0,
    maxZoom: 5,
    crs: L.CRS.EPSG3857
});

// Add Mars basemap tiles from OpenPlanetaryMap
L.tileLayer('https://cartocdn-gusc.global.ssl.fastly.net/opmbuilder/api/v1/map/named/opm-mars-basemap-v0-2/all/{z}/{x}/{y}.png', {
    attribution: 'OpenPlanetaryMap, NASA/MOLA',
    maxZoom: 5,
    minZoom: 0,
    noWrap: true
}).addTo(map);

// --- Game State Variables ---
let actualCoords = null;     // The real location for the current round
let guessMarker = null;      // The user's guess marker
let answerMarker = null;     // The marker for the actual location
let guessLine = null;        // The line representing the guess

// --- Fetch a random Mars rover image and simulate coordinates ---
async function fetchRandomMarsImage() {
    const resp = await fetch('/api/random_mars_image');
    return await resp.json();
}

// --- Start a new game round ---
async function startRound() {
    document.getElementById('game-info').textContent = "Loading image Please be paitent!...";
    document.getElementById('next-round').style.display = "none";
    if (guessMarker) { map.removeLayer(guessMarker); }
    if (answerMarker) { map.removeLayer(answerMarker); }
    const result = await fetchRandomMarsImage();
    document.getElementById('mars-image').src = result.img;
    actualCoords = result.coords;
    document.getElementById('game-info').textContent = "Click on the map where you think this photo was taken!";
}

// --- Handle user guess on map click ---
map.on('click', function(e) {
    if (!actualCoords) return; // Prevent guessing if round is over
    if (guessMarker) { map.removeLayer(guessMarker); }
    guessMarker = L.marker(e.latlng, {title: "Your Guess"}).addTo(map);

    // Show the actual location with a custom icon
    answerMarker = L.marker(actualCoords, {title: "Actual Location", icon: L.icon({
        iconUrl: 'https://cdn-icons-png.flaticon.com/512/684/684908.png',
        iconSize: [32,32]
    })}).addTo(map);

    // Remove previous line if it exists
    if (guessLine) { map.removeLayer(guessLine); }

    // Draw a line between the guess and the actual location
    guessLine = L.polyline([e.latlng, actualCoords], {
        color: '#ffde59',
        weight: 4,
        opacity: 0.8,
        dashArray: '8, 8'
    }).addTo(map);

    // Calculate rough distance in degrees (for demo purposes)
    const dist = Math.sqrt(
        Math.pow(e.latlng.lat - actualCoords.lat, 2) +
        Math.pow(e.latlng.lng - actualCoords.lng, 2)
    );

    // Display results to the user
    document.getElementById('game-info').innerHTML = `
        <b>Your guess:</b> (${e.latlng.lat.toFixed(2)}, ${e.latlng.lng.toFixed(2)})<br>
        <b>Actual location:</b> (${actualCoords.lat.toFixed(2)}, ${actualCoords.lng.toFixed(2)})<br>
        <b>Distance:</b> ${dist.toFixed(2)} degrees
    `;
    document.getElementById('next-round').style.display = "inline-block";
    actualCoords = null; // Prevent multiple guesses per round
});

// --- Next round button handler ---

document.getElementById('next-round').onclick = startRound;




function makeDraggable(element, dragHandle) {
  let pos1 = 0, pos2 = 0, pos3 = 0, pos4 = 0;

  if (dragHandle) {
    // If a drag handle is provided, listen for mousedown on the handle
    dragHandle.onmousedown = dragMouseDown;
  } else {
    // Otherwise, the entire element is draggable
    element.onmousedown = dragMouseDown;
  }

  function dragMouseDown(e) {
    e = e || window.event;
    e.preventDefault(); // Prevent default browser drag behavior

    // Get the mouse cursor position at startup
    pos3 = e.clientX;
    pos4 = e.clientY;

    document.onmouseup = closeDragElement; // Stop dragging when mouse button is released
    document.onmousemove = elementDrag;   // Call a function whenever the cursor moves
  }

  function elementDrag(e) {
    e = e || window.event;
    e.preventDefault();

    // Calculate the new cursor position
    pos1 = pos3 - e.clientX;
    pos2 = pos4 - e.clientY;
    pos3 = e.clientX;
    pos4 = e.clientY;

    // Set the element's new position
    element.style.top = (element.offsetTop - pos2) + "px";
    element.style.left = (element.offsetLeft - pos1) + "px";
  }

  function closeDragElement() {
    // Stop moving when mouse button is released
    document.onmouseup = null;
    document.onmousemove = null;
  }
}

// Get the draggable div and its header
const draggableDiv = document.getElementById("gameUI");
const draggableDivHeader = document.getElementById("gameUIHeader");

// Make the div draggable using its header as the handle
makeDraggable(draggableDiv, draggableDivHeader);















// --- Start the first round when the page loads ---
startRound();
