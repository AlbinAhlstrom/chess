import React, { useState, useEffect } from 'react';
import { getMe } from '../../api';
import './Profile.css';

function Profile() {
    const [user, setUser] = useState(null);
    const [autoPromote, setAutoPromote] = useState(() => {
        const saved = localStorage.getItem('autoPromoteToQueen');
        return saved !== null ? JSON.parse(saved) : true;
    });

    useEffect(() => {
        getMe().then(data => setUser(data.user)).catch(console.error);
    }, []);

    const handleToggle = () => {
        const newValue = !autoPromote;
        setAutoPromote(newValue);
        localStorage.setItem('autoPromoteToQueen', JSON.stringify(newValue));
    };

    if (!user) {
        return <div className="profile-container">Loading profile...</div>;
    }

    return (
        <div className="profile-container">
            <div className="profile-card">
                <h1>Profile Configuration</h1>
                
                <section className="profile-section">
                    <h2>Profile Info</h2>
                    <div className="info-row">
                        <span className="label">Name:</span>
                        <span className="value">{user.name}</span>
                    </div>
                    <div className="info-row">
                        <span className="label">Email:</span>
                        <span className="value">{user.email}</span>
                    </div>
                </section>

                <section className="profile-section">
                    <h2>Preferences</h2>
                    <div className="preference-row">
                        <div className="preference-info">
                            <span className="label">Auto Promote to Queen</span>
                            <p className="description">Automatically promote pawns to Queen when reaching the last row.</p>
                        </div>
                        <label className="switch">
                            <input 
                                type="checkbox" 
                                checked={autoPromote} 
                                onChange={handleToggle} 
                            />
                            <span className="slider round"></span>
                        </label>
                    </div>
                </section>
            </div>
        </div>
    );
}

export default Profile;
