import React from 'react';
import { getAuthLinks } from '../../../api';

function GuestSignInPrompt({ onDismiss, onDontAskAgain }) {
    const { loginLink } = getAuthLinks();

    return (
        <div className="new-game-dialog-overlay">
            <div className="new-game-dialog">
                <h2>Game Over!</h2>
                <p style={{ textAlign: 'center', marginBottom: '20px' }}>
                    Great game! Sign in now to save your game history and track your progress.
                </p>
                
                <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
                    <a 
                        href={loginLink} 
                        className="start-btn" 
                        style={{ textDecoration: 'none', textAlign: 'center' }}
                    >
                        Sign In with Google
                    </a>
                    
                    <div style={{ display: 'flex', gap: '10px' }}>
                        <button 
                            onClick={onDismiss} 
                            className="cancel-btn"
                            style={{ flex: 1 }}
                        >
                            Later
                        </button>
                        <button 
                            onClick={onDontAskAgain} 
                            className="cancel-btn"
                            style={{ flex: 1, fontSize: '12px' }}
                        >
                            Don't ask again
                        </button>
                    </div>
                </div>
            </div>
        </div>
    );
}

export default GuestSignInPrompt;
