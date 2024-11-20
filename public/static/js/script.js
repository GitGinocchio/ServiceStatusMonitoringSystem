// Esempio di aggiornamento dinamico dello stato
const serverStatus = {
    google: "online",
    youtube: "partial",
    twitter: "offline",
    instagram: "online",
    twitch: "partial",
};

// Aggiorna le card in base allo stato
document.querySelectorAll(".card").forEach(card => {
    const serviceName = card.querySelector("h2").textContent.toLowerCase();
    if (serverStatus[serviceName]) {
        card.classList.add(serverStatus[serviceName]); // Aggiunge la classe dinamica
    }
});

/* 
async function updateStatus() {
    const response = await fetch('/api/status');
    const statuses = await response.json();

    document.querySelectorAll(".card").forEach(card => {
        const serviceName = card.querySelector("h2").textContent.toLowerCase();
        if (statuses[serviceName]) {
            card.className = `card ${statuses[serviceName].status}`; // Aggiorna lo stato
            const desc = card.querySelector('.desc p');
            desc.textContent = `Overall uptime: ${statuses[serviceName].uptime}% \n Average response time: ${statuses[serviceName].responseTime}ms`;
        }
    });
}

updateStatus();
*/