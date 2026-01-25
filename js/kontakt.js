/* ==========================
   Kontaktformular Script
   ========================== */

// EmailJS einbinden
emailjs.init("A4yI-KYfwkjWYSvV7");

export function initContactForm() {

    const kontakt_formular = document.querySelector(".kontakt_formular");
    if (!kontakt_formular) return; // 🛡 Schutz vor JS-Fehlern

    const kontakt_button = document.querySelector(".kontakt_button");
    const kontakt_status = document.querySelector(".kontakt_status");
    const honeypot_feld = kontakt_formular.querySelector('input[name="website"]');

    kontakt_formular.addEventListener("submit", function (e) {
        e.preventDefault();

        // Honeypot-Überprüfung vor dem Senden um Spam zu verhindern
        if (honeypot_feld && honeypot_feld.value !== "") {
            return;
        }

        kontakt_button.textContent = "Sende...";
        kontakt_button.disabled = true;

        kontakt_status.textContent = "";
        kontakt_status.className = "kontakt_status";

        emailjs.sendForm(
            "service_e22dmlg",
            "template_keeldnp",
            kontakt_formular   // stabiler als "this"
        )
            .then(function () {
                kontakt_status.textContent = "Danke! Deine Nachricht wurde erfolgreich gesendet.";
                kontakt_status.classList.add("erfolg");

                kontakt_formular.reset();
            })
            .catch(function (error) {
                kontakt_status.textContent = "Ups! Etwas ist schiefgelaufen. Bitte versuche es später erneut.";
                kontakt_status.classList.add("fehler");

                console.error("EmailJS Fehler:", error);
            })
            .finally(function () {
                kontakt_button.textContent = "Absenden";
                kontakt_button.disabled = false;
            });
    });
}