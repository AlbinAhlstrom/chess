import './App.css';
import Board from './components/Board/Board.js';
import { Pieces } from './components/Pieces/Pieces.js';
import { useCallback } from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';

function GameBoard({ variant }) {
  const handleFenChange = useCallback((newFen) => {
    // FEN state tracking removed from App as it's no longer displayed here
  }, []);

  return (
    <div className="App">
      <Board>
        <Pieces onFenChange={handleFenChange} variant={variant} />
      </Board>
    </div>
  );
}

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<GameBoard variant="standard" />} />
        <Route path="/antichess" element={<GameBoard variant="antichess" />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;