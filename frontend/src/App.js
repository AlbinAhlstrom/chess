import './App.css';
import Board from './components/Board/Board.js';
import { Pieces } from './components/Pieces/Pieces.js';
import { useCallback, useState, useEffect } from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { getMe, getAuthLinks } from './api.js';

function Header() {
  const [user, setUser] = useState(null);
  const { loginLink, logoutLink } = getAuthLinks();

  const fetchUser = useCallback(() => {
    getMe().then(data => {
      if (data.user) {
        setUser(data.user);
      } else {
        setUser(null);
      }
    }).catch(e => {
      console.error("Failed to fetch user:", e);
      setUser(null);
    });
  }, []);

  useEffect(() => {
    fetchUser();
  }, [fetchUser]);

  // Refresh user when tab is focused (e.g. returning from login redirect)
  useEffect(() => {
    window.addEventListener('focus', fetchUser);
    return () => window.removeEventListener('focus', fetchUser);
  }, [fetchUser]);

  return (
    <header className="main-header">
      <div className="auth-section">
        {user ? (
          <div className="user-profile">
            <img src={user.picture} alt={user.name} className="header-avatar" title={user.name} />
            <a className="header-auth-link" href={logoutLink}>Logout</a>
          </div>
        ) : (
          <a className="header-auth-link" href={loginLink}>Login</a>
        )}
      </div>
    </header>
  );
}

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
      <Header />
      <Routes>
        <Route path="/" element={<GameBoard variant="standard" />} />
        <Route path="/standard" element={<GameBoard variant="standard" />} />
        <Route path="/antichess" element={<GameBoard variant="antichess" />} />
        <Route path="/atomic" element={<GameBoard variant="atomic" />} />
        <Route path="/chess960" element={<GameBoard variant="chess960" />} />
        <Route path="/crazyhouse" element={<GameBoard variant="crazyhouse" />} />
        <Route path="/horde" element={<GameBoard variant="horde" />} />
        <Route path="/kingofthehill" element={<GameBoard variant="kingofthehill" />} />
        <Route path="/racingkings" element={<GameBoard variant="racingkings" />} />
        <Route path="/threecheck" element={<GameBoard variant="threecheck" />} />
        <Route path="/game/:gameId" element={<GameBoard />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
