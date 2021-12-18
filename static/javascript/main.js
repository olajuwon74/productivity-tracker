const status_color_map = { 'N': '#FFC234', 'G': '#1B7930', 'P': '#FC2D2D' };
function rgbToHex(color) {
  const rgba = color.replace(/^rgba?\(|\s+|\)$/g, '').split(',');
  const hex = `#${((1 << 24) + (parseInt(rgba[0]) << 16) + (parseInt(rgba[1]) << 8) + parseInt(rgba[2])).toString(16).slice(1)}`;

  return hex.toUpperCase();
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
  window.open(window.location.origin + window.location.pathname + `?startDate=${startDate}&endDate=${endDate}`, "_self");

}

function getLatestProductivity() {
  $.get('/current_record', function (data, status) {
    if (status === 'success') {
      if (data) {
        status_color = status_color_map[data.cat];
        document.getElementById("productivity_status").style.backgroundColor = status_color;

        // update productivity_values in modal
        var popups = document.getElementsByClassName("productivity_value");
        for (var i = 0; i < popups.length; i++) {
          popups[i].innerHTML = data.norm_prod;
        }
      }
    }
  })
}

function showmodal() {
  // if current address is not '/logs', don't show modal
  if (window.location.pathname !== '/logs' || window.location.search) {
    return;
  }
  const modalsId = { 'P': ['bad1', 'bad2', 'bad3'], 'G': ['good1', 'good2', 'good3'], 'N': ['neutral1', 'neutral2', 'neutral3'] }
  const color_status_map = Object.fromEntries(Object.entries(status_color_map).map(a => a.reverse()))
  const current_color = rgbToHex(document.getElementById("productivity_status").style.backgroundColor);

  if (!current_color) {
    return;
  }
  const current_status = color_status_map[current_color];
  const current_modals = modalsId[current_status];

  console.log(current_modals);
  const modal = current_modals[Math.floor(Math.random() * current_modals.length)];
  const modal_element_title = document.getElementById(modal + 'title');
  modal_element_title.style.backgroundColor = current_color;

  if (modal === 'neutral2') {
    constructDayChart();
  }
  $(`#${modal}`).modal('show');


}

function showNotification() {
  // request permission on page load
  if (!Notification) {
    alert('Desktop notifications not available in your browser. Try Chromium.');
    return;
  }

  if (Notification.permission !== 'granted')
    Notification.requestPermission();
  ;


  function notifyMe() {
    if (window.location.pathname !== '/logs' || window.location.search) {
      return;
    }
    if (Notification.permission !== 'granted')
      Notification.requestPermission();
    else {
      const current_color = rgbToHex(document.getElementById("productivity_status").style.backgroundColor);
      const color_status_map = Object.fromEntries(Object.entries(status_color_map).map(a => a.reverse()))
      const current_status = color_status_map[current_color]
      const notification_messages = {
        'P': 'Productivity is going down!',
        'G': 'You are doing great!',
        'N': 'You\'re maintaining productivity!',
      }
      var notification = new Notification("PBC", {
        icon: "data:image/png;base64,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",
        body: notification_messages[current_status]
      });
      notification.onclick = function () {
        window.open('/productivity');
      };
    }
  }
  notifyMe()
}

function constructDayChart() {
  $.get("/day_productivity", function (data, status) {


    const chartColors = { red: '#FC2D2D', orange: '#FFC234', green: '#1B7930', };

    var canvas = document.getElementById("day_chart");
    var ctx = canvas.getContext("2d");

    // var gradientStroke = ctx.createLinearGradient(0, 1200, 0, 0);
    // gradientStroke.addColorStop(0, "#80b6f4");
    // gradientStroke.addColorStop(1, "#94d973");

    const day_productivity_data = data || [{}];
    let width, height, gradient;
    function getGradient(ctx, chartArea) {
      const chartWidth = chartArea.right - chartArea.left;
      const chartHeight = chartArea.bottom - chartArea.top;
      if (!gradient || width !== chartWidth || height !== chartHeight) {
        // Create the gradient because this is either the first render
        // or the size of the chart has changed
        width = chartWidth;
        height = chartHeight;
        gradient = ctx.createLinearGradient(0, chartArea.bottom, 0, chartArea.top);
        gradient.addColorStop(0, chartColors.red);
        gradient.addColorStop(0.3, chartColors.orange);
        gradient.addColorStop(1, chartColors.green);
      }

      return gradient;
    }

    const down = (ctx, value) => day_productivity_data[ctx.p1DataIndex]?.cat === "P" ? value : undefined
    const up = (ctx, value) => day_productivity_data[ctx.p1DataIndex]?.cat === "G" ? value : undefined
    const day_productivity_chart = new Chart(ctx, {
      type: 'line',
      data: {
        labels: day_productivity_data.map(d => d.total_seconds),
        datasets: [{
          raw_data: day_productivity_data,
          data: day_productivity_data.map(d => d.norm_prod),
          borderColor: function (context) {
            const chart = context.chart;
            const { ctx, chartArea } = chart;

            if (!chartArea) {
              // This case happens on initial chart load
              return;
            }
            return getGradient(ctx, chartArea);
          },
          fill: false,
          // segment: {
          //   borderColor: ctx => up(ctx, chartColors.green) || down(ctx, chartColors.red) || chartColors.orange,
          // },
          spanGaps: true,
        },
        {
          data: day_productivity_data.map(r => -0.64),
          pointRadius: 0,
          pointHitRadius: 0,
          borderColor: chartColors.orange,
          borderDash: [5, 10]
        },
        {
          data: day_productivity_data.map(r => 0.17),
          pointRadius: 0,
          pointHitRadius: 0,
          borderColor: chartColors.orange,
          borderDash: [5, 10]
        },
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        elements: {
          point: {
            pointStyle: 'circle',
          }
        },
        plugins: {
          title: {
            display: true,
            text: 'Productivity'
          },
          legend: {
            display: false,
          },
          tooltip: {
            callbacks: {
              usePointStyle: true,
              title: function (context,) {
                const raw_data = context[0].dataset.raw_data;

                if (!raw_data) {
                  return;
                }
                const { start_timestamp } = raw_data[context[0].dataIndex]
                return start_timestamp;
              },
              label: function (context) {
                const raw_data = context.dataset.raw_data
                if (!raw_data) {
                  return;
                }
                const { norm_prod, sequence } = raw_data[context.dataIndex]
                return [norm_prod, sequence];
              },
            }
          },
        },
        interaction: {
          intersect: false,
        },
        scales: {
          x: {
            display: true,
            title: {
              display: true,
              text: 'timeline'
            }
          },
          y: {
            max: 1,
            min: -1,
            display: true,
            title: {
              display: true,
              text: 'productivity'
            },
          }
        }
      },
    },
    )

  });
};


$(document).ready(function () {
  getLatestProductivity();
  //  add click event listener to filter_by_date id
  document.getElementById("filter_by_date")?.addEventListener("click", filterByDate);
  setTimeout(() => {
    showmodal();
  }, 1000);
  setTimeout(() => {
    showNotification();
  }, 1000);
});
