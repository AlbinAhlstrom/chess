// GrapeEngine.js - Ported from grape.html
// Contains game logic, move generation, and AI for the Grape variant.

export const EMPTY = 0;
export const BLUE = 0;
export const RED = 1;

export const BOARD_SIZE = 10;
export const CELL_SIZE = 50;
export const CENTER_SQUARES = [[4, 4], [4, 5], [5, 4], [5, 5]];

export const ZEBRA_P = 2;
export const JAGUAR_P = 4;
export const VAMPIRE_P = 6;
export const ORANGUTAN_P = 8;
export const LEOPARD_P = 10;
export const TIGER_P = 12;
export const INSECT_P = 14;
export const SEAHORSE_P = 16;

export const PIECE_CHARS = {
    'Z': BLUE | ZEBRA_P, 'J': BLUE | JAGUAR_P, 'V': BLUE | VAMPIRE_P,
    'O': BLUE | ORANGUTAN_P, 'L': BLUE | LEOPARD_P, 'T': BLUE | TIGER_P,
    'I': BLUE | INSECT_P, 'S': BLUE | SEAHORSE_P,
    'z': RED | ZEBRA_P, 'j': RED | JAGUAR_P, 'v': RED | VAMPIRE_P,
    'o': RED | ORANGUTAN_P, 'l': RED | LEOPARD_P, 't': RED | TIGER_P,
    'i': RED | INSECT_P, 's': RED | SEAHORSE_P,
};

export const PIECE_TYPE_TO_ANIMAL = {
    [ZEBRA_P]: 'Zebra',
    [JAGUAR_P]: 'Jaguar',
    [VAMPIRE_P]: 'Vampire',
    [ORANGUTAN_P]: 'Orangutan',
    [LEOPARD_P]: 'Leopard',
    [TIGER_P]: 'Tiger',
    [INSECT_P]: 'Insect',
    [SEAHORSE_P]: 'Seahorse'
};

const BASE_SHAPES = {
    [LEOPARD_P]: [[0, 0], [0, 1], [0, 2], [1, 0]],
    [TIGER_P]: [[0, 1], [1, 0], [1, 1], [2, 1]],
    [INSECT_P]: [[0, 0], [0, 1], [0, 2], [0, 3]],
    [JAGUAR_P]: [[0, 0], [1, 0], [1, 1], [1, 2]],
    [ZEBRA_P]: [[0, 1], [1, 0], [1, 1], [2, 0]],
    [SEAHORSE_P]: [[0, 1], [0, 2], [1, 0], [1, 1]],
    [VAMPIRE_P]: [[0, 1], [1, 0], [1, 1]],
    [ORANGUTAN_P]: [[0, 0], [0, 1], [1, 0], [1, 1]]
};

export function isBlue(piece) {
    return piece !== EMPTY && piece % 2 === BLUE;
}

export function getPieceType(piece) {
    return piece & 0b11111110;
}

export function calculateMaterial(board) {
    let score = 0;
    for (let row = 0; row < BOARD_SIZE; row++) {
        for (let col = 0; col < BOARD_SIZE; col++) {
            if (board[row][col] !== EMPTY) {
                // Blue pieces are positive (if Blue=0, Red=1)
                // isBlue(RED piece) is false.
                score += isBlue(board[row][col]) ? 1 : -1;
            }
        }
    }
    return score;
}

function rotateShape90(shape) {
    const maxR = Math.max(...shape.map(([r, c]) => r));
    const rotated = shape.map(([r, c]) => [c, maxR - r]);
    const minR = Math.min(...rotated.map(([r, c]) => r));
    const minC = Math.min(...rotated.map(([r, c]) => c));
    return rotated.map(([r, c]) => [r - minR, c - minC]);
}

function getShapeFingerprint(shape) {
    const sorted = [...shape].sort((a, b) => a[0] - b[0] || a[1] - b[1]);
    return sorted.map(([r, c]) => `${r},${c}`).join('|');
}

