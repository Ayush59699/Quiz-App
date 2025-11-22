<template>
    <div class="dashboard-container">
        <AdminNavbar />

        <div class="dashboard-content">
            <!-- Animated decorative elements -->
            <div class="floating-shape shape1"></div>
            <div class="floating-shape shape2"></div>
            <div class="floating-shape shape3"></div>

            <!-- Main content area -->
            <div class="glass-container">
                <h2 class="dashboard-title">
                    <span class="title-icon">📊</span>
                    <span class="title-text">User Summary</span>
                    <div class="title-underline"></div>
                </h2>

                <div class="charts-grid">
                    <!-- Popular Quizzes Chart -->
                    <div class="chart-module featured-chart">
                        <div class="chart-header">

                            <h3 class="chart-title">
                                <span class="chart-icon">🏆</span>
                                Highest Scores per Quiz
                            </h3>
                        </div>
                        <div class="chart-content">
                            <PopularQuizzesChart />
                        </div>
                    </div>

                    <!-- Subject Top Scores -->
                    <div class="chart-module">
                        <div class="chart-header">

                            <h3 class="chart-title"><span class="chart-icon">🏆</span>
                                Subject-wise Top Scores
                            </h3>
                        </div>
                        <div class="chart-content">
                            <SubjectWiseTopScores />
                        </div>
                    </div>

                    <!-- User Attempts -->
                    <div class="chart-module wide-module">
                        <div class="chart-header">
                            <h3 class="chart-title"><span class="chart-icon">🏆</span>
                                Subject-wise User Attempts</h3>
                        </div>
                        <div class="chart-content">
                            <SubjectWiseUserAttempts />
                        </div>
                    </div>
                </div>

                <div class="navigation-action">
                    <router-link to="/admin_dashboard" class="back-button">
                        <span class="back-icon">⬅</span>
                        <span class="back-text">Back to Dashboard</span>
                    </router-link>
                </div>
            </div>
        </div>
    </div>
</template>


<script>
import PopularQuizzesChart from '@/assets/Charts/PopularQuizzesChart.vue';
import AdminNavbar from '@/components/AdminNavbar.vue';
import SubjectWiseTopScores from '@/assets/Charts/SubjectWiseTopScores.vue';
import SubjectWiseUserAttempts from '@/assets/Charts/SubjectWiseUserAttempts.vue';

export default {
    components: {
        AdminNavbar,
        PopularQuizzesChart,
        SubjectWiseTopScores,
        SubjectWiseUserAttempts,

    },

    name: 'AdminSummary',
    data() {
        return {
            admin_name: '',


        };
    },
    async mounted() {
        const admin_name = localStorage.getItem('admin_name') || 'admin'
        this.admin_name = admin_name


    },
    methods: {


        async logout() {
            try {
                const response = await fetch("http://127.0.0.1:8080/admin_logout", {
                    method: 'POST',
                    headers: {
                        'Authorization': `Bearer ${localStorage.getItem('jwtToken')}`
                    }
                });
                if (response.ok) {
                    localStorage.removeItem('jwtToken');
                    localStorage.removeItem('admin_name');
                    this.$router.push('/');
                }
            } catch (error) {
                console.error("Logout Failes", error);
            }
        }


    }
};
</script>

<style>
/* Base styling */
.dashboard-container {
    min-height: 100vh;
    /* background: linear-gradient(135deg, #1a0b2e 0%, #1f1750 100%);
    */
    position: relative;
    overflow: hidden;
    color: #000000;
}

.dashboard-content {
    padding: 2rem;
    position: relative;
    z-index: 1;
}

/* Floating animated shapes */
.floating-shape {
    position: absolute;
    border-radius: 50%;
    filter: blur(60px);
    opacity: 0.4;
    z-index: 0;
}

.shape1 {
    width: 300px;
    height: 300px;
    /* background: linear-gradient(to right, #ff5e62, #ff9966);*/

    top: -100px;
    right: 10%;
    animation: float 15s ease-in-out infinite alternate;
}

.shape2 {
    width: 400px;
    height: 400px;
    /* background: linear-gradient(to right, #4facfe, #00f2fe);*/
    bottom: -150px;
    left: -100px;
    animation: float 20s ease-in-out infinite alternate-reverse;
}

.shape3 {
    width: 200px;
    height: 200px;
    /* background: linear-gradient(to right, #f093fb, #f5576c);*/
    top: 30%;
    left: 20%;
    animation: float 18s ease-in-out infinite alternate;
}

