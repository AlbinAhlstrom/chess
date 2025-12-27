import React from 'react';
import './About.css';

function About() {
    return (
        <div className="about-container">
            <div className="about-content">
                <h1>Our Mission: Variant-First Chess</h1>
                <p className="mission-statement">
                    V-Chess was born from a simple realization: while standard chess is beautiful, the world of chess variants is an untapped universe of strategic depth and creativity.
                </p>
                
                <section>
                    <h2>Why V-Chess?</h2>
                    <p>
                        Most platforms treat variants as an afterthought. We treat them as the core experience. 
                        Our engine is built from the ground up to support any rule set—from the explosive logic of Atomic chess 
                        to the asymmetrical warfare of Horde.
                    </p>
                </section>

                <section>
                    <h2>The Roadmap</h2>
                    <ul>
                        <li><strong>Community Tournaments:</strong> Daily Arena and Swiss events.</li>
                        <li><strong>Variant Creator:</strong> Tools for you to design and play your own chess rules.</li>
                        <li><strong>Learning Tools:</strong> Daily puzzles and interactive lessons specific to variants.</li>
                    </ul>
                </section>

                <section>
                    <h2>Join the Community</h2>
                    <p>
                        We are currently in early development. Your feedback is what shapes the future of this platform.
                    </p>
                    <div className="about-actions">
                        <a href="https://discord.gg/wGCBs5Qr" target="_blank" rel="noopener noreferrer" className="community-link discord">
                            Join our Discord
                        </a>
                        <a href="https://forms.gle/your-feedback-form" target="_blank" rel="noopener noreferrer" className="community-link feedback">
                            Give Feedback
                        </a>
                    </div>
                </section>
            </div>
        </div>
    );
}

export default About;