const ALL_SHAPE_ROTATIONS = {};
for (const [pieceTypeStr, baseShape] of Object.entries(BASE_SHAPES)) {
    const pieceType = Number(pieceTypeStr);
    ALL_SHAPE_ROTATIONS[pieceType] = {};
    let shape = baseShape;
    for (let rot = 0; rot < 360; rot += 90) {
        ALL_SHAPE_ROTATIONS[pieceType][getShapeFingerprint(shape)] = rot;
        shape = rotateShape90(shape);
    }
}

// Helper: Rotate a point around a center
function rotatePoint(row, col, centerR, centerC) {
    return [
        col - centerC + centerR,
        centerR - row + centerC
    ];
}

// Helper: Get diamond squares around a center
function diamondAroundSquare(rCenter, cCenter, includeSelf) {
    const squares = [];
    for (let i = 0; i < 4; i++) {
        for (let j = 0; j < 4; j++) {
            if (!(i === 0 && j === 0 && !includeSelf) && i + j < 4) {
                if (rCenter + i < BOARD_SIZE && cCenter + j < BOARD_SIZE) {
                    squares.push([rCenter + i, cCenter + j]);
                }
                if (j !== 0 && rCenter + i < BOARD_SIZE && cCenter >= j) {
                    squares.push([rCenter + i, cCenter - j]);
                }
                if (i !== 0 && rCenter >= i && cCenter + j < BOARD_SIZE) {
                    squares.push([rCenter - i, cCenter + j]);
                }
                if (i !== 0 && j !== 0 && rCenter >= i && cCenter >= j) {
                    squares.push([rCenter - i, cCenter - j]);
                }
            }
        }
    }
    return squares;
}

// Helper: Find all squares of a specific piece
function findAllSquaresOfPiece(board, pivotR, pivotC) {
    const targetPiece = board[pivotR][pivotC];
    if (targetPiece === EMPTY) return [];

    // Optimization: Check diamond area only
    const candidates = diamondAroundSquare(pivotR, pivotC, true);
    const coords = [];

    for (const [r, c] of candidates) {
        if (r >= 0 && r < BOARD_SIZE && c >= 0 && c < BOARD_SIZE) {
            if (board[r][c] === targetPiece) {
                coords.push([r, c]);
            }
        }
    }
    return coords;
}

