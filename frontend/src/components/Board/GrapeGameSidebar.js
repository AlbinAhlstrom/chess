import React from 'react';
import './GrapeGame.css'; // Share CSS for now or split if needed

const GrapeGameSidebar = ({
    blueToMove,
    gameOver,
    selectedSquare,
    handleRotation,
    setSelectedSquare
}) => {
    return (
        <div className="grape-sidebar">
            <div className="grape-status">
                Turn: <span className={blueToMove ? 'grape-blue-turn' : 'grape-red-turn'}>
                    {blueToMove ? "Blue" : "Red"}
                </span>
                {gameOver && <strong> - GAME OVER ({gameOver === 1 ? "Blue" : "Red"} Wins!)</strong>}
            </div>

            {selectedSquare && (
                <div className="grape-controls">
                    <button className="grape-rotation-btn" onClick={() => handleRotation(1)}>Rot 1 (90°L)</button>
                    <button className="grape-rotation-btn" onClick={() => handleRotation(2)}>Rot 2 (180°)</button>
                    <button className="grape-rotation-btn" onClick={() => handleRotation(3)}>Rot 3 (90°R)</button>
                    <button className="grape-rotation-btn" onClick={() => setSelectedSquare(null)}>Cancel</button>
                </div>
            )}

            <div className="grape-instructions">
                <p><strong>Controls:</strong> Click piece to select. Click destination to move. Use buttons to rotate.</p>
                <p><em>Note: This is a Relay Game. Rules are enforced by clients.</em></p>
            </div>
        </div>
    );
};

export default GrapeGameSidebar;
