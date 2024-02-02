let stockchart; // Declare chart variable outside to be accessible in updateChart function
let stockName = document.getElementById('stockName').value;
document.getElementById('1mo').addEventListener('click', () => fetchData(stockName, '1mo'));
document.getElementById('3mo').addEventListener('click', () => fetchData(stockName, '3mo'));
document.getElementById('6mo').addEventListener('click', () => fetchData(stockName, '6mo'));
document.getElementById('1y').addEventListener('click', () => fetchData(stockName, '1y'));

document.getElementById('homebutton').addEventListener('click', () => window.location.href='/');

function fetchData(stockName, period) {
   
    fetch(`/specificdata/${stockName}?period=${period}`)
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        updateChart(data,stockName);
    })
    .catch(error => {
        console.error('There has been a problem with your fetch operation:', error);
        // Optionally, update the UI to inform the user
    });
}

function updateChart(data,stockName) {
    const dates = data.map(item => {
        const date = new Date(item.Date);
        return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
    });
    const values = data.map(item => item.Close);    
    
    // Calculate dynamic min and max for the dataset
    const minValue = Math.min(...values);
    const maxValue = Math.max(...values);
    
    // Optionally, add a buffer or margin to min and max values for better chart visualization
    const buffer = (maxValue - minValue) * 0.1; // Adding 10% buffer on each side
    const dynamicMin = minValue - buffer;
    const dynamicMax = maxValue + buffer;

    const ctx = document.getElementById('stockChart').getContext('2d');
    if (stockchart) {
        stockchart.destroy(); // Destroy the old chart instance if it exists
    }
    
    stockchart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: dates,
            datasets: [{
                label: stockName,
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
                    min: dynamicMin,
                    max: dynamicMax,
                }
            }
        }
    });
}

// Rest of your code remains the same

// Initial chart load for default period
fetchData(stockName,'10mo');