// Helper: Make a move (Pure function)
// Returns new game state or null if invalid
export function makeMovePure(pivotR, pivotC, hgrad, gameState) {
    if (pivotR < 0 || pivotR >= BOARD_SIZE || pivotC < 0 || pivotC >= BOARD_SIZE) return null;
    if (hgrad < 1 || hgrad > 3) return null;

    const piece = gameState.board[pivotR][pivotC];
    if (piece === EMPTY) return null;
    if (gameState.blueToMove !== isBlue(piece)) return null;

    const squares = findAllSquaresOfPiece(gameState.board, pivotR, pivotC);

    const newSquares = [];
    for (const [row, col] of squares) {
        let [newRow, newCol] = [row, col];
        for (let i = 0; i < hgrad; i++) {
            [newRow, newCol] = rotatePoint(newRow, newCol, pivotR, pivotC);
        }

        if (newRow < 0 || newRow >= BOARD_SIZE || newCol < 0 || newCol >= BOARD_SIZE) return null;

        const pieceInSquare = gameState.board[newRow][newCol];
        if (pieceInSquare !== piece && pieceInSquare !== EMPTY &&
            gameState.blueToMove === isBlue(pieceInSquare)) {
            return null; // Friendly fire
        }

        newSquares.push([Math.round(newRow), Math.round(newCol)]);
    }

    const newBoard = gameState.board.map(row => [...row]);
    let gameOver = null;
    let newMaterial = gameState.material;
    let capturedSomething = false;
    const alreadyCapturedPieces = new Set();

    // Step 1: Clear old positions
    for (const [row, col] of squares) {
        newBoard[row][col] = EMPTY;
    }

    // Step 2: Find and remove all captured pieces
    for (const [row, col] of newSquares) {
        const pieceInSquare = gameState.board[row][col];
        if (pieceInSquare !== EMPTY && gameState.blueToMove !== isBlue(pieceInSquare)) {
            // Whole piece capture logic
            const pieceKey = `${pieceInSquare}`; // Simple heuristic, works if piece types unique per side or handled by floodfill. 
            // Ideally we need floodfill if multiple pieces of same type exist. 
            // But existing code uses `diamondAroundSquare` on capture target?
            // Let's implement robust capture using the helper.

            // To avoid double counting, we flag the target square?
            // Or better: find all squares of the victim piece.

            // Wait, `findAllSquaresOfPiece` needs the BOARD. We should use `gameState.board` (the old one) to find connectivity.
            // But valid connectivity checks friendly adjacencies?
            // In Grape, pieces are distinct connected components.
            // If I overwrite a square, I capture the whole component connected to that square.

            const victimSquares = findAllSquaresOfPiece(gameState.board, row, col); // Find using OLD board
            // Actually, we must ensure we don't capture the SAME piece multiple times if we land on 2 squares of it.
            // The `victimSquares` will be the same set.

            // We can use a Set of coordinate strings to track captured squares.
            // But we need to know if it's an Orangutan.

            if (victimSquares.length > 0) {
                const sampleP = gameState.board[victimSquares[0][0]][victimSquares[0][1]];
                // Creating a unique ID for the piece instance is hard without object reference.
                // But `victimSquares` defines the piece.
                // Let's just clear them in `newBoard`.

                let isNewCapture = false;
                for (const [vr, vc] of victimSquares) {
                    if (newBoard[vr][vc] !== EMPTY) { // Not yet cleared
                        isNewCapture = true;
                        newBoard[vr][vc] = EMPTY;
                        // Material update? Simplified: +1/-1 per square? Or per piece?
                        // calculateMaterial uses per-square.
                        newMaterial += gameState.blueToMove ? 1 : -1;
                    }
                }

                if (isNewCapture) {
                    capturedSomething = true;
                    const type = getPieceType(sampleP);
                    if (type === ORANGUTAN_P) {
                        if (isBlue(sampleP)) gameOver = -1; // Blue Orangutan captured -> Red wins
                        else gameOver = 1; // Red Orangutan captured -> Blue wins
                    }
                }
            }
        }
    }

    // Step 3: Place our piece at new positions
    for (const [row, col] of newSquares) {
        newBoard[row][col] = piece;
    }

    // Check center win
    const BLUE_ORANGUTAN = BLUE | ORANGUTAN_P;
    const RED_ORANGUTAN = RED | ORANGUTAN_P;

    if (CENTER_SQUARES.every(([r, c]) => newBoard[r][c] === BLUE_ORANGUTAN)) {
        gameOver = 1;
    }
    if (CENTER_SQUARES.every(([r, c]) => newBoard[r][c] === RED_ORANGUTAN)) {
        gameOver = -1;
    }

    return {
        board: newBoard,
        blueToMove: !gameState.blueToMove,
        gameOver: gameOver,
        material: newMaterial,
        move: { row: pivotR, col: pivotC, hgrad: hgrad },
        captured: capturedSomething
    };
}

// Bot AI

function generateMoves(gameState) {
    const moves = [];
    for (let row = 0; row < BOARD_SIZE; row++) {
        for (let col = 0; col < BOARD_SIZE; col++) {
            const piece = gameState.board[row][col];
            if (piece !== EMPTY && gameState.blueToMove === isBlue(piece)) {
                for (let hgrad = 1; hgrad <= 3; hgrad++) {
                    const newState = makeMovePure(row, col, hgrad, gameState);
                    if (newState !== null) {
                        moves.push(newState);
                    }
                }
            }
        }
    }
    return moves;
}

function getOrangutanDistances(board) {
    let blueSumRow = 0, blueSumCol = 0, blueCount = 0;
    let redSumRow = 0, redSumCol = 0, redCount = 0;
    const BLUE_ORANGUTAN = BLUE | ORANGUTAN_P;
    const RED_ORANGUTAN = RED | ORANGUTAN_P;

    for (let row = 0; row < BOARD_SIZE; row++) {
        for (let col = 0; col < BOARD_SIZE; col++) {
            const piece = board[row][col];
            if (piece === BLUE_ORANGUTAN) {
                blueSumRow += row;
                blueSumCol += col;
                blueCount++;
            } else if (piece === RED_ORANGUTAN) {
                redSumRow += row;
                redSumCol += col;
                redCount++;
            }
        }
    }

    const centerRow = 4.5;
    const centerCol = 4.5;

    let blueDist = 0, redDist = 0;
    if (blueCount > 0) {
        const dr = blueSumRow / blueCount - centerRow;
        const dc = blueSumCol / blueCount - centerCol;
        blueDist = dr * dr + dc * dc;
    }
    if (redCount > 0) {
        const dr = redSumRow / redCount - centerRow;
        const dc = redSumCol / redCount - centerCol;
        redDist = dr * dr + dc * dc;
    }

    return { blueDist, redDist };
}

