function open_modal(index, keepTrack = false) {
  var modal = document.getElementById("myModal" + index);
  modal.style.display = "block";
}

// When the user clicks on <span> (x), close the modal
function span_click(index){
  document.getElementById("myModal" + index).style.display = "none";
}

// For redirecting to the completion page
function Completion_button(href) {
  window.open(href, "_blank");
}