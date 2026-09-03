const form = document.querySelector("#houseForm");
const messageBox = document.querySelector("#messageBox");

form.addEventListener("submit", (event) => {
    event.preventDefault();
    messageBox.innerHTML = "";

    const address = document.querySelector("#address").value.trim();
    const bedrooms = document.querySelector("#bedrooms").value.trim();
    const bedroomNum = Number(bedrooms);

    const message = document.createElement("p");

    if (!address || !bedrooms) {
        message.textContent = "Please fill in all required fields.";
        message.style.color = "red";
    } else if (bedroomNum <= 0 || isNaN(bedroomNum)) {
        message.textContent = "Bedrooms must be a positive number.";
        message.style.color = "red";
    } else {
        message.textContent = "Ready to submit";
        message.style.color = "green";
    }

    messageBox.appendChild(message);
});
