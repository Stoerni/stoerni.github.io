/* =====================
    DOTGRID ANIMATION - Interaktive Punkt-Wellen
    Das ist eine Canvas-Animation, die Punkte zeigt und auf Mausklicks reagiert
===================== */

// 📤 EXPORT: Diese Funktion wird von main.js aufgerufen
export function initDotGrid() {
    // 🎯 Canvas-Element abrufen (das HTML5 Zeichnungs-Canvas für Punkte)
    const canvas = document.getElementById('dotCanvas');
    
    // 🛡️ SICHERHEITSCHECK: Wenn kein Canvas da ist, beende die Funktion
    if (!canvas) return;

    // 🎨 Canvas 2D-Kontext: Mit diesem Objekt zeichnen wir auf dem Canvas
    const ctx = canvas.getContext('2d');
    
    // ⚙️ KONFIGURATION - Werte, die du einfach anfassen kannst:
    const spacing = 24;   // 24 Pixel Abstand zwischen den Punkten
    const radius = 4;     // Radius = Größe der Punkte (4 Pixel)
    const points = [];    // Array für alle Punkte (wird später gefüllt)
    const waves = [];     // Array für Wellen (wenn der Nutzer klickt)

    // 🎨 FARBEN
    const dotColor = 'rgba(255,255,255,0.2)';  // Normale Punkte: Weiß, aber sehr transparent (0.2)
    const hoverColor = 'rgba(255,0,0,0.9)';    // Hover-Farbe: Rot und fast vollständig sichtbar

    // 📐 Funktion: Canvas-Größe an Fenster anpassen (responsiv)
    function resizeCanvas() {
        // Canvas-Breite = tatsächliche Fenster-Breite des Canvas
        canvas.width = canvas.offsetWidth;
        // Canvas-Höhe = tatsächliche Fenster-Höhe des Canvas
        canvas.height = canvas.offsetHeight;
        // Punkte nach Resize neu erzeugen
        createPoints();
    }

    // 🔄 Listener: Wenn Fenster größer/kleiner wird, neu zeichnen
    window.addEventListener('resize', resizeCanvas);
    
    // 🚀 Canvas beim Start einmal dimensionieren
    resizeCanvas();

    // 🖱️ Maus-Koordinaten speichern (für Hover-Effekt)
    let mouse = { x: -1000, y: -1000 };  // Start außerhalb des sichtbaren Bereichs

    // 📍 Funktion: Alle Punkte auf dem Canvas erzeugen
    function createPoints() {
        // Array leeren (falls es alte Punkte gibt)
        points.length = 0;
        
        // Verschachtelte Schleifen: Jede Reihe und jede Spalte
        for (let y = spacing; y < canvas.height; y += spacing) {
            // y++ bedeutet: y = y + spacing (einfach schneller geschrieben)
            for (let x = spacing; x < canvas.width; x += spacing) {
                // Jeden Punkt als Objekt speichern mit x und y Koordinaten
                points.push({ x, y });  // { x, y } ist Kurzschreibweise für { x: x, y: y }
            }
        }
    }

    // 🖱️ Listener: Mausbewegung auf dem Canvas
    canvas.addEventListener('mousemove', (e) => {
        // getBoundingClientRect = aktuelle Position des Canvas im Fenster
        const rect = canvas.getBoundingClientRect();
        
        // Maus-Position relativ zum Canvas (nicht zum ganzen Fenster)
        mouse.x = e.clientX - rect.left;      // Fenster-X minus Canvas-links = Canvas-X
        mouse.y = e.clientY - rect.top;       // Fenster-Y minus Canvas-oben = Canvas-Y
    });

    // 🖱️ Listener: Maus verlässt Canvas (zurücksetzen)
    canvas.addEventListener('mouseleave', () => {
        // Maus-Position weit weg setzen (außerhalb des Canvas)
        mouse.x = -1000;
        mouse.y = -1000;
    });

    // 🖱️ Listener: Maus-Klick erzeugt eine Welle
    canvas.addEventListener('click', (e) => {
        // Wiederum: Klick-Position relativ zum Canvas berechnen
        const rect = canvas.getBoundingClientRect();
        
        // Neue Welle ins Array hinzufügen
        waves.push({
            x: e.clientX - rect.left,      // Klick-X Position
            y: e.clientY - rect.top,       // Klick-Y Position
            time: 0,                       // Wellen-Animation startet bei 0
            life: 1                        // Wellen-"Leben": 1 = volles Leben, 0 = tot
        });
    });

    // 🎬 Hauptfunktion: Die Animation läuft kontinuierlich
    function animate() {
        // 🧹 Canvas komplett löschen (schwarzer Hintergrund)
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        // 🎯 Nächsten Punkt zur Maus bestimmen (für exakten Hover)
        // Warum? Weil Punkte zu groß sind, um alle separat zu prüfen
        let closestPoint = null;           // Am nächsten gelegener Punkt
        let closestDistance = Infinity;    // Unendlich große Distanz zum Start

        // Jede Punkt durchgehen
        for (const p of points) {
            // 📏 Distanz berechnen: Pythagoras-Satz
            // Math.hypot = Hypotenuse = Distanz zwischen zwei Punkten
            const d = Math.hypot(mouse.x - p.x, mouse.y - p.y);
            
            // Wenn dieser Punkt näher ist als der bisherige nächste
            if (d < closestDistance) {
                closestDistance = d;  // Neue "kleinste Distanz" speichern
                closestPoint = p;     // Dieser Punkt ist jetzt am nächsten
            }
        }

        // 🌊 Wellen aktualisieren
        for (const wave of waves) {
            // Zeit der Welle erhöhen (für Animation)
            wave.time += 0.15;
            
            // Leben der Welle vermindern (Wellen verblassen)
            // 0.01 = kleine Verblassungs-Geschwindigkeit (Welle bleibt lange sichtbar)
            // Größere Zahl = schneller weg; Kleinere Zahl = länger sichtbar
            wave.life -= 0.01;
        }

        // 🔵 ALLE PUNKTE ZEICHNEN
        for (const p of points) {
            // 🎨 Standard-Farbe setzen (transparentes Weiß)
            let color = dotColor;
            
            // 🔴 Hover-Check: Ist die Maus nah genug dran?
            // spacing / 2 = Radius um den Punkt, in dem Hover aktiv ist
            if (p === closestPoint && closestDistance < spacing / 2) {
                color = hoverColor;  // Farbe auf Rot wechseln
            }

            // 🌊 Wellen-Offset berechnen (wie viel sich dieser Punkt bewegt)
            let waveOffset = 0;

            // Für JEDE aktive Welle:
            for (const wave of waves) {
                // 📏 Distanz von diesem Punkt zur Wellen-Quelle
                const d = Math.hypot(p.x - wave.x, p.y - wave.y);
                
                // 📉 Falloff = wie schwach die Welle wird, je weiter weg
                // Math.max = größere Zahl von zwei Werten (verhindert negative Zahlen)
                // Je weiter weg, desto näher an 0
                const falloff = Math.max(0, 1 - d / 300);

                // 🌊 Amplitude = wie hoch die Welle ist (schwindend mit der Zeit)
                // wave.life = je älter die Welle, desto niedriger
                const amplitude = 6 * wave.life;

                // 🧮 Sinus-Welle berechnen (für wellenförmige Bewegung)
                // Math.sin = macht eine sanfte Wellen-Kurve
                // d * 0.05 = räumliche Frequenz (wie oft die Welle schwingt)
                // - wave.time = Zeit-Versatz (macht Animation)
                waveOffset +=
                    Math.sin(d * 0.05 - wave.time) *  // Sinus-Welle
                    amplitude *                        // Amplitude (Höhe)
                    falloff;                          // Falloff (Abschwächung)
            }

            // 🎨 PUNKT ZEICHNEN
            ctx.beginPath();                          // Neuen Zeichnungs-Pfad starten
            ctx.arc(p.x, p.y + waveOffset, radius, 0, Math.PI * 2); // Kreis
            // p.x, p.y + waveOffset = Mittelpunkt (y wird durch Welle verschoben)
            // radius = Größe des Kreises
            // 0, Math.PI * 2 = Kompletter Kreis (0° bis 360°)
            
            ctx.fillStyle = color;                    // Farbe anwenden
            ctx.fill();                               // Kreis ausfüllen
        }

        // 🧹 Alte, tote Wellen entfernen (räume auf)
        // Rückwärtsschleife, weil wir während der Iteration löschen
        for (let i = waves.length - 1; i >= 0; i--) {
            // Wenn Welle ist dead (life <= 0)
            if (waves[i].life <= 0) {
                waves.splice(i, 1);  // splice = 1 Element ab Index i löschen
            }
        }

        // 🔄 Nächsten Frame anfordern (60 FPS Animation)
        // requestAnimationFrame = "zeichne den nächsten Frame so schnell wie möglich"
        requestAnimationFrame(animate);
    }
    
    // 🔄 Listener: Bei Fenster-Resize auch aktualisieren
    window.addEventListener('resize', resizeCanvas);
    
    // 🚀 Canvas initial setup
    resizeCanvas();
    
    // 🎬 Animation starten
    animate();
}