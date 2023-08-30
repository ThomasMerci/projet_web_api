function sendRequest(ville,cle) {
    return fetch('/api/message', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            ville: ville,
            cle:cle
        })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Erreur lors de l\'envoi des données');
        }
        return response.json();
    });
}

function updateUI(data) {
    const responseElement = document.getElementById('reponse');
    responseElement.innerHTML = `<p>${data.data}</p>`;

    const reponseDataVilleElement = document.getElementById('reponse_data_ville');

    if (Array.isArray(data.db_data)) {
        const cities = data.db_data.map(obj => obj.city).join(', '); 
        reponseDataVilleElement.innerHTML = `<p>Les 5 dernières villes : ${cities}</p>`;
    } else {
        reponseDataVilleElement.innerHTML = `<p> Les 5 dernières villes : ${data.db_data}</p>`;
    }
}
function city() {
    const ville = document.getElementById("ville").value || "Paris";
    const cle = document.getElementById("cle").value
    document.getElementById("ville").value = ville;
    document.getElementById("cle").value = cle;


    sendRequest(ville, cle)
        .then(data => {
            updateUI(data);
        })
        .catch(error => {
            console.error("Erreur:", error);
            alert("Une erreur s'est produite. Veuillez réessayer.");
        });
}

