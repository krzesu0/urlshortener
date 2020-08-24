

function parseForm() {
    const url = document.getElementById("formurl").value
    const slug = document.getElementById("formtext").value
    return {url: url, text: slug}
}

function send() {
    sendJSON()
}

function printMessage(data, div, p) {
    p.innerHTML = ""
    if(data["error"]) {
        p.innerText = "Something went wrong! " + data["status"]
    } else {
        readyURL = document.URL + data["text"]
        p.innerHTML = "All good! Your url: <a href='" + readyURL + "'>" + readyURL + "</a>"
    }
    
    div.style = "display: block;"
}

async function sendJSON(json) {
    const div = document.getElementById("output")
    const p = div.children[0]
    div.style = "display: none;"
    const jsonData = JSON.stringify(parseForm())
    await fetch("/", {
        method: "POST",
        headers: {
            "Accept": "application/json",
            "Content-Type": "application/json"
        },
        body: jsonData
    })
    .then(function(res) {return res.json()})
    .then(function(data) {
        console.log(data)
        printMessage(data, div, p)
    })
    .catch(function(e){console.log(e)})

}