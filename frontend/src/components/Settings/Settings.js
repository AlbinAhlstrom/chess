import React, { useState } from 'react';
import './Settings.css';

function Settings() {
    const [autoPromote, setAutoPromote] = useState(() => {
        const saved = localStorage.getItem('autoPromoteToQueen');
        return saved !== null ? JSON.parse(saved) : true;
    });
    const [showCoordinates, setShowCoordinates] = useState(() => {
        const saved = localStorage.getItem('showBoardCoordinates');
        return saved !== null ? JSON.parse(saved) : false;
    });

    const handleAutoPromoteToggle = () => {
        const newValue = !autoPromote;
        setAutoPromote(newValue);
        localStorage.setItem('autoPromoteToQueen', JSON.stringify(newValue));
    };

    const handleCoordinatesToggle = () => {
        const newValue = !showCoordinates;
        setShowCoordinates(newValue);
        localStorage.setItem('showBoardCoordinates', JSON.stringify(newValue));
    };

    return (
        <div className='settings-container'>
            <div className='settings-card'>
                <h1>Account Settings</h1>
                
                <section className='settings-section'>
                    <h2>Game Preferences</h2>
                    <div className='preference-row'>
                        <div className='preference-info'>
                            <span className='label'>Auto Promote to Queen</span>
                            <p className='description'>Automatically promote pawns to Queen when reaching the last row.</p>
                        </div>
                        <label className='switch'>
                            <input type='checkbox' checked={autoPromote} onChange={handleAutoPromoteToggle} />
                            <span className='slider round'></span>
                        </label>
                    </div>

                    <div className='preference-row'>
                        <div className='preference-info'>
                            <span className='label'>Show Board Coordinates</span>
                            <p className='description'>Display rank (1-8) and file (a-h) labels on the board edges.</p>
                        </div>
                        <label className='switch'>
                            <input type='checkbox' checked={showCoordinates} onChange={handleCoordinatesToggle} />
                            <span className='slider round'></span>
                        </label>
                    </div>
                </section>

                <section className='settings-section'>
                    <h2>About V-Chess</h2>
                    <p className='settings-info-text'>
                        V-Chess is a variant-first chess platform. Your preferences are saved locally to this browser.
                    </p>
                </section>
            </div>
        </div>
    );
}

export default Settings;
