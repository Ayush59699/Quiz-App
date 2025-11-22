<template>
    <div class="chart-container">
        <h3>📊 Month-wise Quiz Attempts</h3>
        <Bar id="my-chart-id" :options="chartOptions" :data="chartData" />

    </div>
</template>

<script>
import { Bar } from 'vue-chartjs'
import { Chart as ChartJS, Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale } from 'chart.js'

ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale)

export default {
    name: "SubjectWiseQuizChart",
    components: {
        Bar,
    },
    data() {
        return {

            chartData: {
                labels: [],
                datasets: [
                    {
                        label: "Number of Quiz Attempts",
                        data: [],
                        backgroundColor: "rgba(54, 162, 235, 0.5)",
                        borderColor: "rgba(54, 162, 235, 1)",
                        borderWidth: 1
                    }
                ]
            },
            chartOptions: {
                responsive: true,
                plugins: {
                    legend: { display: false },
                    tooltip: { enabled: true }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        title: { display: true, text: 'Count' }
                    },
                    x: {
                        title: { display: true, text: 'Subjects' }
                    }
                }
            }
        }
    },
    mounted() {
        this.getSubjectQuizData();
    },
    methods: {
        async getSubjectQuizData() {
            try {
                const response = await fetch('http://127.0.0.1:8080/get_month_wise_quiz_chart_data', {
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${localStorage.getItem('jwtToken')}`
                    }
                })
                if (!response.ok) {
                    throw new Error(`HTTP error! Status ${response.status}`)
                }
                const data = await response.json()
                console.log('Month wise quiz data:', data)



                this.chartData = Object.assign({}, this.chartData, {
                    labels: Object.keys(data),
                    datasets: [
                        {
                            ...this.chartData.datasets[0],
                            data: Object.values(data)
                        }
                    ]
                });



            }
            catch (error) {
                console.log('Error', error)
            }

        }
    }





}
</script>