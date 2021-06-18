const socket = io("/waiting")

document.querySelector("#submit").addEventListener("click", function (event) {
    event.preventDefault()
    let code = document.querySelector("#code").value

    socket.emit("code", { 'code': code })
    displayMsg()
})

socket.on("ready", function () {
    console.log("Ready?")

    socket.emit("ready", { 'ready': null })
    changeMsg("Connecting")
})

socket.on("start", function () {
    location.href = "/game"
})

function displayMsg() {
    document.querySelector(".fill").style.display = 'block'
}

function changeMsg(msg) {
    document.querySelector(".msg").innerHTML = msg
}