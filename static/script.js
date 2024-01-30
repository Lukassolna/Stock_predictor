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
    const coeff = [0.0005693932143501474, -0.04166693171601551, -0.0017189670006476443, -0.0029120077788588952];
    fetch(`/daily`)
    .then(response => response.json())
    .then(data => {
        console.log(data);
        const date = data.length > 0 ? new Date(data[0].date).toLocaleDateString() : 'No date available';
        const changes = data.map(stock => {
            const predictedValue = 
                coeff[0] * stock.RSI +
                coeff[1] * stock.Change +
                coeff[2] * stock['10_change'] +
                coeff[3] * stock.percentage_diff;
            return {
                name: stock.name, 
                RSI: stock.RSI,
                Change: (stock.Change * 100).toFixed(2) + '%',
                '10_change': stock['10_change'],
                percentage_diff: stock.percentage_diff,
                predictedValue: (predictedValue*100).toFixed(2)+ '%'
            };
        });

        // Sort the changes array
        changes.sort((a, b) => parseFloat(b.Change.replace('%', '')) - parseFloat(a.Change.replace('%', '')));

        // Get the container element
        const stockInfoContainer = document.getElementById('stockInfo');

        // Create HTML content
        const html = `
            <div class="header">
                <h1>Overview of OMX30 Stocks</h1>
                <h2>Date: ${date}</h2>
            </div>
            <table>
                <tr>
                    <th>Stock</th>
                    <th>Daily Change</th>
                    <th>Predicted Value</th>
                </tr>
                ${changes.map(stock => `
                    <tr>
                        <td>${stock.name}</td>
                        <td>${stock.Change}</td>
                        <td>${stock.predictedValue}</td>
                    </tr>
                `).join('')}
            </table>
        `;

        // Set the HTML content
        stockInfoContainer.innerHTML = html;
    });
}

// Initial chart load for default period
fetchData('10mo');
fetchDaily();