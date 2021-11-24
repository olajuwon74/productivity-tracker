// // When the user scrolls the page, execute myFunction
// window.onscroll = function() {myFunction()};

// // Get the navbar
// var navbar = document.getElementById("navbar");

// // Get the offset position of the navbar
// var sticky = navbar.offsetTop;

// // Add the sticky class to the navbar when you reach its scroll position. Remove "sticky" when you leave the scroll position
// function myFunction() {
//   if (window.pageYOffset >= sticky) {
//     navbar.classList.add("sticky")
//   } else {
//     navbar.classList.remove("sticky");
//   }
// }

var modal = null
 function pop() {
   if(modal === null) {
     document.getElementById("box").style.display = "block";
     modal = true
   } else {
     document.getElementById("box").style.display = "none";
     modal = null
   }
 }

function filterByDate(date) {
  var startDate = document.getElementById("trip_start").value;
  var endDate = document.getElementById("trip_end").value;

  if (startDate === "" && endDate === "") {
    alert("Please enter a start and end date");
    return;
  }
  else if (startDate > endDate) {
    alert("Start date must be before end date");
    return;
  }
  window.open(window.location.origin+window.location.pathname+`?startDate=${startDate}&endDate=${endDate}`,"_self");
  
}

function getLatestProductivity(){
  productivity = $.get('/current_record', function(data, status){
    if (status === 'success'){
      if (data){
        status_color_map = {'N': 'orange', 'G': 'green', 'P': 'red'}
        status_color = status_color_map[data.cat];
        document.getElementById("productivity_status").style.backgroundColor = status_color;
      }
    }
  })
}

$(document).ready(function(){
  getLatestProductivity();
  //  add click event listener to filter_by_date id
  document.getElementById("filter_by_date")?.addEventListener("click", filterByDate);
});