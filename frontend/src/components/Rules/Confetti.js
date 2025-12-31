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
        const SPEED = 20.75;
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

        const makePiece = (init) => {
            const z = Math.random();
            const layer = z < 0.5 ? 0 : z < 0.85 ? 1 : 2;
            const hero = layer === 2 && Math.random() < 0.35;
            const ultra = layer === 2 && Math.random() < 0.05;
            const floaty = Math.random() < 0.22;
            const insaneFlip = Math.random() < 0.06;
            const fastFlip = !insaneFlip && Math.random() < 0.22;
            const base = layer === 0 ? rand(2, 4) : layer === 1 ? rand(4, 7) : ultra ? rand(34, 55) : hero ? rand(18, 28) : rand(12, 20);
            const x = rand(-140, w + 140);
            // Starting position: init pieces scattered, new pieces always from top
            const y = init ? rand(-h, h) : rand(-260, -60); 
            const vy = layer === 0 ? rand(0.35, 0.85) : layer === 1 ? rand(0.7, 1.35) : rand(1.05, 2.0);
            const vx = layer === 0 ? rand(0.1, 0.28) : layer === 1 ? rand(0.16, 0.42) : rand(0.22, 0.62);
            const rgb = pick(palette);
            const r = Math.round(rgb[0] * 0.72), g = Math.round(rgb[1] * 0.72), b = Math.round(rgb[2] * 0.72);
            const aspect = floaty ? rand(1.15, 1.75) : rand(1.0, 1.55);
            const bw = Math.max(2, Math.round(base * rand(0.85, 1.25))), bh = Math.max(3, Math.round(bw * aspect));
            const flipSpeed = insaneFlip ? rand(0.14, 0.26) : fastFlip ? rand(0.06, 0.12) : rand(0.02, 0.05);
            const blur = ultra ? 3 : 0;
            return { x, y, layer, hero, ultra, floaty, spr: getSprite(r, g, b, bw, bh, blur), vx, vy, rot: rand(0, Math.PI * 2), vr: rand(-0.02, 0.02) * (layer + 1), sway: rand(0, Math.PI * 2), swaySpeed: rand(0.01, 0.02), drift: rand(0.2, 0.6), flip: rand(0, Math.PI * 2), flipSpeed, dead: false };
        };

        piecesRef.current = Array.from({ length: COUNT }, () => makePiece(true));

        let last = performance.now();
        let startTime = performance.now();
        const spawnDuration = 2500; // Stop spawning new pieces after 2.5s for a "brief shower"

        const loop = (now) => {
            const dt = Math.min(0.033, (now - last) / 1000);
            last = now;
            ctx.clearRect(0, 0, w, h);
            const t = now * 0.001;
            const wind = 0.5 + Math.sin(t * 0.35) * 0.18 + mxRef.current * 0.3;

            let aliveCount = 0;
            for (let i = 0; i < piecesRef.current.length; i++) {
                const p = piecesRef.current[i];
                if (p.dead) continue;
                aliveCount++;

                const depth = p.layer === 0 ? 0.55 : p.layer === 1 ? 0.85 : 1.0;
                p.sway += p.swaySpeed * 60 * dt * SPEED;
                p.flip += p.flipSpeed * 60 * dt * SPEED;
                const floatDrift = Math.sin(p.sway) * p.drift * (p.floaty ? 1.15 : 1.0);
                const fall = p.floaty ? 0.52 + 0.24 * Math.sin(p.sway * 0.9) : 0.85;
                p.x += (wind * depth + floatDrift + p.vx) * 60 * dt * SPEED;
                p.y += p.vy * fall * 60 * dt * SPEED;
                p.rot += p.vr * 60 * dt * SPEED;

                if (p.x < -300) p.x = w + 300;
                if (p.x > w + 300) p.x = -300;
                
                if (p.y > h + 340) {
                    if (now - startTime < spawnDuration) {
                        piecesRef.current[i] = makePiece(false);
                    } else {
                        p.dead = true;
                    }
                }

                ctx.save();
                ctx.translate(p.x, p.y);
                ctx.rotate(p.rot);
                ctx.scale(0.06 + 0.94 * Math.abs(Math.sin(p.flip)), 1);
                ctx.globalAlpha = p.layer === 0 ? 0.16 : p.layer === 1 ? 0.42 : p.ultra ? 0.95 : p.hero ? 0.9 : 0.72;
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
