import React, { useState, useEffect } from 'react';
import Square from './Square';
import './Board.css';

function Board() {
  const [fen, setFen] = useState('Loading...');
  const ranks = [8, 7, 6, 5, 4, 3, 2, 1];
  const files = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'];
  const squares = [];

  useEffect(() => {
    fetch('/api/board')
      .then(response => response.json())
      .then(data => {
        setFen(data.fen);
      })
      .catch(error => {
        console.error('Error fetching board state:', error);
        setFen('Error loading board.');
      });
  }, []);

  for (let i = 0; i < 8; i++) {
    for (let j = 0; j < 8; j++) {

      const rank = ranks[i];
      const file = files[j];

      const color = (i + j) % 2 === 0 ? 'light' : 'dark';

      squares.push(
        <Square 
          key={`${file}${rank}`}
          color={color}
          rank={rank}
          file={file}
        />
      );
    }
  }

  return (
    <div className="chessboard-container">
      <h2>Current FEN: {fen}</h2> 
      <div className="chessboard">
        {squares}
      </div>
    </div>
  );
}

export default Board;
