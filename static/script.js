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
function fetchDaily() {
    fetch(`/daily`)
    .then(response => response.json())
    .then(data => {
        const date = data.length > 0 ? new Date(data[0].date).toLocaleDateString() : 'No date available';
        const changes = data.map(stock => ({ 
            name: stock.name, 
            Change: (stock.Change * 100).toFixed(2) + '%' // Format as percentage with 2 decimal places
        }));

        // Sort the changes array in descending order based on the 'Change' property
        changes.sort((a, b) => parseFloat(b.Change) - parseFloat(a.Change));

        // Get the container element in your HTML
        const stockInfoContainer = document.getElementById('stockInfo');

        // Create an HTML string to display the information
        const html = `
            <div class="header">
                <h1>Overview of OMX30 Stocks</h1>
                <h2>Date: ${date}</h2>
            </div>
            <table>
                <tr>
                    <th>Stock</th>
                    <th>Daily Change</th>
                </tr>
                ${changes.map(stock => `
                    <tr>
                        <td>${stock.name}</td>
                        <td>${stock.Change}</td>
                    </tr>
                `).join('')}
            </table>
        `;

        // Set the HTML content of the container element
        stockInfoContainer.innerHTML = html;
    });
}

// Initial chart load for default period
fetchData('10mo');
fetchDaily();