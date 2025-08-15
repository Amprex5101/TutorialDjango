const getChartsData = async () => {
    try {
        const response = await fetch('http://127.0.0.2:3000/polls/get_chart/');
        return await response.json();
    }
    catch (ex) {
        console.error("Error al obtener datos:", ex);
        return {};
    }
};

const initCharts = async () => {
    // Obtener los datos de todas las gráficas
    const chartsData = await getChartsData();
    
    // Para cada pregunta se inicia una grafica.
    for (const questionId in chartsData) {
        const chartElement = document.getElementById(`chart-${questionId}`);
        
        if (chartElement) {
            chartElement.style.display = 'block';
            
            setTimeout(() => {
                const chart = echarts.init(chartElement);
                chart.setOption(chartsData[questionId]);
                window.addEventListener('resize', () => {
                    chart.resize();
                });
            }, 100);
        }
    }
};

// Ejecutar cuando el documento esté completamente cargado
document.addEventListener("DOMContentLoaded", async() => {
    await initCharts();
});
