let stockchart; 
let stockName = document.getElementById('stockName').value;
document.getElementById('1mo').addEventListener('click', () => fetchData(stockName, '1mo'));
document.getElementById('3mo').addEventListener('click', () => fetchData(stockName, '3mo'));
document.getElementById('6mo').addEventListener('click', () => fetchData(stockName, '6mo'));
document.getElementById('1y').addEventListener('click', () => fetchData(stockName, '1y'));
document.getElementById('homebutton').addEventListener('click', () => window.location.href='/');
document.addEventListener('DOMContentLoaded', function() {
    const predictedChangeElement = document.getElementById('predictedChange');
    const predictedChangeValue = parseFloat(predictedChangeElement.textContent);
    
    // duplicated %
    let predictedChangeText = predictedChangeElement.textContent.replace('%', '');

    if (predictedChangeValue > 0) {
        predictedChangeElement.className = 'positive';
        predictedChangeElement.innerHTML = `&#9650; ${predictedChangeText}`; // Up arrow for positive change
    } else if (predictedChangeValue < 0) {
        predictedChangeElement.className = 'negative';
        predictedChangeElement.innerHTML = `&#9660; ${predictedChangeText}`; // Down arrow for negative change
    }
   
});

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
        
    });
}

function updateChart(data,stockName) {
    const dates = data.map(item => {
        const date = new Date(item.Date);
        return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
    });
    const values = data.map(item => item.Close);    
    
    
    const minValue = Math.min(...values);
    const maxValue = Math.max(...values);
    

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
//initial chart state
fetchData(stockName,'10mo');
