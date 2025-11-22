<template>
    <div class="chart-container">
        <h3>📊 Subject-wise Top Scores</h3>
        <Pie id="my-chart-id" :options="chartOptions" :data="chartData" />

    </div>
</template>

<script>
import { Pie } from 'vue-chartjs'
import { Chart as ChartJS, Title, Tooltip, Legend, BarElement, ArcElement, CategoryScale, LinearScale } from 'chart.js'

ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, ArcElement, LinearScale)

export default {
    name: "SubjectWiseUserAttempts",
    components: {
        Pie,
    },
    data() {
        return {

            chartData: {
                labels: [],
                datasets: [
                    {
                        label: "Subject WiseUser Attempts",
                        data: [],
                        backgroundColor: "rgba(54, 162, 235, 0.5)",
                        borderColor: '#fff',
                        borderWidth: 2
                    }
                ]
            },
            chartOptions: {
                responsive: true,
                plugins: {
                    legend: { position: "bottom" },
                    tooltip: { enabled: true }
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
                const response = await fetch('http://127.0.0.1:8080/admin_summary3', {
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
                console.log('Subject wise USER ATTEMPTS DATA:', data)

                const totalattempts = {}
                data.forEach(subject => {
                    const subjectName = subject.subject_name
                    const attempt_count = subject.attempt_count
                    totalattempts[subjectName] = attempt_count
                })

                const allSubjectNames = Object.keys(totalattempts)
                const allAttempts = Object.values(totalattempts)

                const colors = allSubjectNames.map(() =>
                    `hsl(${Math.random() * 360}, 70%, 60%)`
                );

                console.log("Subject Names:", allSubjectNames)
                console.log("Total Attempts:", allAttempts)

                this.chartData = {
                    labels: allSubjectNames,
                    datasets: [{
                        label: "Subject Wise User attempts",
                        data: allAttempts,
                        backgroundColor: colors,
                        borderColor: "#fff",
                        borderWidth: 4
                    }]
                };
            }
            catch (error) {
                console.log('Error', error)
            }

        }
    }





}
</script>
<style scoped>
.chart-container {
    width: 100%;
    max-width: 600px;
    margin: auto;
}
</style>