<template>
    <div>
        <UserNavbar />

        <div class="container mt-4">
            <h3> Welcome to {{ username }}'s Dashboard' </h3>
            <br>
            <h2 class="mb-4"> Upcoming quizzes:</h2>
            <hr>
            <!-- Loading state -->
            <div v-if="loading" class="text=center">
                <div class="spinner-border" role="status">
                    <span class='visually-hidden'>Loading...</span>
                </div>
            </div>
            <div v-if='error' class="alert alert-danger" role="alert">
                {{ error }}
            </div><br>

            <div v-if="!loading && (!activeQuizzes || activeQuizzes.length === 0)" class="alert alert-info">
                No upcoming quizzes available at this moment. Check back later!
            </div>

            <div class="row row-cols-1 row-cols-md-2 row-cols-lg-3 g-4">
                <div v-for="quiz in activeQuizzes" :key="quiz.id" class="col">
                    <div class="card h-100">
                        <div class="card-header bg-primary text-white">
                            {{ quiz.quiz_name }}
                        </div>
                        <div class="card-body">
                            <h5 class="card-title">{{ quiz.quiz_name }}</h5> <!-- FIXED -->
                            <p class="card-text">This quiz has {{ quiz.questions.length }} questions.</p> <!-- FIXED -->

                            <ul class="list-group list-group-flush mb-3">
                                <li class="list-group-item"><strong>Date:</strong> {{ formatDate(quiz.date_of_quiz) }}
                                </li>
                                <li class="list-group-item"><strong>Duration:</strong> {{ quiz.time_duration }} seconds
                                </li>
                                <li class="list-group-item"><strong>Questions:</strong> {{ quiz.questions ?
                                    quiz.questions.length : 0 }}</li>
                            </ul>
                            <button class="btn btn-primary me-2" @click="viewQuizDetails(quiz.id)"> View Quiz
                                Details</button>

                            <div v-if="quiz.questions.length > 0">
                                <button class="btn btn-success" @click="takeQuiz(quiz.id)">Start Quiz</button>
                            </div>
                            <div v-else>
                                <button class="btn btn-success" @click="takeQuiz(quiz.id)" disabled>Locked[Empty
                                    Quiz]</button>

                            </div>


                        </div>
                    </div>
                </div>
            </div>

            <br>
            <hr>
            <h2 class="mb-4"> Expired quizzes:</h2>
            <hr><br>
            <div v-if="!loading && (!expiredQuizzes || expiredQuizzes.length === 0)" class="alert alert-info">
                No upcoming quizzes available at this moment. Check back later!
            </div>

            <div class="row row-cols-1 row-cols-md-2 row-cols-lg-3 g-4">
                <div v-for="quiz in expiredQuizzes" :key="quiz.id" class="col">
                    <div class="card h-100 border-danger">
                        <div class="card-header bg-danger text-white">
                            {{ quiz.quiz_name }} (Expired)
                        </div>
                        <div class="card-body">
                            <h5 class="card-title">{{ quiz.quiz_name }}</h5>
                            <p class="card-text">This quiz had {{ quiz.questions ? quiz.questions.length : 0 }}
                                questions.</p>
                            <ul class="list-group list-group-flush mb-3">
                                <li class="list-group-item"><strong>Date:</strong> {{ formatDate(quiz.date_of_quiz) }}
                                </li>
                                <li class="list-group-item"><strong>Duration:</strong> {{ quiz.time_duration }} seconds
                                </li>
                            </ul>
                            <button class="btn btn-secondary" disabled>
                                🔒 Locked / Expired
                            </button>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Modal for Viewing Quiz Details -->
            <div v-if="selectedQuiz">
                <div class="modal fade show d-block" style="background: rgba(0,0,0,0.5)">
                    <div class="modal-dialog modal-dialog-centered">
                        <div class="modal-content">
                            <div class="modal-header">
                                <h5 class="modal-title">{{ selectedQuiz.quiz_name }} Details</h5>
                                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"
                                    @click="selectedQuiz = null"></button>
                            </div>
                            <div class="modal-body">
                                <p><strong>Quiz ID:</strong> {{ selectedQuiz.quiz_id }}</p>
                                <p><strong>Chapter Name:</strong> {{ selectedQuiz.chapter_name }}</p>
                                <p><strong>Subject Name:</strong> {{ selectedQuiz.subject_name }}</p>
                                <p><strong>Date:</strong> {{ selectedQuiz.date_of_quiz }}</p>
                                <p><strong>Duration:</strong> {{ selectedQuiz.time_duration }} minutes</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            z

        </div>
    </div>
