var toggleHidden = function(id) {
  console.log("toggling hidden");
  const toggle = document.getElementById(id);
  toggle.classList.toggle('hidden');
}
var bar = function(n) {
  document.getElementById("searchBar").addEventListener("input");
}
