// 📤 EXPORT: Diese Funktion wird von main.js aufgerufen
export function initTyping() {

    // 🔎 HTML-Elemente abrufen - diese müssen im HTML existieren
    
    // Element, in dem der animierte Text erscheint ("alt aber nicht veraltet", etc.)
    const typingElement = document.getElementById("typing_text");

    // Element, in dem das Bild angezeigt wird (olderbot-Bild)
    const imageElement = document.getElementById("typing_image");

    // Container für olderbot + Augen (Overlay) - wird später sichtbar/unsichtbar
    const imageWrapper = document.querySelector(".olderbot_container");

    // ❗ SICHERHEITSCHECK: Wenn eines der Elemente fehlt, Script stoppen
    // Das verhindert JavaScript-Fehler, wenn HTML falsch ist
    if (!typingElement || !imageElement) return;

    // 📝 Liste aller Wörter + dazugehörigen Bilder
    // Reihenfolge ist wichtig, wird nacheinander abgespielt
    const items = [
        { text: "alt aber nicht veraltet", image: "images/olderbot.webp" },  // Erstes Wort mit Bild (WebP = deutlich kleiner/schneller)
        { text: "Lösungsorientiert", image: null },                         // Zweites Wort (kein Bild)
        { text: "Analytisch", image: null },                               // Drittes Wort
        { text: "Strukturiert", image: null }                              // Viertes Wort
    ];

    // ⏱️ Geschwindigkeit & Pausen (alle Werte in Millisekunden)
    const typingSpeed = 90;          // Verzögerung zwischen jedem Buchstaben beim Schreiben (90ms)
    const deletingSpeed = 50;        // Verzögerung zwischen Buchstaben beim Löschen (schneller)
    const holdAfterTyping = 1400;    // Pause, nachdem Wort komplett geschrieben ist (1,4 Sekunden)
    const holdAfterDeleting = 300;   // Kleine Pause zwischen gelöschtem Wort und nächstem Wort

    // 📍 Status-Variablen - speichern den aktuellen Zustand der Animation
    let wordIndex = 0;    // Welches Wort aus der Liste ist aktuell aktiv (0, 1, 2, 3)
    let charIndex = 0;    // Welcher Buchstabe wird gerade angezeigt (0 bis Wort-Länge)
    let isDeleting = false; // Flag: Sind wir gerade im Schreib- oder Lösch-Modus?

    // 🖼️ Funktion: Bild einblenden mit sanifter Animation
    function showImage(src) {
        imageElement.src = src;              // Bildquelle setzen (z.B. "images/olderbot.png")
        imageWrapper.classList.add("show");  // CSS-Klasse hinzufügen → Bild wird sichtbar
        imageElement.classList.add("show");  // Auch das Bild selbst mit der "show"-Klasse markieren
        // CSS definiert dabei eine schöne Fade-In Animation mit opacity und transform
    }

    // 🖼️ Funktion: Bild ausblenden
    function hideImage() {
        imageWrapper.classList.remove("show");  // CSS-Klasse entfernen
        imageElement.classList.remove("show");  // Das blendet das Bild automatisch aus (CSS)
    }

    // 🔁 Hauptfunktion, die sich selbst wiederholt → erzeugt die Animation
    // setTimeout ruft diese Funktion immer wieder auf
    function typeLoop() {

        // 🎯 Aktuelles Wort + Bild aus der Liste holen
        // items[wordIndex] = das aktuelle Wort-Objekt
        const currentItem = items[wordIndex];
        // currentWord = der Text des Wortes (z.B. "alt aber nicht veraltet")
        const currentWord = currentItem.text;

        // ✍️ SCHREIBEN - wenn wir nicht gerade am Löschen sind
        if (!isDeleting) {

            // slice(0, charIndex + 1) = nimmt die ersten charIndex+1 Buchstaben
            // z.B. Buchstabe 0-3 = "alt" (a, l, t)
            typingElement.textContent = currentWord.slice(0, charIndex + 1);
            
            // charIndex++ = zum nächsten Buchstaben gehen
            // Das ist Kurzschreibweise für: charIndex = charIndex + 1
            charIndex++;

            // 🎯 Wenn das Wort komplett geschrieben ist
            // currentWord.length = Anzahl aller Buchstaben (z.B. 20 für "alt aber nicht veraltet")
            if (charIndex === currentWord.length) {

                // 🔑 Nur Bild anzeigen, wenn eins vorhanden ist (nicht null)
                if (currentItem.image) {
                    showImage(currentItem.image);
                }

                // ⏱️ Nach der langen Pause startet das Löschen
                // setTimeout = "führe das aus, nachdem holdAfterTyping Millisekunden vorbei sind"
                setTimeout(() => isDeleting = true, holdAfterTyping);
            }

            // 🧹 LÖSCHEN - Buchstabe für Buchstabe rückwärts entfernen
        } else {

            // Bild sofort ausblenden, sobald das Löschen BEGINNT
            // (nicht in jeder Iteration, sondern nur beim ersten Mal)
            if (charIndex === currentWord.length) {
                hideImage();
            }

            // slice(0, charIndex - 1) = nimmt die ersten charIndex-1 Buchstaben
            // Das löscht einen Buchstaben rückwärts
            typingElement.textContent = currentWord.slice(0, charIndex - 1);
            
            // charIndex-- = einen Schritt nach vorne (erinnere: wir gehen rückwärts)
            // Das ist Kurzschreibweise für: charIndex = charIndex - 1
            charIndex--;

            // 🎯 Wenn alles gelöscht ist (charIndex = 0)
            if (charIndex === 0) {
                isDeleting = false;                    // Wieder in Schreib-Modus wechseln
                
                // nächstes Wort auswählen (mit Modulo-Trick = Schleife)
                // % items.length = "wenn größer als Array, von vorne beginnen"
                // z.B. 4 % 4 = 0, 3 % 4 = 3
                wordIndex = (wordIndex + 1) % items.length;

                // ⏱️ Kleine Pause bevor neues Wort startet
                // Diese setTimeout ist eigentlich nicht nötig, da nextFrame aufgerufen wird
                setTimeout(() => { }, holdAfterDeleting);
            }
        }

        // ⏱️ Geschwindigkeit basierend auf Phase (Schreiben ist langsamer als Löschen)
        const speed = isDeleting ? deletingSpeed : typingSpeed;

        // 🔄 Rekursiver Aufruf: Funktion ruft sich selbst auf
        // Das ist die Basis der Animation - immer wieder, immer wieder...
        // Mit unterschiedlichen Verzögerungen (speed variable)
        setTimeout(typeLoop, speed);
    }

    // 🚀 Animation starten - typenLoop wird zum ersten Mal aufgerufen
    typeLoop();
}