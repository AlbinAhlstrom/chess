import React from 'react';

export function MatchmakingSettings({
    ratingRange,
    setRatingRange,
    saveSettings,
    saving
}) {
    return (
        <section className='settings-section'>
            <h2>Matchmaking</h2>
            <div className='preference-row'>
                <div className='preference-info'>
                    <span className='label'>Rating Range (±)</span>
                    <p className='description'>Find opponents within this rating difference of yours.</p>
                </div>
                <div className='range-input-container' style={{ display: 'flex', alignItems: 'center', gap: '15px' }}>
                    <input 
                        type='range' 
                        min='50' 
                        max='1000' 
                        step='50'
                        value={ratingRange} 
                        onChange={(e) => {
                            const val = parseInt(e.target.value);
                            setRatingRange(val);
                        }}
                        onMouseUp={() => saveSettings({ ratingRange })}
                        onTouchEnd={() => saveSettings({ ratingRange })}
                        className='settings-range'
                    />
                    <span className='range-value' style={{ minWidth: '45px', fontWeight: 'bold' }}>{ratingRange}</span>
                </div>
            </div>
            {saving && <p className="saving-indicator">Saving...</p>}
        </section>
    );
}