function evaluatePosition(gameState) {
    if (gameState.gameOver !== null) {
        return gameState.gameOver * 10000;
    }

    let score = gameState.material;

    // Orangutan distance to center
    const distances = getOrangutanDistances(gameState.board);
    score += (distances.redDist - distances.blueDist) * 0.5;

    return score;
}

// Transposition Table
const transpositionTable = new Map();
const TT_EXACT = 0;
const TT_LOWER = 1;
const TT_UPPER = 2;

function minimax(gameState, depth, maximize, alpha, beta) {
    if (gameState.gameOver !== null) {
        return gameState.gameOver * 10000;
    }

    if (depth === 0) {
        return evaluatePosition(gameState);
    }

    // Simplified hashing 
    // Ideally use Zobrist, but passing hash down is complex without class. 
    // We'll skip TT for this port to keep it robust and simple, or use simple board string key.
    // Given JS speed, string key is slow.
    // Let's implement a poor man's key: 
    // Just use material + turn + piece count? Collisions likely.

    // For now, disabling TT to avoid bugs in porting. Depth 3 will still be fast enough.

    let moves = generateMoves(gameState);

    if (moves.length === 0) {
        return maximize ? -9999 : 9999;
    }

    // Sort moves: winning moves first, then by material
    moves.sort((a, b) => {
        if (a.gameOver !== null && b.gameOver === null) return -1;
        if (a.gameOver === null && b.gameOver !== null) return 1;
        return maximize ? b.material - a.material : a.material - b.material;
    });

    let best;

    if (maximize) {
        best = -Infinity;
        for (const childState of moves) {
            const val = minimax(childState, depth - 1, false, alpha, beta);
            best = Math.max(best, val);
            alpha = Math.max(alpha, val);
            if (beta <= alpha) break;
        }
    } else {
        best = Infinity;
        for (const childState of moves) {
            const val = minimax(childState, depth - 1, true, alpha, beta);
            best = Math.min(best, val);
            beta = Math.min(beta, val);
            if (beta <= alpha) break;
        }
    }

    return best;
}

export function findBestMove(gameState, depth = 3) {
    const moves = generateMoves(gameState);
    if (moves.length === 0) return { move: null, value: 0 };

    // Check for immediate winning move
    for (const moveState of moves) {
        if (moveState.gameOver !== null) {
            if ((gameState.blueToMove && moveState.gameOver === 1) ||
                (!gameState.blueToMove && moveState.gameOver === -1)) {
                const winValue = gameState.blueToMove ? 100000 : -100000;
                return { move: moveState.move, value: winValue };
            }
        }
    }

    moves.sort((a, b) => {
        const aWins = (gameState.blueToMove && a.gameOver === 1) || (!gameState.blueToMove && a.gameOver === -1);
        const bWins = (gameState.blueToMove && b.gameOver === 1) || (!gameState.blueToMove && b.gameOver === -1);
        if (aWins && !bWins) return -1;
        if (!aWins && bWins) return 1;
        return gameState.blueToMove ? b.material - a.material : a.material - b.material;
    });

    let bestMove = null;
    let bestValue = gameState.blueToMove ? -Infinity : Infinity;

    for (const moveState of moves) {
        const moveValue = minimax(moveState, depth - 1, !gameState.blueToMove, -Infinity, Infinity);

        if (gameState.blueToMove) {
            if (moveValue > bestValue) {
                bestValue = moveValue;
                bestMove = moveState.move;
            }
        } else {
            if (moveValue < bestValue) {
                bestValue = moveValue;
                bestMove = moveState.move;
            }
        }
    }

    return { move: bestMove, value: bestValue };
}
