import React from 'react';
import './FenDisplay.css';

function FenDisplay({ fen }) {
    const copyFenToClipboard = async () => {
        console.log('Attempting to copy FEN:', fen);
        try {
            await navigator.clipboard.writeText(fen);
            // alert('FEN copied to clipboard!'); // Removed alert
        } catch (err) {
            console.error('Failed to copy FEN: ', err);
            // alert('Failed to copy FEN. Please check console for details.'); // Removed alert
        }
    };

    return (
        <div className="fen-display-container">
            <p className="fen-string">{fen}</p>
            <button className="copy-fen-button" onClick={copyFenToClipboard}>
                Copy FEN
            </button>
        </div>
    );
}

export default FenDisplay;
