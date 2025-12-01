document.addEventListener('DOMContentLoaded', function() {
    const canvases = document.querySelectorAll('.chart-canvas');
    if (canvases.length) {
        const ensure = (cb) => {
            if (typeof Chart === 'undefined') {
                const s = document.createElement('script');
                s.src = 'https://cdn.jsdelivr.net/npm/chart.js';
                s.onload = cb;
                document.body.appendChild(s);
            } else cb();
        };

        ensure(() => {
            canvases.forEach(canvas => {
                try {
                    const labels = JSON.parse(canvas.dataset.labels || '[]');
                    const values = JSON.parse(canvas.dataset.values || '[]');
                    const dtype = canvas.dataset.type || 'bar';
                    createChart(canvas, labels, values, dtype);
                } catch (e) {
                    console.error('Error parsing chart data', e);
                }
            });
        });
    }

    window.filterConsultas = function(prioridad) {
        const rows = document.querySelectorAll('.consulta-row');
        rows.forEach(row => {
            if (prioridad === 'all' || row.dataset.prioridad === prioridad) {
                row.style.display = '';
            } else {
                row.style.display = 'none';
            }
        });
        document.querySelectorAll('.card-header button').forEach(btn => btn.classList.remove('active'));
    };
});

function createChart(canvas, labels, values, dtype='bar') {
    const cfg = {
        type: dtype,
        data: {
            labels: labels,
            datasets: [{
                label: canvas.dataset.label || '',
                data: values,
                backgroundColor: (dtype === 'doughnut') ? ['#198754', '#ffc107'] : 'rgba(13,110,253,0.8)'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
        }
    };

    if (dtype === 'bar') {
        cfg.options.scales = { y: { beginAtZero: true } };
    }

    new Chart(canvas, cfg);
}
