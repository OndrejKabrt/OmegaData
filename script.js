

/*const formElement = document.querySelector('houseForm');
function sendForm(){
    
    const formData = {
        "pocet_pokoju": document.getElementById('pocet_pokoju').value,
        "kuchyne": document.getElementById('kuchyne').value,
        "plocha": document.getElementById('plocha').value,
        "gps_lat": document.getElementById('gps_lat').value,
        "gps_lon": document.getElementById('gps_lon').value,
        "rekonstuovano": document.getElementById('rekonstuovano').value,
        "parkovani": document.getElementById('parkovani').value,
        "sklep": document.getElementById('sklep').value
    };

    console.log(formData)
    
    fetch('https://127.0.0.1:65523/submit', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(formData)
    })
    .then(response => response.json())
    .then(data => console.log(data))
    .catch(error => console.log(error));
};*/

const formElement = document.querySelector('.houseForm');
formElement.addEventListener('submit', event => {
    event.preventDefault();

    const formData = {
        "Pocet_pokoju": document.getElementById('pocet_pokoju').value,
        "Kuchyne": document.getElementById('kuchyne').value,
        "Plocha": document.getElementById('plocha').value,
        "GPS_lat": document.getElementById('gps_lat').value,
        "GPS_lon": document.getElementById('gps_lon').value,
        "rekonstuovano": document.getElementById('rekonstuovano').value,
        "parkovani": document.getElementById('parkovani').value,
        "sklep": document.getElementById('sklep').value
    };

    

    //const data = Object.fromEntries(formData);
    console.log(formData);

    fetch('https://127.0.0.1:65523/api/predict', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(formData)
    })
    .then(response => response.json())
    .then(data => {
        console.log(data)
        document.getElementById('prediction').value=response;
    })
    .catch(error => console.log(error));
});