<template>
    <div>
        <UserNavbar />
        <div class="container mt-4">
            <h2 class="text-center mb-4">📊 Your Quiz Attempts</h2>

            <div v-if="quizAttempts.length > 0" class="row">
                <div v-for="quiz in quizAttempts" :key="quiz.quiz_id" class="col-md-6 mb-3">
                    <div class="card shadow-sm p-3">
                        <div class="card-body">
                            <h4 class="card-title">🎯 {{ quiz.quiz_name }}</h4>

                            <p class="card-text">
                                <strong>🏆 Max Score:</strong>
                                <span class="badge bg-success fs-6">{{ quiz.highest_score }}</span>
                            </p>

                            <h5 class="mt-3">📅 Previous Attempts:</h5>
                            <ul class="list-group">
                                <li v-for="attempt in quiz.attempts" :key="attempt.time_of_attempt"
                                    class="list-group-item">
                                    ⏳ <strong>{{ formatDateTime(attempt.time_of_attempt) }}</strong> -
                                    <span class="badge bg-primary">Score: {{ attempt.total_score }}</span>
                                </li>
                            </ul>
                        </div>
                    </div>
                </div>
            </div>

            <div v-else class="alert alert-warning text-center">
                🚨 No quiz attempts found. Try taking a quiz! 📝
            </div>
        </div>
    </div>
</template>


<script>
import UserNavbar from '@/components/UserNavbar.vue';

export default {
    components: { UserNavbar },
    data() {
        return {
            quizAttempts: []
        };
    },
    async mounted() {
        await this.fetchUserAttempts();
    },
    methods: {
        async fetchUserAttempts() {
            try {
                const response = await fetch("http://127.0.0.1:8080/my_attempts", {
                    method: "GET",
                    headers: {
                        "Content-Type": "application/json",
                        "Authorization": `Bearer ${localStorage.getItem('jwtToken')}`
                    }
                });

                if (!response.ok) {
                    throw new Error("Failed to fetch attempts");
                }

                this.quizAttempts = await response.json();
            } catch (error) {
                console.error("Error fetching attempts:", error);
            }
        },

        formatDateTime(dateTime) {
            const date = new Date(dateTime);
            return date.toLocaleString();
        }
    }
};
</script>

<style scoped>
.card {
    border-radius: 10px;
}
</style>
