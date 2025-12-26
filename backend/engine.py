import asyncio
import os
import logging
from typing import Optional, Dict
from v_chess.game import Game
from v_chess.move import Move

logger = logging.getLogger(__name__)

VARIANT_MAP = {
    "standard": "chess",
    "antichess": "antichess",
    "atomic": "atomic",
    "chess960": "chess", # handled via FEN
    "crazyhouse": "crazyhouse",
    "horde": "horde",
    "kingofthehill": "kingofthehill",
    "racingkings": "racingkings",
    "threecheck": "3check",
}

class UCIEngine:
    def __init__(self, engine_path: str):
        self.engine_path = engine_path
        self.process: Optional[asyncio.subprocess.Process] = None
        self.lock = asyncio.Lock()

    async def start(self):
        if self.process:
            return

        if not os.path.exists(self.engine_path):
            raise FileNotFoundError(f"Engine not found at {self.engine_path}")

        self.process = await asyncio.create_subprocess_exec(
            self.engine_path,
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        
        # Initialize UCI
        await self.send_command("uci")
        while True:
            line = await self.read_line()
            if line == "uciok":
                break

    async def stop(self):
        if self.process:
            try:
                self.process.terminate()
                await self.process.wait()
            except Exception as e:
                logger.error(f"Error stopping engine: {e}")
            self.process = None

    async def send_command(self, command: str):
        if self.process and self.process.stdin:
            logger.info(f"Engine << {command}")
            self.process.stdin.write(f"{command}\n".encode())
            await self.process.stdin.drain()

    async def read_line(self) -> str:
        if self.process and self.process.stdout:
            line = await self.process.stdout.readline()
            decoded = line.decode().strip()
            if decoded:
                logger.info(f"Engine >> {decoded}")
            return decoded
        return ""

    async def set_option(self, name: str, value: str):
        await self.send_command(f"setoption name {name} value {value}")

    async def is_ready(self):
        await self.send_command("isready")
        while True:
            line = await self.read_line()
            if line == "readyok":
                break

    async def go(self, fen: str, moves: list[str] = None, time_limit: float = 1.0, variant: str = "standard") -> Optional[str]:
        async with self.lock:
            # Set variant if needed
            fairy_variant = VARIANT_MAP.get(variant, "chess")
            await self.set_option("UCI_Variant", fairy_variant)
            
            await self.is_ready()

            # Setup position
            if fen == "startpos":
                cmd = "position startpos"
            else:
                cmd = f"position fen {fen}"
            
            if moves:
                cmd += f" moves {' '.join(moves)}"
            await self.send_command(cmd)
            
            # Start search
            # movetime is in milliseconds
            movetime = int(time_limit * 1000)
            await self.send_command(f"go movetime {movetime}")

            best_move = None
            while True:
                line = await self.read_line()
                if line.startswith("bestmove"):
                    parts = line.split()
                    if len(parts) >= 2:
                        best_move = parts[1]
                        if best_move == "(none)":
                            best_move = None
                    break
            
            return best_move

# Singleton instance or factory could be used
ENGINE_PATH = os.path.join(os.path.dirname(__file__), "engines", "fairy-stockfish")

class EngineManager:
    """Manages a single engine instance shared or dedicated."""
    def __init__(self):
        self.engine = UCIEngine(ENGINE_PATH)
        self.started = False

    async def ensure_started(self):
        if not self.started:
            await self.engine.start()
            self.started = True

    async def get_best_move(self, fen: str, variant: str = "standard", time_limit: float = 1.0) -> Optional[str]:
        await self.ensure_started()
        return await self.engine.go(fen=fen, variant=variant, time_limit=time_limit)

# Global engine manager
engine_manager = EngineManager()
