import './Board.css'
import { fileIntToString } from '../helpers.js'

const Board = () => {
    const ranks = Array(8).fill().map((x, i) => 8-i)
    const files = Array(8).fill().map((x, i) => fileIntToString(i))

    return <div className="board">
        {ranks.map((rank, i) =>
            files.map((file, j) =>
                <div>{file}{rank}</div>)
        )
        }
    </div>
}

export default Board
