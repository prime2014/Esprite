function getAJAX(category) {
    var request = new XMLHttpRequest();
    request.open("GET", `/products/?q=${category}/`);
    request.send(null);
    if (request.status == 200) {
        alert(request.responseText);
    } else {
        alert("Error " + request.status + " " + request.statusText);
    }
}