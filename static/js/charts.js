// charts.js
function getPriorityColor(priority) {
    switch(priority?.toUpperCase()) {
        case 'CRITICAL': return '#dc2626'; // red-600
        case 'HIGH': return '#f97316'; // orange-500
        case 'MEDIUM': return '#eab308'; // yellow-500
        case 'LOW': return '#22c55e'; // green-500
        default: return '#9ca3af'; // gray-400
    }
}

const defaultOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
        legend: { position: 'bottom' }
    }
};

function createDoughnutChart(canvasId, labels, data, colors) {
    const ctx = document.getElementById(canvasId);
    if (!ctx) return null;
    return new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: labels,
            datasets: [{
                data: data,
                backgroundColor: colors,
                borderWidth: 0
            }]
        },
        options: {
            ...defaultOptions,
            cutout: '70%'
        }
    });
}

function createLineChart(canvasId, labels, data, label) {
    const ctx = document.getElementById(canvasId);
    if (!ctx) return null;
    return new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: label,
                data: data,
                borderColor: '#3b82f6',
                backgroundColor: 'rgba(59, 130, 246, 0.1)',
                borderWidth: 2,
                fill: true,
                tension: 0.4
            }]
        },
        options: {
            ...defaultOptions,
            scales: {
                y: { beginAtZero: true }
            }
        }
    });
}

function createBarChart(canvasId, labels, data, colors) {
    const ctx = document.getElementById(canvasId);
    if (!ctx) return null;
    return new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Count',
                data: data,
                backgroundColor: colors || '#3b82f6',
                borderRadius: 4
            }]
        },
        options: {
            ...defaultOptions,
            indexAxis: 'y',
            plugins: { legend: { display: false } },
            scales: {
                x: { beginAtZero: true }
            }
        }
    });
}
