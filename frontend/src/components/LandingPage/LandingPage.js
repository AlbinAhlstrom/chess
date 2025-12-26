import React from 'react';
import { useNavigate } from 'react-router-dom';
import { getAuthLinks } from '../../api';
import './LandingPage.css';

function LandingPage() {
    const navigate = useNavigate();
    const { loginLink } = getAuthLinks();

    return (
        <div className="landing-container">
            <section className="hero-section">
                <div className="hero-content">
                    <h1>The Definitive Home for <span className="highlight">Chess Variants</span></h1>
                    <p className="hero-subtitle">
                        From Atomic to Racing Kings, explore a world beyond 64 squares. 
                        Built for enthusiasts, innovators, and anyone who thinks standard chess is just the beginning.
                    </p>
                    <div className="hero-actions">
                        <a href={loginLink} className="cta-button primary">Sign Up Now</a>
                        <button onClick={() => navigate('/create-game')} className="cta-button secondary">Browse Lobbies</button>
                    </div>
                </div>
            </section>

            <section className="features-grid">
                <div className="feature-card">
                    <div className="feature-icon">🛡️</div>
                    <h3>Atomic & Beyond</h3>
                    <p>Full support for Atomic, Antichess, Horde, and more with pixel-perfect rule enforcement.</p>
                </div>
                <div className="feature-card">
                    <div className="feature-icon">📈</div>
                    <h3>Elo Ratings</h3>
                    <p>Climb the ranks with dedicated Elo ratings for every variant, plus a global overall ranking.</p>
                </div>
                <div className="feature-card">
                    <div className="feature-icon">📱</div>
                    <h3>Modern Experience</h3>
                    <p>Fast, responsive, and real-time. Designed for both desktop and mobile play.</p>
                </div>
            </section>

            <section className="mission-statement">
                <h2>Our Mission</h2>
                <p>
                    Most platforms treat variants as an afterthought. At V-Chess, they are our DNA. 
                    We are building a world-class platform that gives variants the professional 
                    environment they deserve.
                </p>
            </section>
        </div>
    );
}

export default LandingPage;
