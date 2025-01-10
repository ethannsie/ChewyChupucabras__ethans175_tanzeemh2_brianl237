var toggleHiddden = function(elementid) {
  console.log("toggling hidden");
  const toggle = document.getElementById(elementid);
  toggle.classList.toggle('hidden');
}
var bar = function(n) {
  document.getElementById("searchBar").addEventListener("input");
}