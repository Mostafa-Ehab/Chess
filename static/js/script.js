const socket = io("/game")
// socket.emit('move', 'get')
const color = (document.querySelector("table").classList.contains('white-board')) ? 'White' : 'Black'
let turn = (color == 'White') ? true : false
changeTurn(turn)
let cells = document.querySelectorAll("td")

class Cell {
    constructor(x, y) {
        this.x = x
        this.y = y
        this.moves = []
    }

    addMoves(type, result) {
        // Set Moves Object
        let move = {}
        if (type == 'move') {
            // Unpack Results
            let x1 = result[0][0]
            let y1 = result[0][1]
            let x2 = result[1][0]
            let y2 = result[1][1]

            move['type'] = 'move'
            move['coor'] = String(x2) + String(y2)
            move['show'] = function () { showMove((x2 * 8) + y2, 'green') }
            move['make'] = function () { makeMove((x1 * 8) + y1, (x2 * 8) + y2) }
            move['send'] = { 'move': [[x1, y1], [x2, y2]] }

        } else if (type == 'promation') {
            // Unpack Results
            let x1 = result[0][0]
            let y1 = result[0][1]
            let x2 = result[1][0]
            let y2 = result[1][1]

            move['type'] = 'promation'
            move['coor'] = String(x2) + String(y2)
            move['show'] = function () { showMove((x2 * 8) + y2, 'yellow') }
            move['make'] = function () {
                makeMove((x1 * 8) + y1, (x2 * 8) + y2)
                /*
                ** Show Modal that ask for the Promation
                */
                $("#promation").modal('show')
                let modal = document.querySelector("#promation")
                modal.setAttribute("data-x1", x1)
                modal.setAttribute("data-y1", y1)
                modal.setAttribute("data-x2", x2)
                modal.setAttribute("data-y2", y2)

                let buttons = modal.querySelectorAll("button")
                for (let k = 0, len = buttons.length; k < len; k++) {
                    buttons[k].addEventListener("click", promation)
                }
            }
            move['send'] = { 'promation': [[x1, y1], [x2, y2]] }

        } else if (type == 'castle') {
            // Unpack Results
            let kx1 = result[0][0]
            let ky1 = result[0][1]
            let kx2 = result[1][0]
            let ky2 = result[1][1]
            let rx1 = result[2][0]
            let ry1 = result[2][1]
            let rx2 = result[3][0]
            let ry2 = result[3][1]


            move['type'] = 'castle'
            move['coor'] = String(kx2) + String(ky2)
            move['show'] = function () { showMove((kx2 * 8) + ky2, 'purple') }
            move['make'] = function () {
                makeMove((kx1 * 8) + ky1, (kx2 * 8) + ky2)
                makeMove((rx1 * 8) + ry1, (rx2 * 8) + ry2)
            }
            move['send'] = { 'castle': [[kx1, ky1], [kx2, ky2]] }
        }
        // Push Object to the Array
        this.moves.push(move)
    }

    resetMoves() {
        this.moves = []
    }

    showMoves() {
        for (let i = 0, len = this.moves.length; i < len; i++) {
            this.moves[i].show()
        }
    }

    makeMoves(x, y) {
        for (let i = 0, len = this.moves.length; i < len; i++) {
            if (this.moves[i]['coor'] == String(x) + String(y)) {
                this.moves[i].make()
                if (this.moves[i]['type'] == 'move' || this.moves[i]['type'] == 'castle') {
                    socket.emit('make_move', this.moves[i].send)
                }
            }
        }
        changeTurn(false)
        removeMoves()
    }
}

let data = {}
let selected = null
for (let i = 0; i < 8; i++) {
    for (let j = 0; j < 8; j++) {
        data[(i * 8) + j] = new Cell(i, j)
        cells[(i * 8) + j].addEventListener("click", function (event) {
            // No selected Cell
            if (selected == null) {
                data[(i * 8 + j)].showMoves()
                selected = [i, j]

                // Current Selected Cell
            } else if (selected[0] == i && selected[1] == j) {
                removeMoves()
            }

            // Cell that can make a move
            else if (event.currentTarget.classList.contains("can-move")) {
                data[(selected[0] * 8) + selected[1]].makeMoves(i, j)
                removeMoves()
            }

            // An Empty or another Cell
            else {
                removeMoves()
                data[(i * 8 + j)].showMoves()
                selected = [i, j]
            }
        })
    }
}

