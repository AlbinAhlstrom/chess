from dataclasses import dataclass, field
from typing import Optional
import time
from v_chess.enums import Color
from v_chess.move import Move

@dataclass
class RelayState:
    """Minimal state container for RelayGame."""
    fen: str
    turn: Color = Color.WHITE
    explosion_square: Optional[str] = None
    
    # Mock board object to satisfy some accessors if needed, 
    # but mostly we just return None or empty stuff if accessed.
    @property
    def board(self):
        class MockBoard:
            def get_piece(self, sq): return None
        return MockBoard()

class RelayGame:
    """
    A game implementation that acts as a dumb relay.
    It trusts the inputs (FEN, moves) provided by the client/controller
    and does not enforce rules or move validation.
    """
    def __init__(self, state: str | None = None, rules=None, time_control=None):
        # Initial Grape FEN or custom start
        # Standard Grape FEN: "lllziiiioo/lvzzsstjoo/vvzssttjjj/......t...///...T....../JJJTTSSZVV/OOJTSSZZVL/OOIIIIZLLL w"
        default_fen = "lllziiiioo/lvzzsstjoo/vvzssttjjj/......t...///...T....../JJJTTSSZVV/OOJTSSZZVL/OOIIIIZLLL w"
        
        start_fen = state if isinstance(state, str) else default_fen
        if hasattr(state, 'fen'): start_fen = state.fen
            
        self.state = RelayState(fen=start_fen)
        
        # Parse turn from FEN if possible (simple check)
        parts = start_fen.split(' ')
        if len(parts) >= 2:
            self.state.turn = Color(parts[1])
            
        self.time_control = time_control
        self.clocks = {}
        if time_control:
            limit = time_control.get('limit', 600)
            self.clocks = {Color.WHITE: limit, Color.BLACK: limit}
            
        self.move_history = []  # List of move notations/objects
        self.uci_history = []   # List of UCI strings
        self.last_move_at = None
        self.is_over = False
        self.winner = None
        self.is_check = False
        
        self._history_stack = [] # To support undo

    def take_turn(self, move: Move, offer_draw: bool = False, **kwargs):
        """
        Relay the turn. 
        kwargs expected to contain 'fen', 'turn', 'is_over', 'winner' from client.
        """
        # Save current state for undo
        self._history_stack.append({
            'fen': self.state.fen,
            'turn': self.state.turn,
            'move_history': list(self.move_history),
            'uci_history': list(self.uci_history),
            'is_over': self.is_over,
            'winner': self.winner,
            'last_move_at': self.last_move_at,
            'clocks': self.clocks.copy() if self.clocks else {}
        })

        # Update timings
        now = time.time()
        if self.time_control and self.last_move_at:
            elapsed = now - self.last_move_at
            # Subtract from the player who just MOVED (the one whose turn it was)
            # Wait, standard logic: turn is WHO IS TO MOVE.
            # If valid move comes in, it was made by 'self.state.turn'.
            if self.state.turn in self.clocks:
                self.clocks[self.state.turn] -= elapsed
                if self.time_control.get('increment'):
                    self.clocks[self.state.turn] += self.time_control['increment']
        self.last_move_at = now

        # Update histories
        # move.uci is the string notation
        self.move_history.append(move.uci) 
        self.uci_history.append(move.uci)

        # Update State from Client Data (Authoritative)
        new_fen = kwargs.get('fen')
        if new_fen:
            self.state.fen = new_fen
            
            # Update turn based on FEN or explicit arg
            parts = new_fen.split(' ')
            if len(parts) >= 2:
                try:
                    self.state.turn = Color(parts[1])
                except:
                    pass
        else:
            # Fallback: simple toggle if no FEN provided (shouldn't happen with correct frontend)
            self.state.turn = Color.BLACK if self.state.turn == Color.WHITE else Color.WHITE

        # Check game over data from client
        if kwargs.get('is_over'):
            self.is_over = True
            self.winner = kwargs.get('winner')

    def undo_move(self):
        if not self._history_stack:
            return
        
        prev = self._history_stack.pop()
        self.state.fen = prev['fen']
        self.state.turn = prev['turn']
        self.move_history = prev['move_history']
        self.uci_history = prev['uci_history']
        self.is_over = prev['is_over']
        self.winner = prev['winner']
        self.last_move_at = prev['last_move_at']
        self.clocks = prev['clocks']

    def get_current_clocks(self):
        # Simple projection if game is active
        if self.is_over or not self.last_move_at or not self.time_control:
            return self.clocks
        
        ret = self.clocks.copy()
        elapsed = time.time() - self.last_move_at
        if self.state.turn in ret:
            ret[self.state.turn] -= elapsed
        return ret

    # Required interfaces for GameService / Persistence
    def abort(self):
        self.is_over = True
        self.winner = "aborted"

    def resign(self, player_color: Color):
        self.is_over = True
        self.winner = "white" if player_color == Color.BLACK else "black"

    def agree_draw(self):
        self.is_over = True
        self.winner = None # Draw

    @property
    def history(self): 
        # For undo checks - returning something truthy if moves exist
        return self.move_history