@keyframes float {
    0% {
        transform: translate(0, 0) rotate(0deg);
    }

    50% {
        transform: translate(30px, 20px) rotate(5deg);
    }

    100% {
        transform: translate(-20px, 40px) rotate(-5deg);
    }
}

/* Glass morphism container */
.glass-container {
    background: rgba(255, 255, 255, 0.05);
    backdrop-filter: blur(10px);
    border-radius: 24px;
    border: 1px solid rgba(204, 190, 190, 0.1);
    box-shadow: 0 8px 32px rgba(221, 217, 217, 0.2);
    padding: 2.5rem;
    margin: 1rem auto;
    max-width: 1400px;
}

/* Dashboard title */
.dashboard-title {
    display: flex;
    align-items: center;
    margin-bottom: 2.5rem;
    position: relative;
}

.title-icon {
    font-size: 2rem;
    margin-right: 1rem;
    filter: drop-shadow(0 0 10px rgba(220, 98, 98, 0.3));
}

.title-text {
    font-size: 2.5rem;
    font-weight: 800;
    background: linear-gradient(to right, #452778, #1c8dc2);
    background-clip: text;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    letter-spacing: 1px;
}

.title-underline {
    position: absolute;
    bottom: -10px;
    left: 0;
    width: 100px;
    height: 4px;
    background: linear-gradient(to right, #f093fb, #000000);
    border-radius: 2px;
}

/* Charts layout */
.charts-grid {
    display: grid;
    grid-template-columns: repeat(12, 1fr);
    grid-gap: 1.5rem;
    margin-bottom: 2.5rem;
}

.chart-module {
    background: linear-gradient(135deg, rgba(106, 81, 165, 0.2), rgba(255, 186, 164, 0.1));
    border-radius: 16px;
    border: 1px solid rgba(89, 81, 194, 0.775);
    overflow: hidden;
    transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
    position: relative;
    grid-column: span 6;
}

.wide-module {
    grid-column: span 12;
}

.featured-chart {
    grid-column: span 6;
    background: linear-gradient(135deg, rgba(106, 81, 165, 0.2), rgba(255, 186, 164, 0.1));
    border: 1px solid rgba(89, 81, 194, 0.775);
}

.chart-module:hover {
    transform: translateY(-5px);
    box-shadow: 0 15px 30px rgba(0, 0, 0, 0.3);
    border: 1px solid rgba(255, 255, 255, 0.2);
}

.chart-header {
    padding: 1.5rem;
    border-bottom: 1px solid rgba(255, 255, 255, 0.08);
    position: relative;
}

.chart-badge {
    position: absolute;
    top: 1.5rem;
    /* Fixed position to align with title */
    right: 1.5rem;
    background: linear-gradient(to right, #f093fb, #f5576c);
    padding: 5px 12px;
    border-radius: 20px;
    font-size: 0.75rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 1px;
    box-shadow: 0 4px 15px rgba(240, 147, 251, 0.5);
}

.chart-title {
    font-size: 1.25rem;
    font-weight: 600;
    margin: 0;
    display: flex;
    align-items: center;
}

.chart-icon {
    margin-right: 0.75rem;
    font-size: 1.5rem;
}

.chart-content {
    padding: 1.5rem;
    min-height: 300px;
}

/* Back button */
.navigation-action {
    display: flex;
    justify-content: flex-start;
}

.back-button {
    display: flex;
    align-items: center;
    background: linear-gradient(135deg, #6828fa, #ff5e62);
    border: none;
    color: white;
    padding: 0.75rem 1.5rem;
    border-radius: 50px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s ease;
    text-decoration: none;
    box-shadow: 0 10px 20px rgba(104, 40, 250, 0.4);
}

.back-button:hover {
    transform: translateY(-3px);
    box-shadow: 0 15px 25px rgba(104, 40, 250, 0.5);
    background: linear-gradient(135deg, #5f20fa, #ff4f58);
}

.back-icon {
    margin-right: 0.5rem;
    font-size: 1.25rem;
}

/* Responsive adjustments */
@media (max-width: 1024px) {
    .chart-module {
        grid-column: span 12;
    }

    .dashboard-content {
        padding: 1rem;
    }

    .glass-container {
        padding: 1.5rem;
    }
}

/* Additional styling for custom scrollbars */
::-webkit-scrollbar {
    width: 8px;
    height: 8px;
}

::-webkit-scrollbar-track {
    background: rgba(255, 255, 255, 0.05);
    border-radius: 10px;
}

::-webkit-scrollbar-thumb {
    background: linear-gradient(to bottom, #6828fa, #ff5e62);
    border-radius: 10px;
}
</style>