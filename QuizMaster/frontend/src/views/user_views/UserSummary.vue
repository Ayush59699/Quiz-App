<template>
    <div class="user-summary">
        <UserNavbar />

        <div class="container" style="max-width: 1350px;">
            <h2 class="page-title text-center">📊 User Summary</h2>

            <div class="row">
                <div class="col-md-6 mb-4">
                    <div class="chart-card">
                        <h3 class="chart-title">🏆 Highest Scores per Quiz</h3>
                        <MaxScoresChart />
                    </div>
                </div>

                <div class="col-md-6 mb-4">
                    <div class="chart-card">
                        <h3 class="chart-title">📈 Score Progression Over Time</h3>
                        <ScoreProgressChart />
                    </div>
                </div>

                <div class="col-md-6 mb-4">
                    <div class="chart-card">
                        <h3 class="chart-title">📈 Subject Wise Quiz Attempts</h3>
                        <SubjectWiseQuizChart />
                    </div>
                </div>

                <div class="col-md-6 mb-4">
                    <div class="chart-card">
                        <h3 class="chart-title">📈 Month Wise Quiz Attempts</h3>
                        <MonthWiseQuizChart />
                    </div>
                </div>
            </div>

            <div class="back-btn-container text-center mt-4">
                <router-link to="/user_dashboard" class="btn btn-primary">⬅ Back to Dashboard</router-link>
            </div>

        </div>
    </div>
</template>


<script>
import UserNavbar from '@/components/UserNavbar.vue'
import MaxScoresChart from '@/assets/Charts/MaxScoresChart.vue'
import ScoreProgressChart from '@/assets/Charts/ScoreProgressChart.vue'
import SubjectWiseQuizChart from '@/assets/Charts/SubjectWiseQuizChart.vue'
import MonthWiseQuizChart from '@/assets/Charts/MonthWiseQuizChart.vue'

import { Bar } from 'vue-chartjs'
import { Chart as ChartJS, Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale } from 'chart.js'

ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale)

export default {
    name: 'BarChart',
    components: {
        Bar,
        UserNavbar,
        MaxScoresChart,
        ScoreProgressChart,
        SubjectWiseQuizChart,
        MonthWiseQuizChart,


    },
    data() {
        return {

        }
    },
    mounted() {

    },

    methods: {


    }
}

</script>
<style scoped>
/* General Page Styling */
.user-summary {
    background-color: #f8f9fa;
    min-height: 100vh;
    padding-bottom: 30px;
}

/* Container Styling */
.container {
    max-width: 900px;
    margin: auto;
    padding: 20px;
    text-align: center;
}

/* Page Title */
.page-title {
    font-size: 28px;
    font-weight: bold;
    color: #343a40;
    margin-bottom: 20px;
}

/* Back Button */
.back-btn-container {
    margin-bottom: 20px;
}

.btn-primary {
    font-size: 16px;
    padding: 10px 20px;
    font-weight: bold;
    background-color: #007bff;
    border: none;
    border-radius: 5px;
    text-decoration: none;
    color: white;
    transition: 0.3s ease-in-out;
}

.btn-primary:hover {
    background-color: #0056b3;
}

/* Chart Cards */
.chart-card {
    background: white;
    padding: 20px;
    margin: 20px 0;
    border-radius: 10px;
    box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
    text-align: center;
}

.chart-title {
    font-size: 20px;
    font-weight: bold;
    margin-bottom: 15px;
    color: #495057;
}
</style>