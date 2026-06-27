document.addEventListener('DOMContentLoaded', () => {
    
    // --- CHANGED THIS LINE ---
    // Centered on the world map [20, 0] with a zoom level of 2 (fully zoomed out)
    var map = L.map('map').setView([20.0, 0.0], 2);

    L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
    }).addTo(map);

    setTimeout(() => { 
        map.invalidateSize(); 
    }, 400);

    let currentMarker = null;
    const guessBtn = document.getElementById('guess-btn');
    const resultBox = document.getElementById('result-box');

    map.on('click', function(e) {
        if (currentMarker) {
            map.removeLayer(currentMarker);
        }
        currentMarker = L.marker(e.latlng).addTo(map);
        guessBtn.disabled = false;
        
        resultBox.style.display = 'none';
        resultBox.className = '';
    });

    guessBtn.addEventListener('click', async () => {
        if (!currentMarker) return;

        const position = currentMarker.getLatLng();
        guessBtn.disabled = true;
        resultBox.style.display = 'block';
        resultBox.className = 'verifying';
        resultBox.innerHTML = 'Verifying coordinates...';

        try {
            const response = await fetch('/api/guess', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ lat: position.lat, lng: position.lng })
            });

            const data = await response.json();

            resultBox.className = '';

            if (data.success) {
                resultBox.classList.add('result-success');
                resultBox.innerHTML = `<div class="status-title">TARGET ACQUIRED</div><span class="flag-text">${data.flag}</span>`;
            } else {
                resultBox.classList.add('result-error');
                resultBox.innerHTML = `<div class="status-title">MISSION FAILED</div><div class="status-msg">${data.message}</div>`;
                guessBtn.disabled = false; 
            }
        } catch (error) {
            resultBox.className = 'result-error';
            resultBox.innerHTML = 'Server connection failed.';
            guessBtn.disabled = false;
        }
    });
});
