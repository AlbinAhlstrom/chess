// Force localhost for development to ensure session cookies work correctly
const getApiBase = () => {
    if (process.env.REACT_APP_API_URL) return process.env.REACT_APP_API_URL;
    
    // In development, always use localhost to match Google OAuth settings
    return `http://localhost:8000/api`;
};

// Helper to get consistent WS base
export const getWsBase = () => {
    if (process.env.REACT_APP_WS_URL) return process.env.REACT_APP_WS_URL;
    
    return `ws://localhost:8000/ws`;
};

const API_BASE = getApiBase();
const AUTH_BASE = API_BASE.replace('/api', '/auth');

export const getAllLegalMoves = async (gameId) => {
    const res = await fetch(`${API_BASE}/moves/all_legal`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ game_id: gameId }),
        credentials: 'include'
    });
    return res.json();
};

export const createGame = async (variant = "standard", fen = null, timeControl = null) => {
    const res = await fetch(`${API_BASE}/game/new`, { 
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ 
            variant, 
            fen,
            time_control: timeControl 
        }),
        credentials: 'include'
    });
    return res.json();
};

export const getLegalMoves = async (gameId, square) => {
    const res = await fetch(`${API_BASE}/moves/legal`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ game_id: gameId, square }),
        credentials: 'include'
    });
    return res.json();
};

export const getGame = async (gameId) => {
    const res = await fetch(`${API_BASE}/game/${gameId}`, {
        credentials: 'include'
    });
    return res.json();
};

export const getMe = async () => {
    const res = await fetch(`${API_BASE}/me`, {
        credentials: 'include'
    });
    return res.json();
};

export const getAuthLinks = () => {
    return {
        loginLink: `${AUTH_BASE}/login`,
        logoutLink: `${AUTH_BASE}/logout`
    };
};