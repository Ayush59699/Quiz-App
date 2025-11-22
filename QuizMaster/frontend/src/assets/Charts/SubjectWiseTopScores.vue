<template>
    <div class="chart-container">
        <h3>📊 Subject-wise Top Scores</h3>
        <Bar id="my-chart-id" :options="chartOptions" :data="chartData" />

    </div>
</template>

<script>
import { Bar } from 'vue-chartjs'
import { Chart as ChartJS, Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale } from 'chart.js'

ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale)

export default {
    name: "SubjectWiseTopScores",
    components: {
        Bar,
    },
    data() {
        return {

            chartData: {
                labels: [],
                datasets: [
                    {
                        label: "Subject Wise Top Scores",
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
                        title: { display: true, text: 'Scores' }
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
                const response = await fetch('http://127.0.0.1:8080/admin_summary2', {
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
                console.log('Subject wise TOP SCORES DATA:', data)



                const topScores = {}
                data.forEach(subject => {
                    const subjectName = subject.subject_name
                    const top_score = subject.top_score
                    if (!topScores[subjectName] || topScores[subjectName] < top_score) {
                        topScores[subjectName] = top_score
                    }
                })
                const allQuizNames = Object.keys(topScores)
                const allScores = Object.values(topScores)
                console.log("Subject Names:", allQuizNames)
                console.log("Top Scores:", allScores)

                this.chartData = {
                    labels: allQuizNames,
                    datasets: [{
                        label: "Subject Wise Top Scores",
                        data: allScores,
                        backgroundColor: "rgba(75, 192, 192, 0.2)",
                        borderColor: "rgba(75, 192, 192, 1)",
                        borderWidth: 1
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