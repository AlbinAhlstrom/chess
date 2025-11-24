import React, { useState, useEffect } from 'react';
import Square from './Square';
import './Board.css';

function Board() {
  const [fen, setFen] = useState('Loading...'); 

  useEffect(() => {
    fetch('/api/board')
      .then(response => response.json())
      .then(data => {
        setFen(data.fen);
        console.log("FEN received:", data.fen);
      })
      .catch(error => {
        console.error('Error fetching board state:', error);
        setFen('Error loading board.');
      });
  }, []);

  return (
    <div className="chessboard-container">
      <h2>Current FEN: {fen}</h2>
      <div className="chessboard">
      </div>
    </div>
  );
}

export default Board;
