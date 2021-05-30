let table = document.querySelector("table")
let cells = document.querySelectorAll("td")

// To Trace the Shaded Cells
let selected = null
let turn = document.querySelector("table").getAttribute("data-turn")

for (let i = 0; i < 8; i++) {
    for (let j = 0; j < 8; j++) {
        cells[(i * 8) + j].addEventListener("click", function (event) {

            // If the Selected cell wasn't selected or no cells are selected
            if (selected == null) {
                // Remove shadows from the cells
                removeGreen()
                // Get the posible moves for the selected cell
                getMoves(event, i, j)
            }
            else if (selected[0] != i || selected[1] != j) {
                if (event.currentTarget.classList.contains("green")) {
                    let xhttp = new XMLHttpRequest()
                    xhttp.onreadystatechange = function () {
                        if (this.readyState == 4 && this.status == 200) {
                            console.log(this.response)
                            // Get All classes from old cell to the new cell
                            let classes = cells[selected[0] * 8 + selected[1]].querySelector("i").getAttribute("class")
                            cells[selected[0] * 8 + selected[1]].querySelector("i").removeAttribute("class")
                            cells[i * 8 + j].querySelector("i").setAttribute("class", classes)
                            // Remove Shadows from all cells
                            removeGreen()
                            check_end(this.response)
                            turn = (turn == 'White') ? 'Black' : 'White'
                        }
                    }
                    xhttp.open("POST", "/make_move")
                    xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
                    xhttp.send("&x1=" + selected[0] + "&y1=" + selected[1] + "&x2=" + i + "&y2=" + j)
                } else if (event.currentTarget.classList.contains("purple")) {
                    let xhttp = new XMLHttpRequest()
                    xhttp.onreadystatechange = function () {
                        if (this.readyState == 4 && this.status == 200) {
                            console.log(this.response)
                            if (selected[0] == 0) {
                                king1 = 4
                                if (j == 2) {
                                    king2 = 2
                                    rook1 = 0
                                    rook2 = 3
                                }
                                else {
                                    king2 = 2
                                    rook1 = 7
                                    rook2 = 5
                                }
                            }
                            else {
                                king1 = 60
                                if (j == 2) {
                                    king2 = 58
                                    rook1 = 56
                                    rook2 = 59
                                }
                                else {
                                    king2 = 62
                                    rook1 = 63
                                    rook2 = 61
                                }
                            }
                            // The King
                            let classes = cells[king1].querySelector("i").getAttribute("class")
                            cells[king1].querySelector("i").removeAttribute("class")
                            cells[king2].querySelector("i").setAttribute("class", classes)
                            // The Rook
                            classes = cells[rook1].querySelector("i").getAttribute("class")
                            cells[rook1].querySelector("i").removeAttribute("class")
                            cells[rook2].querySelector("i").setAttribute("class", classes)
                            // results = JSON.parse(this.response)
                            // Remove Shadows from all cells
                            removeGreen()
                            check_end(this.response)
                            turn = (turn == 'White') ? 'Black' : 'White'
                        }
                    }
                    xhttp.open("POST", "/make_castle")
                    xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
                    xhttp.send("&x1=" + selected[0] + "&y1=" + selected[1] + "&x2=" + i + "&y2=" + j)
                } else if (event.currentTarget.classList.contains("yellow")) {
                    let modal = document.querySelector("#promation")
                    modal.setAttribute("data-i", i)
                    modal.setAttribute("data-j", j)
                    /*
                    ** ****************** **
                    ** If the Pawn reched the end then show a modal that askes for the promation
                    ** ****************** **
                    */
                    $("#promation").modal('show')
                    buttons = modal.querySelectorAll("button")
                    for (let k = 0, len = buttons.length; k < len; k++) {
                        buttons[k].addEventListener("click", promation)
                    }
                } else {
                    removeGreen()
                    getMoves(event, i, j)
                }
            } else {
                removeGreen()
            }
        })
    }
}

/*
** Get Posible moves for Selected cell
*/
function getMoves(event, i, j) {
    let player = (turn == 'White') ? 'white-peice' : 'black-peice'
    if (event.currentTarget.querySelector('i').classList.length != 0
        && event.currentTarget.querySelector('i').classList.contains(player)) {
        let xhttp = new XMLHttpRequest()
        xhttp.onreadystatechange = function () {
            if (this.readyState == 4 && this.status == 200) {
                results = JSON.parse(this.response)
                console.log(results)
                if (results.length != 0) {
                    for (let k = 0, len = results.length; k < len; k++) {
                        // Check if Can Castle
                        if (results[k][0] == 'Castle') {
                            x = results[k][1][0]
                            y = results[k][1][1]
                            cells[(x * 8) + y].classList.add("purple")
                            if (results[k].length == 3) {
                                x = results[k][2][0]
                                y = results[k][2][1]
                                cells[(x * 8) + y].classList.add("purple")
                            }
                        } else if (results[k][0] == 'Upgrade') {
                            x = results[k][1][0]
                            y = results[k][1][1]
                            cells[(x * 8) + y].classList.add("yellow")
                        } else {
                            x = results[k][0]
                            y = results[k][1]
                            // Add shadows to the posible moves cells
                            cells[(x * 8) + y].classList.add("green")
                        }
                    }
                    // Mark the cell as selected cell
                    selected = [i, j]
                }
            }
        }
        xhttp.open("POST", "/get_moves", true);
        xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
        xhttp.send("&x=" + i + "&y=" + j)
    }
}

/*
** Control Pawn Promation
*/
function promation(event) {
    let name = event.currentTarget.getAttribute('data-name')
    let modal = document.querySelector("#promation")
    let i = parseInt(modal.getAttribute("data-i"))
    let j = parseInt(modal.getAttribute("data-j"))
    let xhttp = new XMLHttpRequest()
    xhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            console.log("Checked")
            console.log(this.response)
            // Get All classes
            let classes = cells[selected[0] * 8 + selected[1]].querySelector("i").getAttribute("class")
            cells[selected[0] * 8 + selected[1]].querySelector("i").removeAttribute("class")
            cells[i * 8 + j].querySelector("i").setAttribute("class", classes)
            // Change fa-chess-pawn to fa-chess-{Selected Peice}
            cells[i * 8 + j].querySelector("i").classList.remove("fa-chess-pawn")
            cells[i * 8 + j].querySelector("i").classList.add("fa-chess-" + name)
            // Remove Shadows from all cells
            removeGreen()
            $('#promation').modal('hide')
            check_end(this.response)
            turn = (turn == 'White') ? 'Black' : 'White'
        }
    }
    xhttp.open("POST", "/promation")
    xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhttp.send("&x1=" + selected[0] + "&y1=" + selected[1] + "&x2=" + i + "&y2=" + j + "&name=" + name)
    for (let t = 0; t < 5; t++) {
        buttons[t].removeEventListener('click', promation)
    }
}

/*
** Remove All shadows
*/
function removeGreen() {
    for (let k = 0; k < 64; k++) {
        cells[k].classList.remove("green")
        cells[k].classList.remove("purple")
        cells[k].classList.remove("yellow")
    }
    selected = null
}

function check_end(response) {
    if (response == 'Ended') {
        let modal = document.querySelector("#ended")
        let winner = (turn == 'White') ? '1' : '2'
        modal.querySelector(".winner").innerHTML = "Player " + winner + " won!"
        $('#ended').modal('show')
    }
}

