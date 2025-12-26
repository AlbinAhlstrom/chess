import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { getMe, getUserRatings, getUserProfile } from '../../api';
import './Profile.css';

function Profile() {
    const { userId: urlUserId } = useParams();
    const [user, setUser] = useState(null);
    const [ratings, setRatings] = useState([]);
    const [overall, setOverall] = useState(1500);
    const [isOwnProfile, setIsOwnProfile] = useState(false);
    
    const [autoPromote, setAutoPromote] = useState(() => {
        const saved = localStorage.getItem('autoPromoteToQueen');
        return saved !== null ? JSON.parse(saved) : true;
    });
    const [showCoordinates, setShowCoordinates] = useState(() => {
        const saved = localStorage.getItem('showBoardCoordinates');
        return saved !== null ? JSON.parse(saved) : false;
    });

    useEffect(() => {
        if (urlUserId) {
            // Viewing a public profile
            getUserProfile(urlUserId).then(data => {
                setUser(data.user);
                setRatings(data.ratings);
                setOverall(data.overall);
                
                // Check if this is the logged-in user's profile
                getMe().then(meData => {
                    if (meData.user && String(meData.user.id) === String(urlUserId)) {
                        setIsOwnProfile(true);
                    } else {
                        setIsOwnProfile(false);
                    }
                }).catch(() => setIsOwnProfile(false));
            }).catch(console.error);
        } else {
            // Viewing own profile
            getMe().then(data => {
                if (data.user) {
                    setUser(data.user);
                    setIsOwnProfile(true);
                    getUserRatings(data.user.id).then(rData => {
                        setRatings(rData.ratings || []);
                        setOverall(rData.overall || 1500);
                    });
                }
            }).catch(console.error);
        }
    }, [urlUserId]);

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

    if (!user) {
        return <div className='profile-container'>Loading profile...</div>;
    }

    return (
        <div className='profile-container'>
            <div className='profile-card'>
                <h1>{isOwnProfile ? "Your Profile" : `${user.name}'s Profile`}</h1>
                
                <section className='profile-section'>
                    <div className="profile-header">
                        {user.picture && <img src={user.picture} alt={user.name} className="profile-picture" />}
                        <div className="profile-identity">
                            <div className='info-row'>
                                <span className='label'>Name:</span>
                                <span className='value'>{user.name}</span>
                            </div>
                            {isOwnProfile && (
                                <div className='info-row'>
                                    <span className='label'>Email:</span>
                                    <span className='value'>{user.email}</span>
                                </div>
                            )}
                        </div>
                    </div>
                </section>

                <section className='profile-section'>
                    <h2>Elo Ratings</h2>
                    <div className='overall-rating'>
                        <span className='label'>Overall Ranking:</span>
                        <span className='value'>{Math.round(overall)}</span>
                    </div>
                    <div className='ratings-grid'>
                        {ratings.length > 0 ? ratings.map(r => (
                            <div key={r.variant} className='rating-item'>
                                <span className='variant-name'>{r.variant.charAt(0).toUpperCase() + r.variant.slice(1)}</span>
                                <span className='variant-rating'>{Math.round(r.rating)}</span>
                                <span className='variant-rd'>±{Math.round(r.rd)}</span>
                            </div>
                        )) : <p>No games played yet.</p>}
                    </div>
                </section>

                {isOwnProfile && (
                    <section className='profile-section'>
                        <h2>Preferences</h2>
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
                )}
            </div>
        </div>
    );
}

export default Profile;
