document.getElementById("searchBar").size = "50";
var toggleHidden = function(id) {
  console.log("toggling hidden");
  const toggle = document.getElementById(id);
  toggle.classList.toggle('hidden');
}
