var products = ["Potatoes", "Wheat", "Broccoli", "Carrots", "Onions", "Peppers", "Spinach", "Watermelons"];
var averageRatings = [4.2, 3.8, 4.5, 3.2, 4.0, 3.9, 4.1, 3.7];

var ctx = document.getElementById('ratingsChart').getContext('2d');

var ratingsChart = new Chart(ctx, {
    type: 'pie',
    data: {
        labels: products,
        datasets: [{
            label: 'Average Ratings',
            data: averageRatings,
            backgroundColor: [
                'rgba(255, 99, 132, 1)',
                'rgba(54, 162, 235, 1)',
                'rgba(255, 206, 86, 1)',
                'rgba(75, 192, 192, 1)',
                'rgba(153, 102, 255, 1)',
                'rgba(255, 159, 64, 1)',
                'rgba(255, 183, 159, 1)',
                'rgba(94, 245, 112, 1)',
            ],
        }],
    },
});