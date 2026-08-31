let comparisonChartInstance = null;

function renderRadarChart(chartData, nameA, nameB) {
    const ctx = document.getElementById('radarChart').getContext('2d');

    if (comparisonChartInstance) {
        comparisonChartInstance.destroy();
    }

    comparisonChartInstance = new Chart(ctx, {
        type: 'radar',
        data: {
            labels: chartData.labels,
            datasets: [
                {
                    label: nameA,
                    data: chartData.policy_a_scores,
                    backgroundColor: 'rgba(37, 99, 235, 0.2)',
                    borderColor: 'rgba(37, 99, 235, 1)',
                    pointBackgroundColor: 'rgba(37, 99, 235, 1)',
                    borderWidth: 2,
                },
                {
                    label: nameB,
                    data: chartData.policy_b_scores,
                    backgroundColor: 'rgba(239, 68, 68, 0.2)',
                    borderColor: 'rgba(239, 68, 68, 1)',
                    pointBackgroundColor: 'rgba(239, 68, 68, 1)',
                    borderWidth: 2,
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                r: {
                    angleLines: { color: 'rgba(0, 0, 0, 0.1)' },
                    grid: { color: 'rgba(0, 0, 0, 0.05)' },
                    pointLabels: {
                        font: { size: 14, family: "'Inter', sans-serif", weight: 'bold' },
                        color: '#374151'
                    },
                    ticks: { min: 0, max: 100, stepSize: 20, display: false }
                }
            },
            plugins: {
                legend: { position: 'bottom', labels: { font: { size: 14, weight: 'bold' } } }
            }
        }
    });
}