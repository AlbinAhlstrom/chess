import React from 'react';
import './Square.css';
import { getPieceImagePath } from './fenUtils';

function Square({ isLight, pieceChar, onClick, isSelected }) {
    const imagePath = getPieceImagePath(pieceChar);

    let squareClass = isLight ? 'square light' : 'square dark';
    if (isSelected) {
        squareClass += ' selected';
    }

    return (
        <div className={squareClass} onClick={onClick}>
            {imagePath && (
                <img
                    src={imagePath}
                    alt={pieceChar}
                    className="piece-image"
                />
            )}
        </div>
    );
}

export default Square;
