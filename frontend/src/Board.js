import React, { useState, useEffect } from 'react';
import Square from './Square';
import { fenToBoardArray, coordsToAlgebraic } from './fenUtils';
import './Board.css';

const getTurn = (fen) => {
    const parts = fen.split(' ');
    return parts.length > 1 ? parts[1] : 'w';
}

const isPlayersPiece = (pieceChar, fen) => {
    if (!pieceChar) return false;
    const turn = getTurn(fen);
    if (turn === 'w') {
        return pieceChar === pieceChar.toUpperCase();
    } else {
        return pieceChar === pieceChar.toLowerCase();
    }
}

function Board() {
    const [boardArray, setBoardArray] = useState(Array(8).fill(Array(8).fill(null)));
    const [fen, setFen] = useState('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1');
    const [selectedSquare, setSelectedSquare] = useState(null);

    const [orientation, setOrientation] = useState('white');

    useEffect(() => {
        const fetchBoard = () => {
             fetch('/api/board')
                .then(res => res.json())
                .then(data => {
                    const fenString = data.fen;
                    setFen(fenString);
                    setBoardArray(fenToBoardArray(fenString));
                })
                .catch(error => console.error('Error fetching FEN:', error));
        }

        fetchBoard();
    }, []);

    const handleSquareClick = (squareAlgebraic, pieceChar) => {
        if (selectedSquare) {
            const move = `${selectedSquare}${squareAlgebraic}`;
            const promotionMove = move + 'q';

            if (squareAlgebraic === selectedSquare) {
                setSelectedSquare(null);
                return;
            }

            fetch('/api/move', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ move_uci: move.length === 4 ? move : promotionMove }),
            })
            .then(res => res.json())
            .then(data => {
                // Check for 'success' status from FastAPI response
                if (data.status === 'success') {
                    // Use 'fen' from FastAPI response
                    setFen(data.fen);
                    setBoardArray(fenToBoardArray(data.fen));
                } else {
                    // FastAPI returns a 400 response on illegal move, but if we catch it here it will be a non-ok fetch response.
                    // If the response is OK but the move failed logically (which shouldn't happen with the FastAPI structure):
                    console.error("Illegal move or server error:", data);
                }
            })
            .catch(error => console.error('Error sending move:', error));

            setSelectedSquare(null);
            return;
        }

        if (pieceChar && isPlayersPiece(pieceChar, fen)) {
            setSelectedSquare(squareAlgebraic);
        }
    }

    const getBoardLayout = () => {
        let rows = boardArray.map((row, rowIndex) => ({ row, rowIndex }));

        if (orientation === 'black') {
            rows = rows.reverse();
        }

        return rows.flatMap(({ row, rowIndex }) => {
            let cols = row.map((pieceChar, colIndex) => ({ pieceChar, colIndex }));

            return cols.map(({ pieceChar, colIndex }) => {
                const algebraic = coordsToAlgebraic(rowIndex, colIndex);

                return (
                    <Square
                        key={algebraic}
                        isLight={isLight(rowIndex, colIndex)}
                        pieceChar={pieceChar}
                        onClick={() => handleSquareClick(algebraic, pieceChar)}
                        isSelected={selectedSquare === algebraic}
                    />
                );
            });
        });
    }

    const isLight = (row, col) => (row + col) % 2 === 0;

    return (
        <div className="chessboard-container">
            <div className="fen-display">{fen}</div>
            <div className="chessboard">
                {getBoardLayout()}
            </div>
            <button
                onClick={() => setOrientation(orientation === 'white' ? 'black' : 'white')}
                className="mt-4 p-2 bg-gray-200 rounded shadow hover:bg-gray-300 transition duration-150"
            >
                Flip Board
            </button>
        </div>
    );
}

export default Board;
