// Initialize map when the page loads
document.addEventListener('DOMContentLoaded', function() {
    // Initialize map with Prague coordinates
    const map = L.map('map').setView([50.0471543, 14.0013247], 13);
    
    // Add map tiles
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);
    
    // Create marker and add to map
    let marker = L.marker([50.0471543, 14.0013247]).addTo(map)
        .bindPopup("<b>Byt je zde</b>")
        .openPopup();
    
    // When user clicks the map
    map.on('click', function(e) {
        // Update marker position
        marker.setLatLng(e.latlng);
        
        // Update hidden form fields with new coordinates
        document.getElementById('gps_lat').value = e.latlng.lat;
        document.getElementById('gps_lon').value = e.latlng.lng;
        
        // Update displayed coordinates
        document.getElementById('coordinates-display').textContent = 
            `${e.latlng.lat}, ${e.latlng.lng}`;
        
        // Open popup
        marker.openPopup();
    });
});