<template>
    <div v-if="loading">Loading...</div>
    <div v-else-if="error">{{ error }}</div>
    <div v-else>
        <Bar id="my-chart-id" :options="chartOptions" :data="chartData" />
    </div>
</template>

<script>
import { Bar } from 'vue-chartjs'
import { Chart as ChartJS, Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale } from 'chart.js'

ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale)

export default {
    name: "BarChartComponent",
    components: { Bar },
    data() {
        return {
            error: "",
            loading: false,
            chartData: {
                labels: [],
                datasets: []
            },
            chartOptions: {
                responsive: true
            }
        }
    },
    mounted() {
        this.getScores();
    },
    methods: {
        async getScores() {
            this.loading = true;
            try {
                const response = await fetch(`http://127.0.0.1:8080/user/scores`, {
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${localStorage.getItem('jwtToken')}`
                    }
                });

                if (!response.ok) {
                    throw new Error(`HTTP error! Status: ${response.status}`);
                }

                const data = await response.json();
                console.log("Fetched MaxScoresChart Data:", data);

                const quizScores = {}
                data.forEach(quiz => {
                    const quizName = quiz.quiz_name
                    const score = quiz.total_score
                    if (!quizScores[quizName] || quizScores[quizName] < score) {
                        quizScores[quizName] = score
                    }
                })
                const allQuizNames = Object.keys(quizScores)
                const allScores = Object.values(quizScores)
                console.log("Unique Quiz Names:", allQuizNames)
                console.log("Highest Scores Per Quiz:", allScores)

                this.chartData = {
                    labels: allQuizNames,
                    datasets: [{
                        label: "Highest Scores per Quiz",
                        data: allScores,
                        backgroundColor: "rgba(75, 192, 192, 0.2)",
                        borderColor: "rgba(75, 192, 192, 1)",
                        borderWidth: 1
                    }]
                };

            } catch (error) {
                this.error = "Failed to load data";
                console.error(error);
            } finally {
                this.loading = false;
            }
        }
    }
}
</script>
