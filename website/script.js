function search() {
    var input = document.getElementById('searchInput').value;
    document.getElementById('searchResults').innerHTML = "You searched for: " + input;
}