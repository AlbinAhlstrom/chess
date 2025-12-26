import React from 'react';
import { Link } from 'react-router-dom';

function PlayerNameDisplay({ 
    isOpponent, 
    isFlipped, 
    player,
    ratingDiff,
    takebackOffer, 
    user, 
    timers, 
    turn, 
    formatTime 
}) {
    const displayClass = isOpponent ? "opponent-name" : "player-name";
    
    const playerName = player ? player.name : "Anonymous";
    const rating = player && player.rating ? player.rating : null;
    const playerId = player ? player.id : null;

    // Logic for which timer to show
    const timerKey = isOpponent 
        ? (isFlipped ? 'w' : 'b') 
        : (isFlipped ? 'b' : 'w');
    
    const isTimerActive = turn === timerKey;

    const renderName = () => {
        if (playerId && playerId !== "computer") {
            return (
                <Link to={`/profile/${playerId}`} className="name-link">
                    <span className="name-text">{playerName}</span>
                </Link>
            );
        }
        return <span className="name-text">{playerName}</span>;
    };

    return (
        <div className={`player-name-display ${displayClass}`}>
            <div className="player-info">
                {renderName()}
                {rating && <span className="rating-text"> ({rating})</span>}
                {ratingDiff !== null && ratingDiff !== undefined && (
                    <span className={`rating-diff ${ratingDiff >= 0 ? 'positive' : 'negative'}`}>
                        {ratingDiff > 0 ? `+${ratingDiff}` : ratingDiff}
                    </span>
                )}
            </div>
            
            {isOpponent && takebackOffer && user && takebackOffer.by_user_id !== user.id && (
                <span className="takeback-prompt">Accept takeback?</span>
            )}
            
            {timers && (
                <span className={`clock-display ${isTimerActive ? 'active' : ''}`}>
                    {formatTime(timers[timerKey])}
                </span>
            )}
        </div>
    );
}

export default PlayerNameDisplay;
