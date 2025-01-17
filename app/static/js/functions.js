document.getElementById("searchBar").size = "50";
var toggleHidden = function(id) {
  console.log("toggling hidden");
  const toggle = document.getElementById(id);
  toggle.classList.toggle('hidden');
}
var addPokemon = function(pokemonName) {
  fetch('/add_pokemon', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
    },
    body: JSON.stringify({pokemon_name: pokemonName})
})
.then(response => {
    if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
    }
    return response.json(); // Only attempt to parse JSON if response is OK
})
.then(data => {
    console.log('Server response:', data);
    if (data.success) {
        alert('Pokemon added successfully.');
    } else {
        alert("Failed to add Pokemon: " + (data.error || 'Unknown error'));
    }
})
.catch(error => {
    console.error('Error during fetch:', error);
    alert('Your team is full.');
});
}