</template>


<script>
import UserNavbar from '@/components/UserNavbar.vue';

export default {
    components: {
        UserNavbar
    },

    name: 'UserDashboard',
    data() {
        return {
            username: '',
            upcomingQuizzes: [],
            activeQuizzes: [],
            expiredQuizzes: [],
            loading: true,
            error: null,
            selectedQuiz: null

        };

    },
    created() {
        this.fetchUpcomingQuizzes();
    },

    async mounted() {
        this.username = localStorage.getItem('user_name')
        this.fetch_data()

    },

    methods: {

        async exportQuizData() {
            try {
                const response = await fetch("http://127.0.0.1:8080/export_quiz_data", {
                    method: "POST",
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${localStorage.getItem('jwtToken')}`
                    }
                })
                if (!response.ok) {
                    throw new Error(`Error: ${response.status}`);
                }
                const data = await response.json()
                console.log(data)





            } catch (error) {
                console.error(error);
                alert("Failed to export quiz data.");
            }
        },


        async viewQuizDetails(quizId) {
            console.log("Fetching details for Quiz ID:", quizId);
            try {
                const response = await fetch(`http://127.0.0.1:8080/view_quiz_details/${quizId.replace(/-/g, "")}`, {
                    method: "GET",
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${localStorage.getItem('jwtToken')}`,
                    },
                });

                if (!response.ok) {
                    throw new Error(`Error: ${response.status}`);
                }

                this.selectedQuiz = await response.json();
            } catch (error) {
                console.error("Error fetching quiz details:", error);
            }
        },

        async fetchUpcomingQuizzes() {
            this.loading = true
            this.error = null

            try {
                const token = localStorage.getItem('jwtToken')
                if (!token) {
                    this.$router.push('/user_login')
                    return
                }
                const response = await fetch('http://127.0.0.1:8080/user_dashboard', {
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${token}`
                    }
                });
                const data = await response.json()


                if (!response.ok) throw new Error(data.message || "Failed to fetch incoming quizzes")
                this.activeQuizzes = data.active_quizzes;
                this.expiredQuizzes = data.expired_quizzes;

            }
            catch (error) {
                console.error('Error fetching quizzes', error)
                this.error = error.message
            } finally {
                this.loading = false;
            }
        },

        formatDate(dateString) {
            const options = { year: 'numeric', month: 'long', day: 'numeric' };
            return new Date(dateString).toLocaleDateString(undefined, options);
        },

        takeQuiz(quizId) {
            if (window.confirm("Are you ready to take the Quiz?")) {
                this.$router.push(`/take_quiz/${quizId} `);

            }

        },

        async fetch_data() {
            try {
                const response = await fetch("http://127.0.0.1:8080/user_dashboard", {
                    method: "GET",
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${localStorage.getItem('jwtToken')}`,
                    },
                });

                if (!response.ok) {
                    throw new Error(`HTTP error! Status: ${response.status}`);
                }

                const data = await response.json()
                console.log(data)
                this.users = data.users
                this.subjects = data.subjects


            }
            catch (error) {
                console.log("Some error:", error);
            }
        },

        async logout() {
            localStorage.removeItem('jwtToken');
            localStorage.removeItem('user_name');
            localStorage.removeItem('user_email');
            this.$router.push('/');
        }
    }

}
</script>
<style scoped>
.card {
    transition: transform 0.3s ease;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.card:hover {
    transform: translateY(-5px);
    box-shadow: 0 10px 20px rgba(0, 0, 0, 0.2);
}

.btn-primary {
    background-color: #0d6efd;
    border-color: #0d6efd;
}

.btn-primary:hover {
    background-color: #0b5ed7;
    border-color: #0a58ca;
}
</style>