/*
** A function that Responsible for Updating move list from server
*/
socket.on('update_moves', function (results) {
    console.log(results)
    for (let i = 0; i < 64; i++) {
        data[i].resetMoves()
    }
    for (let r = 0, len = results.length; r < len; r++) {
        if (results[r]['color'] == color && turn == true) {
            let result = results[r]
            let type = Object.keys(result)[0]
            let i = result[type][0][0]
            let j = result[type][0][1]
            data[(i * 8) + j].addMoves(type, result[type])
        }
    }
})

socket.on('make_move', function (result) {
    console.log(result)
    let type = Object.keys(result)[1]
    if (result['color'] != color) {
        if (type == 'move') {
            // Unpack Results
            let x1 = result['move'][0][0]
            let y1 = result['move'][0][1]
            let x2 = result['move'][1][0]
            let y2 = result['move'][1][1]
            makeMove(((x1 * 8) + y1), ((x2 * 8) + y2))
        } else if (type == 'promation') {
            // Unpack Results
            let x = result['promation'][0]
            let y = result['promation'][1]
            let name = result['promation'][2]

            // Change fa-chess-pawn to fa-chess-{Selected Peice}
            cells[(x * 8) + y].querySelector("i").classList.remove("fa-chess-pawn")
            cells[(x * 8) + y].querySelector("i").classList.add("fa-chess-" + name)
        }
        changeTurn(true)
    }
})

socket.on('check', function (king) {
    console.log(king)
    let i = king['king'][0]
    let j = king['king'][1]

    cells[(i * 8) + j].classList.add("red")
})

socket.on('Oppo_Disconnect', function (msg) {
    document.querySelector("#disconnected p").innerHTML = msg
    $("#disconnected").modal("show")
    setTimeout(function () {
        location.href = "/waiting"
    }, 2000)
})

socket.on("end_game", function (msg) {
    console.log(msg)
    if (msg == color) {
        $('#win').modal("show")
    } else if (msg == 'Tie') {
        $('#tie').modal("show")
    } else {
        $('#lose').modal("show")
    }
    setTimeout(function () {
        location.href = "/waiting"
    }, 2000)
})

/*
** A function to move Peice
** cell1 => The cell to move from
** cell2 => The cell to move to
*/
function makeMove(cell1, cell2) {
    let classes = cells[cell1].querySelector("i").getAttribute("class")
    cells[cell1].querySelector("i").removeAttribute("class")
    cells[cell2].querySelector("i").setAttribute("class", classes)
    removeMoves()
}

/*
** A function to show move
** cell => The cell to color
** clss => The class to add
*/
function showMove(cell, classes) {
    cells[cell].classList.add(classes)
    cells[cell].classList.add('can-move')
}

/*
** A function that remove all highlights
*/
function removeMoves() {
    for (let i = 0; i < 64; i++) {
        cells[i].classList.remove('green')
        cells[i].classList.remove('yellow')
        cells[i].classList.remove('purple')
        cells[i].classList.remove('red')
        cells[i].classList.remove('can-move')
    }
    selected = null
}

/*
** A function that responsible for Promation
*/
function promation(event) {
    let name = event.currentTarget.getAttribute('data-name')
    let modal = document.querySelector("#promation")
    let x1 = parseInt(modal.getAttribute("data-x1"))
    let y1 = parseInt(modal.getAttribute("data-y1"))
    let x2 = parseInt(modal.getAttribute("data-x2"))
    let y2 = parseInt(modal.getAttribute("data-y2"))

    // Change fa-chess-pawn to fa-chess-{Selected Peice}
    cells[(x2 * 8) + y2].querySelector("i").classList.remove("fa-chess-pawn")
    cells[(x2 * 8) + y2].querySelector("i").classList.add("fa-chess-" + name)

    // Send Data To the server
    let move = { 'promation': [[x1, y1], [x2, y2]], 'name': name }
    socket.emit('make_move', move)

    // Remove Event Listener
    let buttons = modal.querySelectorAll("button")
    for (let i = 0; i < 5; i++) {
        buttons[i].removeEventListener('click', promation)
    }
    $('#promation').modal('hide')
}

/*
** Change Turn
*/
function changeTurn(bool) {
    if (bool == true) {
        document.querySelectorAll("h1")[1].style.display = 'None'
        document.querySelectorAll("h1")[0].style.display = 'Block'
    } else {
        document.querySelectorAll("h1")[0].style.display = 'None'
        document.querySelectorAll("h1")[1].style.display = 'Block'
    }
    turn = bool
}
