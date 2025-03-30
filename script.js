document.getElementById('realEstateForm').addEventListener('submit', function(event) {
    event.preventDefault();
    
    const formData = {
        pocet_pokoju: document.getElementById('pocet_pokoju').value,
        kuchyne: document.getElementById('kuchyne').value,
        plocha: document.getElementById('plocha').value,
        gps_lat: document.getElementById('gps_lat').value,
        gps_lon: document.getElementById('gps_lon').value,
        rekonstuovano: document.getElementById('rekonstuovano').value,
        parkovani: document.getElementById('parkovani').value,
        sklep: document.getElementById('sklep').value
    };
    
    fetch('https://api.example.com/submit', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(formData)
    })
    .then(response => response.json())
    .then(data => alert('Data byla úspěšně odeslána!'))
    .catch(error => alert('Chyba při odesílání dat.'));
});
