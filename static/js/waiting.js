const socket = io('/waiting')

document.querySelector("#submit").addEventListener("click", function (event) {
    event.preventDefault()
    let code = document.querySelector("#code").value
    socket.emit("waiting_room", { 'code': code })
    displayMsg()
})

socket.on("is_ready", function (data) {
    console.log(data)
    changeMsg("Connecting")
    socket.emit("start", { "Starting": "" })
})

socket.on("start", function (data) {
    console.log(data)
    changeMsg("Starting")
    setTimeout(function () {
        location.href = "/game"
    }, 2000)
})

socket.on('Oppo_Disconnect', function (msg) {
    document.querySelector("#disconnected p").innerHTML = msg
    $("#disconnected").modal("show")
    setTimeout(function () {
        location.href = "/"
    }, 2000)
})

function displayMsg() {
    document.querySelector(".fill").style.display = 'block'
}

function changeMsg(msg) {
    document.querySelector(".msg").innerHTML = msg
}
