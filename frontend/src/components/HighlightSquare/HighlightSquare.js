import React from 'react';
import './HighlightSquare.css';

function HighlightSquare({ file, rank, isDark }) {
    const style = {
        left: `calc(${file} * var(--square-size))`,
        top: `calc(${rank} * var(--square-size))`,
    };

    return (
        <div className={`highlight-square ${isDark ? 'dark' : ''}`} style={style}></div>
    );
}

export default HighlightSquare;
