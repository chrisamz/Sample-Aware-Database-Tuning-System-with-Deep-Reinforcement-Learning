// scripts.js

document.addEventListener("DOMContentLoaded", function() {
    // Function to update performance metrics
    function updatePerformanceMetrics() {
        fetch('/api/performance_metrics')
            .then(response => response.json())
            .then(data => {
                document.getElementById('cpu-usage').innerText = data.cpu_usage + '%';
                document.getElementById('memory-usage').innerText = data.memory_usage + '%';
                document.getElementById('disk-usage').innerText = data.disk_usage + '%';
            })
            .catch(error => console.error('Error fetching performance metrics:', error));
    }

    // Function to update optimization status
    function updateOptimizationStatus() {
        fetch('/api/optimization_status')
            .then(response => response.json())
            .then(data => {
                document.getElementById('optimization-status').innerText = data.status;
            })
            .catch(error => console.error('Error fetching optimization status:', error));
    }

    // Event listener for parameter adjustment
    document.getElementById('adjust-params-form').addEventListener('submit', function(event) {
        event.preventDefault();

        const formData = new FormData(this);
        const params = {};
        formData.forEach((value, key) => {
            params[key] = value;
        });

        fetch('/api/adjust_params', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(params),
        })
        .then(response => response.json())
        .then(data => {
            alert('Parameters adjusted successfully!');
            updatePerformanceMetrics();
            updateOptimizationStatus();
        })
        .catch(error => console.error('Error adjusting parameters:', error));
    });

    // Initial load
    updatePerformanceMetrics();
    updateOptimizationStatus();

    // Periodic updates
    setInterval(updatePerformanceMetrics, 5000);
    setInterval(updateOptimizationStatus, 5000);
});
