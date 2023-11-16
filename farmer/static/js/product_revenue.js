var products = ["Potatoes", "Onions", "Carrots", "Broccoli", "Watermelons", "Wheat", "Spinach", "Peppers"];
var revenueData = [10000, 6000, 5900, 5850, 5699, 5550, 5478, 5398, 5350];

var ctx = document.getElementById("revenueChart").getContext("2d");

var revenueChart = new Chart(ctx, {
    type: "bar",
    data: {
        labels: products,
        datasets: [{
            label: "Revenue (CAD)",
            data: revenueData,
            backgroundColor: "rgba(75, 192, 192, 1)",
            borderColor: "rgba(75, 192, 192, 1)",
            borderWidth: 1,
        }]
    },
    options: {
        scales: {
            y: {
                beginAtZero: true,
                title: {
                    display: true,
                    text: 'Revenue (CAD)',
                },
            }
        },
        plugins: {
            title: {
                display: true,
                text: 'Products Revenue List - Last Month',
            },
        },
    }
});


// var products = ["Potatoes", "Onions", "Carrots", "Broccoli", "Watermelons", "Wheat", "Spinach", "Peppers"];
// var revenueData = [10000, 6000, 5900, 5850, 5699, 5550, 5478, 5398, 5350];
//
// var ctx = document.getElementById("revenueChart").getContext("2d");
//
// var revenueChart = new Chart(ctx, {
//     type: "pie", // Change type to "pie" for a pie chart
//     data: {
//         labels: products,
//         datasets: [{
//             label: "Revenue",
//             data: revenueData,
//             // Remove backgroundColor and borderColor properties for pie chart
//         }]
//     },
//     options: {
//         plugins: {
//             title: {
//                 display: true,
//                 text: 'Products Revenue Distribution - Last Month',
//             },
//         },
//     }
// });


