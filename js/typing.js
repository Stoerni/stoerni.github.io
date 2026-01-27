export function initTyping() {

    // 🔎 HTML-Elemente abrufen
    // Element, in dem der animierte Text erscheint
    const typingElement = document.getElementById("typing_text");

    // Element, in dem das Bild angezeigt wird
    const imageElement = document.getElementById("typing_image");

    // Container für T800 + Augen (Overlay)
    const imageWrapper = document.querySelector(".t800_container");

    // ❗ Sicherheitscheck: Wenn eines der Elemente fehlt, Script stoppen
    if (!typingElement || !imageElement) return;

    // 📝 Liste aller Wörter + dazugehörigen Bilder
    // Reihenfolge ist wichtig, wird nacheinander abgespielt
    const items = [
        { text: "alt aber nicht veraltet", image: "images/olderbot.png" },
        { text: "Lösungsorientiert", image: null },
        { text: "Analytisch", image: null },
        { text: "Strukturiert", image: null }
    ];

    // ⏱️ Geschwindigkeit & Pausen (ms)
    const typingSpeed = 90;          // Zeit zwischen jedem Buchstaben beim Schreiben
    const deletingSpeed = 50;        // Zeit zwischen Buchstaben beim Löschen
    const holdAfterTyping = 1400;    // Pause, nachdem Wort komplett geschrieben ist (Bild sichtbar)
    const holdAfterDeleting = 300;   // Kleine Pause zwischen gelöschtem Wort und nächstem Wort

    // 📍 Statusvariablen
    let wordIndex = 0;    // Welches Wort aktuell aktiv ist
    let charIndex = 0;    // Welcher Buchstabe gerade angezeigt wird
    let isDeleting = false; // Flag: Schreiben oder Löschen

    // 🖼️ Funktion: Bild einblenden
    function showImage(src) {
        imageElement.src = src;            // Bildquelle setzen
        imageWrapper.classList.add("show");   // 🔥 Container aktivieren → Augen reagieren
        imageElement.classList.add("show"); // Klasse für CSS-Fade-In Animation
    }

    // 🖼️ Funktion: Bild ausblenden
    function hideImage() {
        imageWrapper.classList.remove("show"); // Augen aus
        imageElement.classList.remove("show"); // Klasse entfernen → CSS blendet aus
    }

    // 🔁 Hauptfunktion, die sich selbst wiederholt → erzeugt Animation
    function typeLoop() {

        // Aktuelles Wort + Bild aus der Liste holen
        const currentItem = items[wordIndex];
        const currentWord = currentItem.text;

        // ✍️ SCHREIBEN
        if (!isDeleting) {

            // Text wird Buchstabe für Buchstabe angezeigt
            typingElement.textContent = currentWord.slice(0, charIndex + 1);
            charIndex++; // zum nächsten Buchstaben gehen

            // Wenn das Wort komplett geschrieben ist
            if (charIndex === currentWord.length) {

                // 🔑 Nur Bild anzeigen, wenn eins vorhanden ist
                if (currentItem.image) {
                    showImage(currentItem.image);
                }

                // Nach der Pause startet das Löschen
                setTimeout(() => isDeleting = true, holdAfterTyping);
            }

            // 🧹 LÖSCHEN (Schreibmaschinen-Effekt)
        } else {

            // Bild sofort ausblenden, sobald das Löschen beginnt
            if (charIndex === currentWord.length) {
                hideImage();
            }

            // Text Buchstabe für Buchstabe löschen
            typingElement.textContent = currentWord.slice(0, charIndex - 1);
            charIndex--; // Rückwärts gehen

            // Wenn alles gelöscht ist → nächstes Wort
            if (charIndex === 0) {
                isDeleting = false; // wieder in Schreibmodus
                wordIndex = (wordIndex + 1) % items.length; // nächstes Wort (modulo = Schleife)

                // kleine Pause bevor neues Wort startet
                setTimeout(() => { }, holdAfterDeleting);
            }
        }

        // Geschwindigkeit anpassen je nach Phase
        const speed = isDeleting ? deletingSpeed : typingSpeed;

        // Rekursiver Aufruf → Animation läuft weiter
        setTimeout(typeLoop, speed);
    }

    // 🚀 Animation starten
    typeLoop();
}