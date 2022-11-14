// Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontFamily = 'Nunito', '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#858796';

// Pie Chart Example
var ctx = document.getElementById("myPieChart");
var myPieChart = new Chart(ctx, {
  type: 'doughnut',
  data: {
    labels: ["A", "B", "C", "D", "E", "F", "G"],
    datasets: [{
      data: [2, 3, 4, 5, 6, 7],
      backgroundColor: ['#4e73df', '#1cc88a', '#36b9cc', '#1cb0c8', '#1cc834', '#c81c5a','#36b9cc'],
      hoverBackgroundColor: ['#2e59d9', '#17a673', '#2c9faf','#1cb0c8', '#1cc834', '#c81c5a','#36b9cc'],
      hoverBorderColor: "rgba(234, 236, 244, 1)",
    }],
  },
  options: {
    maintainAspectRatio: false,
    tooltips: {
      backgroundColor: "rgb(255,255,255)",
      bodyFontColor: "#858796",
      borderColor: '#dddfeb',
      borderWidth: 1,
      xPadding: 15,
      yPadding: 15,
      displayColors: false,
      caretPadding: 10,
    },
    legend: {
      display: false
    },
    cutoutPercentage: 80,
  },
});
