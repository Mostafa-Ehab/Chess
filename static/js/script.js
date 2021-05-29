let table = document.querySelector("table")
let cells = document.querySelectorAll("td")

// To Trace the Shaded Cells
let selected = null

for (let i = 0; i < 8; i++) {
    for (let j = 0; j < 8; j++) {
        cells[(i * 8) + j].addEventListener("click", function (event) {

            /*
            ** If the Selected cell wasn't selected or no cells are selected
            */
            if (selected == null) {
                /*
                ** Get the posible moves for the selected cell
                */
                // Remove shadows from the cells
                removeGreen()
                getMoves(event, i, j)

            }
            else if (selected[0] != i || selected[1] != j) {
                if (event.currentTarget.classList.contains("green")) {
                    let xhttp = new XMLHttpRequest()
                    xhttp.onreadystatechange = function () {
                        if (this.readyState == 4 && this.status == 200) {
                            console.log("Moved")
                            console.log(this.response)

                            /*
                            ** Get All classes from old cell to the new cell
                            */
                            let classes = cells[selected[0] * 8 + selected[1]].querySelector("i").getAttribute("class")
                            cells[selected[0] * 8 + selected[1]].querySelector("i").removeAttribute("class")
                            cells[i * 8 + j].querySelector("i").setAttribute("class", classes)

                            // Remove Shadows from all cells
                            removeGreen()
                        }
                    }
                    xhttp.open("POST", "/make_move")
                    xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
                    xhttp.send("&x1=" + selected[0] + "&y1=" + selected[1] + "&x2=" + i + "&y2=" + j)
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
    if (event.currentTarget.querySelector('i').classList.length != 0) {
        let xhttp = new XMLHttpRequest()
        xhttp.onreadystatechange = function () {
            if (this.readyState == 4 && this.status == 200) {
                results = JSON.parse(this.response)
                console.log(results)
                if (results.length != 0) {
                    for (let k = 0, len = results.length; k < len; k++) {
                        x = results[k][0]
                        y = results[k][1]

                        // Add shadows to the posible moves cells
                        cells[(x * 8) + y].classList.add("green")
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
** Remove All shadows
*/
function removeGreen() {
    for (let k = 0; k < 64; k++) {
        cells[k].classList.remove("green")
    }
    selected = null
}

