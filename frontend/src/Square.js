import React from 'react';
import './Square.css';

function Square({ color, rank, file }) {
  const squareClass = `square ${color}`;

  const notation = `${file}${rank}`;

  return (
    <div className={squareClass}>
      <span className="notation">{notation}</span>
    </div>
  );
}

export default Square;
