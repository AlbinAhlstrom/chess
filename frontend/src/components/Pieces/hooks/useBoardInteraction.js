import { useState, useCallback, useRef, useEffect } from 'react';
import { coordsToAlgebraic, algebraicToCoords } from '../../../helpers';

export function useBoardInteraction(isFlipped, position, allPossibleMoves, canMovePiece, onMoveAttempt) {
    const [selectedSquare, setSelectedSquare] = useState(null);
    const [legalMoves, setLegalMoves] = useState([]);
    const dragStartSelectionState = useRef(false);
    const ref = useRef(null);
    const highlightRef = useRef(null);

    // Clear selection when position changes (move made)
    useEffect(() => {
        setSelectedSquare(null);
        setLegalMoves([]);
    }, [position]);

    const calculateSquare = useCallback(e => {
        if (!ref.current) return null;
        const { width, left, top } = ref.current.getBoundingClientRect();
        
        // Handle both MouseEvent/TouchEvent and custom objects {clientX, clientY}
        const clientX = e.clientX ?? (e.touches?.[0]?.clientX) ?? (e.changedTouches?.[0]?.clientX);
        const clientY = e.clientY ?? (e.touches?.[0]?.clientY) ?? (e.changedTouches?.[0]?.clientY);

        if (clientX === undefined || clientY === undefined) return null;

        const size = width / 8;
        let file = Math.floor((clientX - left) / size);
        let rank = Math.floor((clientY - top) / size);
        
        if (isFlipped) {
            file = 7 - file;
            rank = 7 - rank;
        }
        
        return { file, rank, algebraic: coordsToAlgebraic(file, rank) };
    }, [isFlipped]);

    const updateLegalMoves = useCallback((square, pieceColor) => {
        if (canMovePiece(pieceColor)) {
            const moves = allPossibleMoves.filter(m => m.startsWith(square));
            setLegalMoves(moves);
        } else {
            setLegalMoves([]); // Opponents get no dots
        }
    }, [allPossibleMoves, canMovePiece]);

    // Handle Drag Start - Selects the piece immediately
    const handlePieceDragStart = useCallback(({ file, rank, piece }) => {
        const square = coordsToAlgebraic(file, rank);
        const pieceColor = piece === piece.toUpperCase() ? 'w' : 'b';
        
        // Record if it was already selected before this interaction started
        dragStartSelectionState.current = (selectedSquare === square);

        // Always select, even if opponent (requirement 6)
        setSelectedSquare(square);
        updateLegalMoves(square, pieceColor);
    }, [updateLegalMoves, selectedSquare]);

    const handleSquareClick = useCallback((e) => {
        const squareData = calculateSquare(e);
        if (!squareData) return;
        const { file, rank, algebraic: clickedSquare } = squareData;

        const pieceChar = (r, f) => {
            if (r < 0 || r > 7 || f < 0 || f > 7) return null;
            return position[r][f];
        };
        const piece = pieceChar(rank, file);

        if (selectedSquare) {
            // Same piece -> Deselect
            if (clickedSquare === selectedSquare) {
                setSelectedSquare(null);
                setLegalMoves([]);
                return;
            }

            // Legal Move -> Execute
            const movesToTarget = legalMoves.filter(m => m.slice(2, 4) === clickedSquare);
            if (movesToTarget.length > 0) {
                onMoveAttempt(selectedSquare, clickedSquare, movesToTarget);
                return;
            }

            // Another piece -> Switch Selection
            if (piece) {
                setSelectedSquare(clickedSquare);
                const pieceColor = piece === piece.toUpperCase() ? 'w' : 'b';
                updateLegalMoves(clickedSquare, pieceColor);
                return;
            }

            // Empty square -> Deselect
            setSelectedSquare(null);
            setLegalMoves([]);
        } else {
            // No selection -> Select piece if clicked
            if (piece) {
                setSelectedSquare(clickedSquare);
                const pieceColor = piece === piece.toUpperCase() ? 'w' : 'b';
                updateLegalMoves(clickedSquare, pieceColor);
            }
        }
    }, [calculateSquare, position, selectedSquare, legalMoves, updateLegalMoves, onMoveAttempt]);

    const handleManualDrop = useCallback(({ clientX, clientY, file, rank }) => {
        if (highlightRef.current) highlightRef.current.style.display = 'none';
        
        const squareData = calculateSquare({ clientX, clientY });
        if (!squareData) return;
        const { algebraic: toSquare } = squareData;
        const fromSquare = coordsToAlgebraic(file, rank);

        // "Dragging a piece and dropping it back to its initial square counts as clicking"
        if (fromSquare === toSquare) {
            if (dragStartSelectionState.current) {
                // It was already selected -> Deselect (counts as second click)
                setSelectedSquare(null);
                setLegalMoves([]);
            } else {
                // It wasn't selected -> Keep selected (it was selected in DragStart)
            }
            return;
        }

        const movesToTarget = allPossibleMoves.filter(m => m.startsWith(fromSquare) && m.slice(2, 4) === toSquare);
        if (movesToTarget.length > 0) {
            // Move is valid
            onMoveAttempt(fromSquare, toSquare, movesToTarget);
        } else {
            // Invalid drop -> treat as click on target square (switch/deselect)
            handleSquareClick({ clientX, clientY });
        }
    }, [calculateSquare, allPossibleMoves, onMoveAttempt, handleSquareClick]);

    const handlePieceDragHover = useCallback((clientX, clientY) => {
        if (!highlightRef.current) return;
        
        if (!clientX || !clientY) {
            highlightRef.current.style.display = 'none';
            return;
        }
        const squareData = calculateSquare({ clientX, clientY });
        if (!squareData) return;
        const { file, rank } = squareData;
        
        if (file >= 0 && file <= 7 && rank >= 0 && rank <= 7) {
            highlightRef.current.style.display = 'block';
            
            let displayFile = isFlipped ? 7 - file : file;
            let displayRank = isFlipped ? 7 - rank : rank;

            highlightRef.current.style.left = `calc(${displayFile} * var(--square-size))`;
            highlightRef.current.style.top = `calc(${displayRank} * var(--square-size))`;
            
            const isDark = (file + rank) % 2 !== 0;
            highlightRef.current.style.border = isDark 
                ? '5px solid var(--drag-hover-dark-border)' 
                : '5px solid var(--drag-hover-light-border)';
        } else {
            highlightRef.current.style.display = 'none';
        }
    }, [calculateSquare, isFlipped]);

    return {
        selectedSquare, setSelectedSquare,
        legalMoves, setLegalMoves,
        ref, highlightRef,
        handleSquareClick,
        handlePieceDragStart,
        handlePieceDragHover,
        handleManualDrop
    };
}