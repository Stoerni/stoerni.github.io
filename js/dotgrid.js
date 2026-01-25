/* =====================
    DOTGRID ANIMATION
===================== */
export function initDotGrid() {
    const canvas = document.getElementById('dotCanvas');
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    const spacing = 24;   // Abstand zwischen Punkten
    const radius = 4;   // Größe der Punkte
    const points = [];
    const waves = [];

    // Dotgrid Farben (einfach anpassen)
    const dotColor = 'rgba(255,255,255,0.2)';
    const hoverColor = 'rgba(255,0,0,0.9)';

    // Canvas-Größe anpassen
    function resizeCanvas() {
        canvas.width = canvas.offsetWidth;
        canvas.height = canvas.offsetHeight;
        createPoints();
    }

    // Initial + bei Resize
    window.addEventListener('resize', resizeCanvas);
    resizeCanvas();

    let mouse = { x: -1000, y: -1000 };

    // Punkte erzeugen
    function createPoints() {
        points.length = 0;
        for (let y = spacing; y < canvas.height; y += spacing) {
            for (let x = spacing; x < canvas.width; x += spacing) {
                points.push({ x, y });
            }
        }
    }

    // Mausbewegung
    canvas.addEventListener('mousemove', (e) => {
        const rect = canvas.getBoundingClientRect();
        mouse.x = e.clientX - rect.left;
        mouse.y = e.clientY - rect.top;
    });

    // Maus verlässt Canvas
    canvas.addEventListener('mouseleave', () => {
        mouse.x = -1000;
        mouse.y = -1000;
    });

    // Klick → neue Welle
    canvas.addEventListener('click', (e) => {
        const rect = canvas.getBoundingClientRect();

        waves.push({
            x: e.clientX - rect.left,
            y: e.clientY - rect.top,
            time: 0,
            life: 1
        });
    });

    // Animation
    function animate() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        // nächsten Punkt zur Maus bestimmen (für exakten Hover)
        let closestPoint = null;
        let closestDistance = Infinity;

        for (const p of points) {
            const d = Math.hypot(mouse.x - p.x, mouse.y - p.y);
            if (d < closestDistance) {
                closestDistance = d;
                closestPoint = p;
            }
        }

        // Wellen-Zeit erhöhen
        for (const wave of waves) {
            wave.time += 0.15;
            wave.life -= 0.01; // Fade-Out-Geschwindigkeit (kleiner Wert = länger sichtbar großer Wert = kürzer sichtbar)
        }

        // Punkte zeichnen
        for (const p of points) {
            // Hover-Farbe
            let color = dotColor;
            if (p === closestPoint && closestDistance < spacing / 2) {
                color = hoverColor;
            }

            // Wellen-Offset (Summe aller Wellen)
            let waveOffset = 0;

            for (const wave of waves) {
                const d = Math.hypot(p.x - wave.x, p.y - wave.y);
                const falloff = Math.max(0, 1 - d / 300);

                const amplitude = 6 * wave.life; // sanftes Ausklingen

                waveOffset +=
                    Math.sin(d * 0.05 - wave.time) *
                    amplitude *
                    falloff;
            }

            ctx.beginPath();
            ctx.arc(p.x, p.y + waveOffset, radius, 0, Math.PI * 2);
            ctx.fillStyle = color;
            ctx.fill();
        }

        // Alte Wellen entfernen
        for (let i = waves.length - 1; i >= 0; i--) {
            if (waves[i].life <= 0) {
                waves.splice(i, 1);
            }
        }

        requestAnimationFrame(animate);
    }
    window.addEventListener('resize', resizeCanvas);
    resizeCanvas();
    animate();
}