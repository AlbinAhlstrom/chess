export const fenToBoardArray = (fen) => {
    const [piecesPlacement] = fen.split(' ');
    const ranks = piecesPlacement.split('/');
    const boardArray = [];

    ranks.forEach(rank => {
        const row = [];
        for (let i = 0; i < rank.length; i++) {
            const char = rank[i];

            if (/\d/.test(char)) {
                const emptySquares = parseInt(char, 10);
                for (let j = 0; j < emptySquares; j++) {
                    row.push(null);
                }
            }
            else {
                row.push(char);
            }
        }
        boardArray.push(row);
    });

    return boardArray;
}

export const getPieceImagePath = (pieceChar) => {
    if (!pieceChar || !PIECE_IMAGE_MAP[pieceChar]) {
        return null;
    }
    return `/images/pieces/${PIECE_IMAGE_MAP[pieceChar]}`;
}

export const coordsToAlgebraic = (rowIndex, colIndex) => {
    const file = String.fromCharCode('a'.charCodeAt(0) + colIndex);
    const rank = 8 - rowIndex;
    return `${file}${rank}`;
}

export const algebraicToCoords = (algebraic) => {
    const file = algebraic.charCodeAt(0) - 'a'.charCodeAt(0);
    const rank = 8 - parseInt(algebraic[1], 10);
    return [rank, file];
}

const PIECE_IMAGE_MAP = {
    'p': 'black-pawn.png', 'n': 'black-knight.png', 'b': 'black-bishop.png',
    'r': 'black-rook.png', 'q': 'black-queen.png', 'k': 'black-king.png',

    'P': 'white-pawn.png', 'N': 'white-knight.png', 'B': 'white-bishop.png',
    'R': 'white-rook.png', 'Q': 'white-queen.png', 'K': 'white-king.png',
};
