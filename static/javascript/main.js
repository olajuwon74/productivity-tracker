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

        // update productivity_values in modal
        var popups = document.getElementsByClassName("productivity_value");
        for (var i = 0; i < popups.length; i++) {
          popups[i].innerHTML = data.class_weight;
        }
      }
    }
  })
}

function showmodal(){
  // if current address is not '/logs', don't show modal
  if (window.location.pathname !== '/logs' || window.location.search){
    return;
  }
  const modalsId = {'P': ['bad1', 'bad2'], 'G': ['good1', 'good2'], 'N': ['neutral1', 'neutral2']}
  const color_status_map = {'orange': 'N', 'green': 'G', 'red': 'P'}
  const current_color = document.getElementById("productivity_status").style.backgroundColor;
  if (!current_color){
    return;
  }
  const current_status = color_status_map[current_color];
  const current_modals = modalsId[current_status];
  const modal = current_modals[Math.floor(Math.random() * current_modals.length)];
  const modal_element_title = document.getElementById(modal+'title');
  modal_element_title.style.backgroundColor = current_color;
  $(`#${modal}`).modal('show');
}

$(document).ready(function(){
  getLatestProductivity();
  //  add click event listener to filter_by_date id
  document.getElementById("filter_by_date")?.addEventListener("click", filterByDate);
  setTimeout(() => {
    showmodal();
  }, 1000);
});
