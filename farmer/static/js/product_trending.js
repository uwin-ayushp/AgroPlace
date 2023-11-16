var products = ["Potatoes", "Wheat", "Broccoli", "Carrots", "Onions", "Peppers", "Spinach", "Watermelons"];
var counts = [63, 45, 39, 35, 33, 30, 27, 27];

var ctx = document.getElementById('trendingChart').getContext('2d');

var trendingChart = new Chart(ctx, {
    type: 'bar',
    data: {
        labels: products,
        datasets: [{
            label: 'Count (lbs)',
            data: counts,
            backgroundColor: 'rgba(255, 99, 132, 1)',
            borderColor: 'rgba(255, 99, 132, 1)',
            borderWidth: 1,
        }],
    },
    options: {
        scales: {
            y: {
                beginAtZero: true,
                title: {
                    display: true,
                    text: 'Count (lbs)',
                },
            },
        },
        plugins: {
            title: {
                display: true,
                text: 'Trending Products - Last Week',
            },
        },
    },
});