const socket = io("/game")
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

    addAction(type, result) {
        let move = {}
        // Unpack Results
        let x2 = result[1][0]
        let y2 = result[1][1]

        move['x2'] = x2
        move['y2'] = y2
        move['type'] = type
        move['coor'] = String(x2) + String(y2)
        move['make'] = function () { sendAction(type, result) }

        this.moves.push(move)
    }

    makeAction(x2, y2) {
        for (let i = 0, len = this.moves.length; i < len; i++) {
            if (this.moves[i]['coor'] == String(x2) + String(y2)) {
                this.moves[i].make()
                break
            }
        }
    }

    showAction() {
        for (let i = 0, len = this.moves.length; i < len; i++) {
            let x2 = this.moves[i]['x2']
            let y2 = this.moves[i]['y2']
            if (this.moves[i]['type'] == "move") {
                showAction(x2 * 8 + y2, 'green')
            } else if (this.moves[i].type == "promation") {
                showAction(x2 * 8 + y2, 'yellow')
            } else {
                showAction(x2 * 8 + y2, 'purple')
            }
        }
    }

    resetAction() {
        this.moves = []
    }
}

let data = {}
let selected = null
for (let i = 0; i < 8; i++) {
    for (let j = 0; j < 8; j++) {
        data[i * 8 + j] = new Cell(i, j)
        cells[i * 8 + j].addEventListener("click", function (event) {
            // No selected Cell
            if (selected == null) {
                data[(i * 8 + j)].showAction()
                selected = [i, j]
            }

            // Current Selected Cell
            else if (selected[0] == i && selected[1] == j) {
                removeAction()
            }

            // Cell that can make a move
            else if (event.currentTarget.classList.contains("can-move")) {
                data[(selected[0] * 8) + selected[1]].makeAction(i, j)
                removeAction()
            }

            // An Empty or another Cell
            else {
                removeAction()
                data[(i * 8 + j)].showAction()
                selected = [i, j]
            }
        })
    }
}

socket.on("update_action", function (response) {
    console.log(response)
    // Remove Check Mate Alert
    for (let i = 0; i < 64; i++) {
        cells[i].classList.remove('red')
    }
    // Add Moves to Cell
    for (let i = 0, len = response.length; i < len; i++) {
        let result = response[i]
        let type = Object.keys(result)[0]
        let x1 = result[type][0][0]
        let y1 = result[type][0][1]
        data[x1 * 8 + y1].addAction(type, result[type])
    }
})

socket.on("make_action", function (response) {
    let type = Object.keys(response)[0]
    let result = response[type]
    let cell1 = (result[0][0] * 8) + result[0][1]
    let cell2 = (result[1][0] * 8) + result[1][1]
    // Move the peice
    pieceMove(cell1, cell2)
    cells[cell1].classList.add("yellow-border")
    cells[cell2].classList.add("red-border")

    // If Action is Castle move the Rook
    if (type == "castle") {
        let cell3 = (result[2][0] * 8) + result[2][1]
        let cell4 = (result[3][0] * 8) + result[3][1]
        pieceMove(cell3, cell4)
    }
    // If Action is Promation
    else if (type == "promation") {
        let name = response['name']
        // Change fa-chess-pawn to fa-chess-{Selected Peice}
        cells[cell2].querySelector("i").classList.remove("fa-chess-pawn")
        cells[cell2].querySelector("i").classList.add("fa-chess-" + name)
    }
})

socket.on("check_mate", function (response) {
    // Add red Alert if check mate
    let cell = (response['king'][0] * 8) + response['king'][1]
    showAction(cell, "red")
})

socket.on("end_game", function (msg) {
    console.log(msg)
    if (msg['winner'] == color) {
        $('#win').modal("show")
    } else if (msg['winner'] == 'Tie') {
        $('#tie').modal("show")
    } else {
        $('#lose').modal("show")
    }
    setTimeout(function () {
        location.href = "/"
    }, 3000)
})

socket.on('oppo_disconnect', function (msg) {
    document.querySelector("#disconnected p").innerHTML = msg
    $("#disconnected").modal("show")
    setTimeout(function () {
        location.href = "/"
    }, 3000)
})

/*
** A function that make and send Action
*/
function sendAction(type, result) {
    let cell1 = (result[0][0] * 8) + result[0][1]
    let cell2 = (result[1][0] * 8) + result[1][1]
    // Move the peice
    pieceMove(cell1, cell2)
    removeAction()
    cells[cell1].classList.add("yellow-border")
    cells[cell2].classList.add("red-border")
    // If Action is simple move
    if (type == "move") {
        socket.emit("make_action", { "move": result })
    }
    // If Action is Castle Move the Rook
    else if (type == "castle") {
        let cell3 = (result[2][0] * 8) + result[2][1]
        let cell4 = (result[3][0] * 8) + result[3][1]
        pieceMove(cell3, cell4)
        console.log("Made Castle")
        // Send Data
        socket.emit("make_action", { "castle": result })
    }
    // If action is promation
    else {
        console.log("Promating")
        $('#promation').modal('show')
        let div = document.querySelector("#promation")
        let promat = setInterval(function () {
            if (div.getAttribute("data-name") != "") {
                let name = div.getAttribute("data-name")
                // Change fa-chess-pawn to fa-chess-{Selected Peice}
                cells[cell2].querySelector("i").classList.remove("fa-chess-pawn")
                cells[cell2].querySelector("i").classList.add("fa-chess-" + name)
                div.setAttribute("data-name", "")
                $('#promation').modal('hide')
                // Send Data
                socket.emit("make_action", { "promation": result, "name": name })
                clearInterval(promat)
            }
        }, 100)
    }

    // Reset Actions and Remove Check Mate Alert
    for (let i = 0; i < 64; i++) {
        cells[i].classList.remove('red')
        data[i].resetAction()
    }
}

/*
** A function that move Piece
*/
function pieceMove(cell1, cell2) {
    let classes = cells[cell1].querySelector("i").getAttribute("class")
    cells[cell1].querySelector("i").removeAttribute("class")
    cells[cell2].querySelector("i").setAttribute("class", classes)
}

/*
** Assign clicked button value to Main Div
*/
function promation(name) {
    document.querySelector("#promation").setAttribute("data-name", name)
}

/*
** A function to show move
*/
function showAction(cell, classes) {
    cells[cell].classList.add(classes)
    cells[cell].classList.add('can-move')
}

/*
** A function that remove all highlights
*/
function removeAction() {
    for (let i = 0; i < 64; i++) {
        cells[i].classList.remove('green')
        cells[i].classList.remove('yellow')
        cells[i].classList.remove('purple')
        // cells[i].classList.remove('red')
        cells[i].classList.remove('can-move')
        cells[i].classList.remove('yellow-border')
        cells[i].classList.remove('red-border')
    }
    selected = null
}

/*
** Change Player Turn
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