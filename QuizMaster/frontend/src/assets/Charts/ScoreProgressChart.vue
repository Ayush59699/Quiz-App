<template>
    <div>

        <div class="chart-container">
            <h2>Score Progression Over Time</h2>
            <Line v-if="chartData.labels.length" :data="chartData" :options="chartOptions" />
            <p v-else>Loading chart...</p>
        </div>



    </div>
</template>

<script>
import { Line } from 'vue-chartjs'

import { Chart as ChartJS, Title, Tooltip, Legend, LineElement, PointElement, CategoryScale, LinearScale } from 'chart.js'

ChartJS.register(Title, Tooltip, Legend, CategoryScale, LinearScale, LineElement, PointElement)

export default {
    name: "ScoreProgressChart",
    components: { Line },
    data() {
        return {
            chartData: {
                labels: [],
                datasets: []
            },
            chartOptions: {
                responsive: true,
                scales: {
                    y: {
                        beginAtZero: true,
                        title: {
                            display: true,
                            text: 'Score'
                        }
                    },
                    x: {
                        title: {
                            display: true,
                            text: 'Time of Attempt'
                        }
                    }
                }
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
                console.log("Fetched Data:", data);

                const quizAttempts = {}; // Stores attempts per quiz

                data.forEach(quiz => {
                    const quizName = quiz.quiz_name;
                    if (!quizAttempts[quizName]) {
                        quizAttempts[quizName] = [];
                    }
                    quizAttempts[quizName].push(quiz.total_score);
                });

                const allQuizNames = Object.keys(quizAttempts);

                this.chartData = {
                    labels: Array.from({ length: Math.max(...Object.values(quizAttempts).map(q => q.length)) }, (_, i) => i + 1),
                    datasets: allQuizNames.map((quizName, index) => ({
                        label: quizName,
                        data: quizAttempts[quizName],
                        borderColor: this.getColor(index),
                        backgroundColor: this.getColor(index, 0.2),
                        borderWidth: 2,
                        tension: 0.3,
                        fill: false
                    }))
                };

            } catch (error) {
                this.error = "Failed to load data";
                console.error(error);
            } finally {
                this.loading = false;
            }
        },

        getColor(index, opacity = 1) {
            const hue = (index * 137) % 360; // Ensures different colors for each quiz
            return `hsla(${hue}, 70%, 50%, ${opacity})`;
        }

    }
}
</script>
