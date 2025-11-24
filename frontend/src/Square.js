import React from 'react';
import './Square.css';
import { getPieceImagePath } from './fenUtils';

function Square({ isLight, pieceChar }) { 
    const imagePath = getPieceImagePath(pieceChar);
    const squareClass = isLight ? 'square light' : 'square dark';

    return (
        <div className={squareClass}>
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
