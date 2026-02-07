import React, { useState, useCallback } from 'react';
import { useParams, useLocation } from 'react-router-dom';
import Board from './Board';
import { Pieces } from '../Pieces/Pieces';
import GrapeGame from './GrapeGame';

function GameBoardWrapper({ variant: propVariant, matchmaking = false, computer = false }) {
  const { variant: urlVariant } = useParams();
  const location = useLocation();
  const variant = urlVariant || propVariant || "standard";
  const [flipped, setFlipped] = useState(false);
  const [isLatest, setIsLatest] = useState(true);

  const handleFenChange = useCallback((newFen) => {
    // FEN state tracking removed from App
  }, []);

  const showCoordinates = (() => {
    const saved = localStorage.getItem('showBoardCoordinates');
    return saved !== null ? JSON.parse(saved) : false;
  })();

  if (variant === 'grape') {
    return (
      <div className="App">
        <GrapeGame
          gameId={location.pathname.split('/').pop()}
          setFlipped={setFlipped}
          setWinner={() => { }}
          setIsGameOver={() => { }}
        />
      </div>
    );
  }

  return (
    <div className="App">
      <Board flipped={flipped} showCoordinates={showCoordinates} pointerEvents={isLatest ? 'auto' : 'none'}>
        <Pieces
          onFenChange={handleFenChange}
          variant={variant}
          matchmaking={matchmaking}
          computer={computer}
          setFlipped={setFlipped}
          setIsLatest={setIsLatest}
          timeControl={location.state?.timeControl}
        />
      </Board>
    </div>
  );
}

export default GameBoardWrapper;
