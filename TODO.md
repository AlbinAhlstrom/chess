# v-chess Strategic Roadmap

**Objective:** To build a world-class, full-featured competitor to Chess.com and Lichess, with a primary strategic focus on supporting the widest possible array of chess variants. We aim to be the definitive home for variant enthusiasts and innovators.

---

## 🟢 Phase 0: Foundations (Completed)
- [x] **Core Game Engine**: Robust OOP-based engine supporting Standard, Horde, Racing Kings, etc.
- [x] **Matchmaking / Lobby**: Global seek system for public games.
- [x] **Real-time Infrastructure**: WebSocket-based movement and game state broadcasting.
- [x] **Persistence Layer**: SQLAlchemy/SQLite database for users and game history.
- [x] **Authentication**: Google OAuth for seamless user onboarding.
- [x] **Time Control**: Reliable clock management and timeout detection.
- [x] **Essential Controls**: Resignation, draws, and takebacks.
- [x] **Mobile-First UX**: Responsive design for play on any device.
- [x] **Advanced Rating System**: Separate Glicko-2 ratings for every variant.

---

## 🟣 Phase 0.5: MVP Polish (Kickstarter/Patreon Launch)
**Goal:** Deliver a polished, bug-free, and engaging experience to showcase potential to backers.
- [ ] **Visual Identity Overhaul**:
    - [ ] Distinctive, high-quality homepage (Landing Page) explaining the "Variant-First" mission.
    - [ ] Professional logo and consistent color palette across the UI.
    - [ ] Interactive "Hero" board on the landing page showing a live variant game.
- [ ] **User Profile & Social Proof**:
    - [ ] Public user profiles showing rating graphs and favorite variants.
    - [ ] "Supporter" badges infrastructure (for future Kickstarter backers).
- [ ] **Game Experience**:
    - [ ] Sound effects for move types (capture, check, castle) - *Partially implemented, needs polish*.
    - [ ] Visual move indicators (last move highlight, legal move dots) - *Refine visibility*.
    - [ ] Simple "Game Over" modal with clear winner and rating change - *Completed*.
- [x] **Community Foundation**:
    - [x] "About" / "Our Mission" page detailing the roadmap.
    - [x] Integration of Discord/Community links in the footer.
    - [x] Feedback mechanism (simple form or link).

---

## 🔴 Phase 1: Competitive & Social Core (High Priority)
- [ ] **Leaderboards**: Top player rankings per variant.
- [ ] **In-Game Socialization**: Real-time chat with system-wide notifications.
- [ ] **Anti-Cheat Infrastructure**: Server-side move validation (completed) and behavior monitoring.
- [ ] **Tournament Engine**: Support for Arena and Swiss-style tournaments for all variants.

---

## 🟡 Phase 2: Variant Explosion & Analysis (Mid Priority)
- [ ] **Expanded Variant Library**:
    - [ ] Duck Chess
    - [ ] Fog of War
    - [ ] Capablanca Chess (10x8)
    - [ ] Custom Variant Creator (Scriptable rules engine)
- [ ] **Server-side Engine Evaluation**: Integration with Stockfish (Multi-variant) for post-game analysis.
- [ ] **WASM Frontend Engine**: In-browser Stockfish for real-time evaluation and "best move" suggestions in analysis mode.
- [ ] **Annotated Move History**: Support for PGN exports with variant-specific extensions.

---

## 🔵 Phase 3: Polish & Advanced Features (Long Term)
- [ ] **Visual Customization**: Board skins, 3D piece sets, and custom soundscapes.
- [ ] **Visual Aids**: Right-click arrow/square highlighting for tactical planning.
- [ ] **Premoving & Smart-Moves**: Low-latency move queuing.
- [ ] **Variant Puzzles**: Daily tactical puzzles generated from actual variant games on the platform.
- [ ] **Streaming Tools**: Integrated "Streamer Mode" and obs-friendly layout components.

---

### Strategic Notes:
*   **Variant-First Design**: Every new feature (analysis, puzzles, ratings) must be designed to work generically across all supported variants.
*   **Infrastructure**: Scale from SQLite to PostgreSQL as the user base grows to support complex analytical queries.