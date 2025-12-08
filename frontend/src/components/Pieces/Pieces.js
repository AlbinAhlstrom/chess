import './Pieces.css'
import Piece from './Piece'
import { fenToPosition } from '../../helpers.js' 

const fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1";

function Pieces() {
    const position = fenToPosition(fen); 

    return (
        <div className="pieces">
            {position.map((rankArray, rankIndex) =>
                rankArray.map((pieceType, fileIndex) => 
                    pieceType 
                        ? <Piece 
                            key={`p-${rankIndex}-${fileIndex}`} 
                            rank={rankIndex}
                            file={fileIndex}
                            piece={pieceType}
                          />
                        : null
                )
            )}
        </div>
    );
}

export default Pieces;
