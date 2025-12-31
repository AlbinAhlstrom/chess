import React, { useEffect, useRef } from 'react';

const Confetti = ({ trigger }) => {
    const canvasRef = useRef(null);
    const requestRef = useRef();
    const piecesRef = useRef([]);
    const mxRef = useRef(0);

    useEffect(() => {
        if (!trigger) return;

        const canvas = canvasRef.current;
        const ctx = canvas.getContext("2d", { alpha: true });
        const COUNT = 1100;
        const SPEED = 1.2; // Adjusted for physics-based loop
        const GRAVITY = 0.15;
        const palette = [
            [255, 214, 102], [255, 107, 107], [116, 185, 255], [120, 224, 143], [235, 235, 235]
        ];
        const spriteCache = new Map();

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

        const handlePointerMove = (e) => {
            mxRef.current = (e.clientX / w) * 2 - 1;
        };

        window.addEventListener("resize", resize);
        window.addEventListener("pointermove", handlePointerMove);
        resize();

        const rand = (a, b) => a + Math.random() * (b - a);
        const pick = (arr) => arr[(Math.random() * arr.length) | 0];

        const makeSprite = (r, g, b, bw, bh, blur) => {
            const pad = blur ? Math.ceil(blur * 3 + 6) : 2;
            const c = document.createElement("canvas");
            c.width = bw + pad * 2;
            c.height = bh + pad * 2;
            const cctx = c.getContext("2d");
            if (blur) {
                cctx.shadowColor = `rgb(${r},${g},${b})`;
                cctx.shadowBlur = blur;
            }
            cctx.fillStyle = `rgb(${r},${g},${b})`;
            cctx.fillRect(pad, pad, bw, bh);
            const dots = Math.max(18, Math.floor((bw * bh) / 9));
            for (let i = 0; i < dots; i++) {
                const x = (pad + Math.random() * bw) | 0;
                const y = (pad + Math.random() * bh) | 0;
                const v = (Math.random() * 60 - 30) | 0;
                const rr = Math.max(0, Math.min(255, r + v));
                const gg = Math.max(0, Math.min(255, g + v));
                const bb = Math.max(0, Math.min(255, b + v));
                cctx.globalAlpha = 0.14 + Math.random() * 0.26;
                cctx.fillStyle = `rgb(${rr},${gg},${bb})`;
                cctx.fillRect(x, y, 1, 1);
            }
            return { img: c, ox: pad + bw / 2, oy: pad + bh / 2 };
        };

        const getSprite = (r, g, b, bw, bh, blur) => {
            const key = `${r},${g},${b}|${bw}x${bh}|${blur}`;
            if (spriteCache.has(key)) return spriteCache.get(key);
            const spr = makeSprite(r, g, b, bw, bh, blur);
            spriteCache.set(key, spr);
            return spr;
        };

        const makePiece = () => {
            const z = Math.random();
            const layer = z < 0.5 ? 0 : z < 0.85 ? 1 : 2;
            const hero = layer === 2 && Math.random() < 0.35;
            const ultra = layer === 2 && Math.random() < 0.05;
            const floaty = Math.random() < 0.22;
            const base = layer === 0 ? rand(2, 4) : layer === 1 ? rand(4, 7) : ultra ? rand(34, 55) : hero ? rand(18, 28) : rand(12, 20);
            
            // Start at bottom center
            const x = w / 2 + rand(-20, 20);
            const y = h + 50;

            // Upward burst velocity with cone spread
            // Angle between -70 and -110 degrees (upwards)
            const angle = rand(-Math.PI * 0.4, -Math.PI * 0.6); 
            // Velocity to reach top of screen: v^2 = 2gh. For h=h, v = sqrt(2*0.15*h)
            const power = Math.sqrt(2 * GRAVITY * h) * rand(0.9, 1.2);
            
            const vx = Math.cos(angle) * power;
            const vy = Math.sin(angle) * power;

            const rgb = pick(palette);
            const r = Math.round(rgb[0] * 0.72), g = Math.round(rgb[1] * 0.72), b = Math.round(rgb[2] * 0.72);
            const aspect = floaty ? rand(1.15, 1.75) : rand(1.0, 1.55);
            const bw = Math.max(2, Math.round(base * rand(0.85, 1.25))), bh = Math.max(3, Math.round(bw * aspect));
            const flipSpeed = rand(0.02, 0.2);
            const blur = ultra ? 3 : 0;

            return { 
                x, y, vx, vy, 
                layer, hero, ultra, floaty, 
                spr: getSprite(r, g, b, bw, bh, blur), 
                rot: rand(0, Math.PI * 2), 
                vr: rand(-0.1, 0.1), 
                sway: rand(0, Math.PI * 2), 
                swaySpeed: rand(0.01, 0.05), 
                drift: rand(0.5, 2), 
                flip: rand(0, Math.PI * 2), 
                flipSpeed, 
                dead: false 
            };
        };

        // Create initial burst
        piecesRef.current = Array.from({ length: COUNT }, () => makePiece());

        let last = performance.now();

        const loop = (now) => {
            const dt = Math.min(0.033, (now - last) / 1000) * 60; // Normalize to ~60fps
            last = now;
            ctx.clearRect(0, 0, w, h);
            
            const wind = mxRef.current * 0.5;

            let aliveCount = 0;
            for (let i = 0; i < piecesRef.current.length; i++) {
                const p = piecesRef.current[i];
                if (p.dead) continue;
                aliveCount++;

                // Physics
                p.vy += GRAVITY * dt;
                p.vx += wind * dt;
                
                // Air resistance / Drift
                p.vx *= Math.pow(0.99, dt);
                
                p.x += p.vx * dt * SPEED;
                p.y += p.vy * dt * SPEED;
                
                p.rot += p.vr * dt;
                p.flip += p.flipSpeed * dt;
                p.sway += p.swaySpeed * dt;

                // Lateral sway
                const swayX = Math.sin(p.sway) * p.drift;
                
                if (p.y > h + 100 && p.vy > 0) {
                    p.dead = true;
                }

                ctx.save();
                ctx.translate(p.x + swayX, p.y);
                ctx.rotate(p.rot);
                ctx.scale(Math.abs(Math.sin(p.flip)), 1);
                ctx.globalAlpha = p.layer === 0 ? 0.2 : p.layer === 1 ? 0.5 : p.ultra ? 0.95 : 0.8;
                ctx.drawImage(p.spr.img, -p.spr.ox, -p.spr.oy);
                ctx.restore();
            }

            if (aliveCount > 0) {
                requestRef.current = requestAnimationFrame(loop);
            }
        };

        requestRef.current = requestAnimationFrame(loop);

        return () => {
            window.removeEventListener("resize", resize);
            window.removeEventListener("pointermove", handlePointerMove);
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