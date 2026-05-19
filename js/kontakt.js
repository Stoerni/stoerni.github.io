/* ==========================
   Kontaktformular Script
   Hier wird das Formular funktionsfähig gemacht und Emails versendet
   ========================== */

// 🔑 EmailJS einbinden - das ist ein Service, der kostenlos Emails versendet
// Der String ist die öffentliche API-ID von deinem EmailJS Account
emailjs.init("A4yI-KYfwkjWYSvV7");

// 📤 EXPORT: Diese Funktion wird von main.js aufgerufen
export function initContactForm() {

    // 🎯 HTML-Elemente für das Formular abrufen
    const kontakt_formular = document.querySelector(".kontakt_formular");
    if (!kontakt_formular) return; // 🛡 Sicherheitscheck: Wenn kein Formular, Script beenden

    // 🎯 Relevant Formular-Elemente
    const kontakt_button = document.querySelector(".kontakt_button");      // Der "Absenden" Button
    const kontakt_status = document.querySelector(".kontakt_status");      // Text, der nach Versand angezeigt wird
    const honeypot_feld = kontakt_formular.querySelector('input[name="website"]'); // Spam-Falle

    // 📝 Listener: Wenn das Formular gesendet wird (Submit-Event)
    kontakt_formular.addEventListener("submit", function (e) {
        // 🛑 Standardverhalten verhindern (normales Formular-Verhalten = Seite neu laden)
        e.preventDefault();

        // 🚨 HONEYPOT-ÜBERPRÜFUNG (Spam-Schutz!)
        // Honeypot = verstecktes Feld, das nur Bots sehen/ausfüllen können
        // Wenn ein Mensch das Formular ausfüllt, bleibt dieses Feld leer
        // Wenn ein Bot das Formular ausfüllt, denkt es, dass das Feld wichtig ist
        if (honeypot_feld && honeypot_feld.value !== "") {
            // 🤖 Spam erkannt! Einfach ignorieren und nichts machen
            return;
        }

        // 🔄 Button-Text ändern (visuelles Feedback dass etwas passiert)
        kontakt_button.textContent = "Sende...";
        // 🔒 Button disabled, damit Nutzer nicht zweimal klicken kann
        kontakt_button.disabled = true;

        // 🧹 Status-Text clearen (fall vom letzten Submit noch Text da ist)
        kontakt_status.textContent = "";
        kontakt_status.className = "kontakt_status";

        // 📨 EmailJS verwenden um Email zu versenden
        // 3 wichtige IDs aus deinem EmailJS Account:
        // - "service_e22dmlg" = dein Email-Service (wie Gmail, Outlook, etc.)
        // - "template_keeldnp" = die Email-Template (wie die Email aussieht)
        // - kontakt_formular = alle Formular-Daten werden automatisch in die Template eingebaut
        emailjs.sendForm(
            "service_e22dmlg",
            "template_keeldnp",
            kontakt_formular
        )
            // ✅ .then() = wenn Email erfolgreich versendet wurde
            .then(function () {
                // Erfolgs-Nachricht anzeigen
                kontakt_status.textContent = "Danke! Deine Nachricht wurde erfolgreich gesendet.";
                // CSS-Klasse "erfolg" hinzufügen (grüne Farbe in CSS)
                kontakt_status.classList.add("erfolg");

                // Formular leeren (so der Nutzer sieht, dass Nachricht angenommen wurde)
                kontakt_formular.reset();
            })
            // ❌ .catch() = wenn etwas schiefgeht (z.B. Internet weg, API-Fehler)
            .catch(function (error) {
                // Fehler-Nachricht anzeigen
                kontakt_status.textContent = "Ups! Etwas ist schiefgelaufen. Bitte versuche es später erneut.";
                // CSS-Klasse "fehler" hinzufügen (rote Farbe in CSS)
                kontakt_status.classList.add("fehler");

                // 🔍 Für Debugging: Fehler in Browser-Konsole ausgeben
                console.error("EmailJS Fehler:", error);
            })
            // 🔄 .finally() = egal ob Erfolg oder Fehler, das hier wird IMMER ausgeführt
            .finally(function () {
                // Button-Text zurücksetzen
                kontakt_button.textContent = "Absenden";
                // Button wieder aktivieren
                kontakt_button.disabled = false;
            });
    });
}