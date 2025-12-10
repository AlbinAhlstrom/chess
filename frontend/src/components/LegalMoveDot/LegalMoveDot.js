import React from 'react';
import './LegalMoveDot.css';

function LegalMoveDot({ file, rank }) {
    const dotStyle = {
        left: `calc(${file} * var(--square-size))`,
        top: `calc(${rank} * var(--square-size))`,
        position: 'absolute', // Ensure absolute positioning to overlay the board
        width: 'var(--square-size)', // Take up the whole square
        height: 'var(--square-size)', // Take up the whole square
    };

    return (
        <div className="legal-move-dot" style={dotStyle}></div>
    );
}

export default LegalMoveDot;