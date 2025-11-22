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
    name: "PopularQuizzesChart",
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
                const response = await fetch(`http://127.0.0.1:8080/admin_summary`, {
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
                console.log("Fetched PopularQuizzesChart Data:", data);


                const attemptCount = {}
                data.forEach(quiz => {
                    const quizName = quiz.quiz_name
                    const attempt_count = quiz.attempt_count
                    if (!attemptCount[quizName] || quizattemptCountcores[quizName] < attempt_count) {
                        attemptCount[quizName] = attempt_count
                    }
                })
                const allQuizNames = Object.keys(attemptCount)
                const allScores = Object.values(attemptCount)
                console.log("Quiz Names:", allQuizNames)
                console.log("Attempt Count:", allScores)

                this.chartData = {
                    labels: allQuizNames,
                    datasets: [{
                        label: "Popular attempted quizzes",
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
