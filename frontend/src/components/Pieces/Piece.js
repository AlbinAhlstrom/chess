import React, { useRef } from 'react';
import './Pieces.css';

function Piece({ piece, file, rank, actualFile, actualRank, onDragStartCallback, onDragEndCallback, onDropCallback, onDragHoverCallback, isCapture }) {
    const ghostRef = useRef(null);
    
    // Fallback to display coords if actual coords not provided
    const realFile = actualFile !== undefined ? actualFile : file;
    const realRank = actualRank !== undefined ? actualRank : rank;

    const pieceStyle = {
        left: `calc(${file} * var(--square-size))`,
        top: `calc(${rank} * var(--square-size))`,
        '--piece-image': `url("/images/pieces/${piece}.png")`
    };

    const startDrag = (e) => {
        // Prevent default to avoid native drag, text selection, or scrolling on touch
        if (e.cancelable) e.preventDefault();

        // 1. Notify start
        if (onDragStartCallback) {
            onDragStartCallback({ file: realFile, rank: realRank, piece, isCapture });
        }

        if (isCapture) {
            return;
        }

        // Get initial coordinates (handle both mouse and touch)
        const clientX = e.type.startsWith('touch') ? e.touches[0].clientX : e.clientX;
        const clientY = e.type.startsWith('touch') ? e.touches[0].clientY : e.clientY;

        // 2. Create custom ghost (fully opaque)
        const rect = e.target.getBoundingClientRect();
        const offsetX = rect.width / 2;
        const offsetY = rect.height / 2;

        const ghost = document.createElement("div");
        ghost.classList.add("piece");
        ghost.style.position = "fixed";
        ghost.style.pointerEvents = "none";
        ghost.style.zIndex = "9999";
        ghost.style.width = `${rect.width}px`;
        ghost.style.height = `${rect.height}px`;
        ghost.style.backgroundImage = pieceStyle['--piece-image'];
        ghost.style.left = `${clientX - offsetX}px`;
        ghost.style.top = `${clientY - offsetY}px`;
        
        document.body.appendChild(ghost);
        ghostRef.current = ghost;

        // 3. Hide original
        e.target.style.opacity = "0";

        // 4. Set global cursor
        document.body.style.cursor = "grabbing";

        // 5. Define handlers
        const handleMove = (moveEvent) => {
            const mClientX = moveEvent.type.startsWith('touch') ? moveEvent.touches[0].clientX : moveEvent.clientX;
            const mClientY = moveEvent.type.startsWith('touch') ? moveEvent.touches[0].clientY : moveEvent.clientY;

            if (ghostRef.current) {
                ghostRef.current.style.left = `${mClientX - offsetX}px`;
                ghostRef.current.style.top = `${mClientY - offsetY}px`;
            }
            if (onDragHoverCallback) {
                onDragHoverCallback(mClientX, mClientY);
            }
        };

        const handleEnd = (endEvent) => {
            // Get last known coordinates from touch/mouse
            const endX = endEvent.type.startsWith('touch') ? endEvent.changedTouches[0].clientX : endEvent.clientX;
            const endY = endEvent.type.startsWith('touch') ? endEvent.changedTouches[0].clientY : endEvent.clientY;

            // Cleanup listeners
            document.removeEventListener('mousemove', handleMove);
            document.removeEventListener('mouseup', handleEnd);
            document.removeEventListener('touchmove', handleMove);
            document.removeEventListener('touchend', handleEnd);

            // Cleanup ghost
            if (ghostRef.current) {
                ghostRef.current.remove();
                ghostRef.current = null;
            }

            // Restore original visibility
            e.target.style.opacity = "1";

            // Restore cursor
            document.body.style.cursor = "default";

            // Notify drop
            if (onDropCallback) {
                onDropCallback({
                    clientX: endX,
                    clientY: endY,
                    piece,
                    file: realFile,
                    rank: realRank
                });
            }

            // Clear hover
            if (onDragHoverCallback) {
                onDragHoverCallback(null);
            }

            // Notify end
            if (onDragEndCallback) {
                onDragEndCallback();
            }
        };

        // Attach global listeners
        document.addEventListener('mousemove', handleMove);
        document.addEventListener('mouseup', handleEnd);
        document.addEventListener('touchmove', handleMove, { passive: false });
        document.addEventListener('touchend', handleEnd);
    };

    return (
        <div
            className="piece"
            style={{...pieceStyle, touchAction: 'none'}}
            onMouseDown={startDrag}
            onTouchStart={startDrag}
            onClick={(e) => {
                if (!isCapture) {
                    e.stopPropagation();
                }
            }}
        />
    );
}

export default Piece;