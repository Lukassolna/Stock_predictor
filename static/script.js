fetch('/data')
.then(response => response.json())
.then(data => {
    const dates = data.map(item => {
        const date = new Date(item.Date);
        return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
    });
    const values = data.map(item => item.Close);

    const ctx = document.getElementById('stockChart').getContext('2d');

    const chart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: dates,
            datasets: [{
                label: 'OMX 30 Index',
                backgroundColor: 'rgba(0, 128, 0, 0.2)', // Light green background
                borderColor: 'rgba(0, 128, 0, 1)', // Green line
                data: values,
                fill: false, // If you want no fill under the line
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: false, // Set to false to not start at zero
                    min: 2000, // Minimum value for y-axis
                    max: 3000, // Maximum value for y-axis
                    // You can also set the stepSize if you want specific increments
                }
            }
        }
    });
});
