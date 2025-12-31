import React, { useEffect, useRef } from 'react';

const Confetti = ({ trigger }) => {
    const canvasRef = useRef(null);
    const requestRef = useRef();
    const piecesRef = useRef([]);

    useEffect(() => {
        if (!trigger) {
            piecesRef.current = [];
            return;
        }

        const canvas = canvasRef.current;
        const ctx = canvas.getContext("2d", { alpha: true });
        
        let w = window.innerWidth;
        let h = window.innerHeight;
        let dpr = Math.min(2, window.devicePixelRatio || 1);

        const resize = () => {
            w = window.innerWidth;
            h = window.innerHeight;
            canvas.width = Math.floor(w * dpr);
            canvas.height = Math.floor(h * dpr);
            canvas.style.width = w + "px";
            canvas.style.height = h + "px";
            ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
        };

        window.addEventListener("resize", resize);
        resize();

        const palette = [
            'rgb(255, 214, 102)', 
            'rgb(255, 107, 107)', 
            'rgb(116, 185, 255)', 
            'rgb(120, 224, 143)', 
            'rgb(235, 235, 235)'
        ];
        const COUNT = 500; // Balanced count for performance and density
        const GRAVITY = 0.35;

        const makePiece = () => {
            const angle = (Math.random() * 0.4 - 0.7) * Math.PI; // Upward cone (-0.5 is straight up)
            const power = Math.sqrt(h) * (Math.random() * 0.6 + 0.9) * 1.2;
            
            return {
                x: w / 2,
                y: h + 20,
                vx: Math.cos(angle) * power,
                vy: Math.sin(angle) * power,
                size: Math.random() * 8 + 4,
                color: palette[Math.floor(Math.random() * palette.length)],
                rotation: Math.random() * Math.PI * 2,
                vrot: (Math.random() - 0.5) * 0.3,
                flip: Math.random() * Math.PI * 2,
                vflip: Math.random() * 0.3 + 0.1,
                dead: false
            };
        };

        // Trigger a single massive burst
        piecesRef.current = Array.from({ length: COUNT }, makePiece);

        const loop = () => {
            ctx.clearRect(0, 0, w, h);
            let alive = 0;

            for (let i = 0; i < piecesRef.current.length; i++) {
                const p = piecesRef.current[i];
                if (p.dead) continue;
                alive++;

                p.x += p.vx;
                p.y += p.vy;
                p.vy += GRAVITY;
                p.rotation += p.vrot;
                p.flip += p.vflip;

                // Simple drag/friction
                p.vx *= 0.99;
                p.vy *= 0.99;

                if (p.y > h + 100 && p.vy > 0) {
                    p.dead = true;
                    continue;
                }

                ctx.save();
                ctx.translate(p.x, p.y);
                ctx.rotate(p.rotation);
                ctx.scale(Math.abs(Math.sin(p.flip)), 1);
                ctx.fillStyle = p.color;
                // Draw a simple rectangle (confetti piece)
                ctx.fillRect(-p.size / 2, -p.size / 2, p.size, p.size * 1.5);
                ctx.restore();
            }

            if (alive > 0) {
                requestRef.current = requestAnimationFrame(loop);
            }
        };

        requestRef.current = requestAnimationFrame(loop);

        return () => {
            window.removeEventListener("resize", resize);
            cancelAnimationFrame(requestRef.current);
        };
    }, [trigger]);

    return (
        <canvas
            ref={canvasRef}
            style={{
                position: 'fixed',
                top: 0,
                left: 0,
                width: '100vw',
                height: '100vh',
                pointerEvents: 'none',
                zIndex: 99999,
                opacity: trigger ? 1 : 0,
                transition: 'opacity 0.5s'
            }}
        />
    );
};

export default Confetti;
