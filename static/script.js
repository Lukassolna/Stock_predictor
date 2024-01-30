let chart; // Declare chart variable outside to be accessible in updateChart function

document.getElementById('1mo').addEventListener('click', () => fetchData('1mo'));
document.getElementById('3mo').addEventListener('click', () => fetchData('3mo'));
document.getElementById('6mo').addEventListener('click', () => fetchData('6mo'));
document.getElementById('1y').addEventListener('click', () => fetchData('1y'));

function fetchData(period) {
    fetch(`/data?period=${period}`)
    .then(response => response.json())
    .then(data => {
        updateChart(data);
    });
}

function updateChart(data) {
    const dates = data.map(item => {
        const date = new Date(item.Date);
        return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
    });
    const values = data.map(item => item.Close);

    const ctx = document.getElementById('stockChart').getContext('2d');

    if (chart) {
        chart.destroy(); // Destroy the old chart instance if it exists
    }

    chart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: dates,
            datasets: [{
                label: 'OMX 30 Index',
                backgroundColor: 'rgba(0, 128, 0, 0.2)',
                borderColor: 'rgba(0, 128, 0, 1)',
                data: values,
                fill: false,
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: false,
                    min: 2000,
                    max: 3000,
                }
            }
        }
    });
}

// Initial chart load for default period
fetchData('10mo');
