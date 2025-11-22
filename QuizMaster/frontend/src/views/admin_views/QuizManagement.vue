<template>
    <div>
        <AdminNavbar />

        <div class="container quiz-management">
            <h3 class="mt-4 page-title">📚 Quiz Management</h3>

            <button class="btn btn-warning add-quiz-btn" @click="this.$router.push('/add_quiz')">
                ➕ Add Quiz
            </button>

            <p v-if="error" class="text-danger">{{ error }}</p>

            <div v-if="quizzes.length" class="row">
                <div v-for="quiz in quizzes" :key="quiz.id" class="col-md-6 col-lg-4">
                    <div class="card quiz-card shadow-sm">
                        <div class="card-header quiz-header">
                            <h5 class="mb-0">
                                <a href="#" @click.prevent="fetchQuizDetails(quiz.id)" class="quiz-title">
                                    {{ quiz.quiz_name }}
                                </a>
                            </h5>
                            <div class="quiz-actions">
                                <button class="btn btn-light btn-sm" @click="openQuizEditModal(quiz)">✏️ Edit</button>
                                <button class="btn btn-danger btn-sm" @click="deleteQuiz(quiz.id)">🗑️ Delete</button>
                            </div>
                        </div>

                        <div class="card-body">
                            <p><strong>📅 Date:</strong> {{ quiz.date_of_quiz }}</p>
                            <p><strong>⏳ Duration:</strong> {{ quiz.time_duration }} sec</p>
                            <p><strong>📖 Chapter ID:</strong> {{ quiz.chapter_id }}</p>

                            <h6 class="mt-3">📝 Questions:</h6>
                            <ul v-if="quiz.questions.length" class="list-group question-list">
                                <li v-for="question in quiz.questions" :key="question.id" class="list-group-item">
                                    <span><strong>{{ question.question_statement }}</strong></span>
                                    <div>
                                        <button class="btn btn-warning btn-sm me-2" @click="openEditModal(question)">✏️
                                            Edit</button>
                                        <button class="btn btn-danger btn-sm" @click="deleteQuestion(question.id)">🗑️
                                            Delete</button>
                                    </div>
                                </li>
                            </ul>
                            <p v-else class="text-muted">No questions available</p>

                            <button class="btn btn-success add-question-btn"
                                @click="$router.push({ path: '/add_question', query: { quiz_id: quiz.id, chapter_id: quiz.chapter_id } })">
                                ➕ Add Question
                            </button>
                        </div>
                    </div>
                </div>
            </div>

            <p v-else class="text-muted">No quizzes found.</p>

            <!-- Edit Quiz Modal -->
            <div v-if="editQuizModalOpen" class="modal fade show modal-overlay">
                <div class="modal-dialog">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h5 class="modal-title">✏️ Edit Quiz</h5>
                            <button type="button" class="btn-close" @click="editQuizModalOpen = false"></button>
                        </div>
                        <div class="modal-body">
                            <label>Quiz Name:</label>
                            <input v-model="editQuizData.quiz_name" type="text" class="form-control mb-2" />

                            <label>Quiz Date:</label>
                            <input v-model="editQuizData.date_of_quiz" type="date" class="form-control mb-2" />

                            <label>Time Duration (Seconds):</label>
                            <input v-model.number="editQuizData.time_duration" type="number"
                                class="form-control mb-2" />
                        </div>
                        <div class="modal-footer">
                            <button class="btn btn-secondary" @click="editQuizModalOpen = false">Cancel</button>
                            <button class="btn btn-primary" @click="updateQuiz">Save Changes</button>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Edit Question Modal -->
            <div v-if="editModalOpen" class="modal fade show modal-overlay">
                <div class="modal-dialog">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h5 class="modal-title">✏️ Edit Question</h5>
                            <button type="button" class="btn-close" @click="editModalOpen = false"></button>
                        </div>
                        <div class="modal-body">
                            <label>Question Statement:</label>
                            <input v-model="editQuestionData.question_statement" type="text"
                                class="form-control mb-2" />

                            <label>Option 1:</label>
                            <input v-model="editQuestionData.option1" type="text" class="form-control mb-2" />

                            <label>Option 2:</label>
                            <input v-model="editQuestionData.option2" type="text" class="form-control mb-2" />

                            <label>Option 3:</label>
                            <input v-model="editQuestionData.option3" type="text" class="form-control mb-2" />

                            <label>Option 4:</label>
                            <input v-model="editQuestionData.option4" type="text" class="form-control mb-2" />

                            <label>Correct Answer:</label>
                            <input v-model.number="editQuestionData.correct_option" type="text"
                                class="form-control mb-2" />
                        </div>
                        <div class="modal-footer">
                            <button class="btn btn-secondary" @click="editModalOpen = false">Cancel</button>
                            <button class="btn btn-primary" @click="updateQuestion">Save Changes</button>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Quiz Details Modal -->
            <div v-if="selectedQuiz" class="modal fade show modal-overlay">
                <div class="modal-dialog">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h5 class="modal-title">📋 Quiz Details</h5>
                            <button type="button" class="btn-close" @click="selectedQuiz = null"></button>
                        </div>
                        <div class="modal-body">
                            <p><strong>Quiz Name:</strong> {{ selectedQuiz.quiz_name }}</p>
                            <p><strong>Date:</strong> {{ selectedQuiz.date_of_quiz }}</p>
                            <p><strong>Duration:</strong> {{ selectedQuiz.time_duration }} sec</p>
                            <p><strong>Chapter Name:</strong> {{ selectedQuiz.chapter_name }}</p>
                            <p><strong>Subject Name:</strong> {{ selectedQuiz.subject_name }}</p>


                        </div>
                    </div>
                </div>
            </div>




        </div>
    </div>
</template>

<script>
import AdminNavbar from '@/components/AdminNavbar.vue';
export default {
    components: {
        AdminNavbar
    },
    name: 'QuizManagement',
    data() {
        return {
            admin_name: '',
            quizzes: [],
            questions: [],
            error: '',
            selectedQuiz: null,
            editModalOpen: false,
            editQuestionData: {
                id: null,
                question_statement: '',
                option1: '',
                option2: '',
                option3: '',
                option4: '',
                correct_option: 1
            },
            editQuizModalOpen: false,
            editQuizData: {
                id: null,
                quiz_name: '',
                date_of_quiz: '',
                time_duration: null
            },

        };
    },
    async mounted() {
        const admin_name = localStorage.getItem('admin_name') || 'admin'
        this.admin_name = admin_name
        await this.fetch_data();


    },
    methods: {
        openQuizEditModal(quiz) {
            this.editQuizData = { ...quiz };
            this.editQuizModalOpen = true;
        },
        async updateQuiz() {
            try {
                const response = await fetch('http://127.0.0.1:8080/edit_quiz', {
                    method: "PUT",
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${localStorage.getItem('jwtToken')}`
                    },
                    body: JSON.stringify({
                        id: this.editQuizData.id,
                        quiz_name: this.editQuizData.quiz_name,
                        date_of_quiz: this.editQuizData.date_of_quiz,
                        time_duration: this.editQuizData.time_duration
                    })
                });

                if (!response.ok) {
                    throw new Error(`Error: ${response.status}`);
                }

                alert("Quiz updated successfully!");
                this.editQuizModalOpen = false;
                await this.fetch_data(); // Refresh quiz list
            } catch (error) {
                console.error("Error updating quiz:", error);
            }
        },

        openEditModal(question) {
            this.editQuestionData = { ...question }; // Clone question data into modal
            this.editModalOpen = true;
        },
        async updateQuestion() {
            try {
                const response = await fetch(`http://127.0.0.1:8080/edit_question/${this.editQuestionData.id}`, {
                    method: "PUT",
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${localStorage.getItem('jwtToken')}`,
                    },
                    body: JSON.stringify(this.editQuestionData)
                });

                if (!response.ok) {
                    throw new Error(`Error: ${response.status}`);
                }

                alert("Question updated successfully!");
                this.editModalOpen = false;
                await this.fetch_data(); // Refresh data
            } catch (error) {
                console.error("Error updating question:", error);
            }
        },
        async fetchQuizDetails(quizId) {
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
                console.log(this.selectedQuiz)
            } catch (error) {
                console.error("Error fetching quiz details:", error);
            }
        },
        async fetch_data() {
            try {
                const response = await fetch("http://127.0.0.1:8080/quiz_management", {
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
                this.quizzes = data
                console.log(data)
            }
            catch (error) {
                console.error("Error Fetching Quizzes", error);
                this.error = 'Failed to fetch quizzes. Try again!';
            }
        },
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
                    window.location.href = '/';
                }
            } catch (error) {
                console.error("Logout Failes", error);
            }
        },
        async deleteQuestion(questionId) {
            if (!confirm("Are you sure you want to delete this question?")) return;

            try {
                const response = await fetch(`http://127.0.0.1:8080/delete_question/${questionId}`, {
                    method: "DELETE",
                    headers: {
                        'Authorization': `Bearer ${localStorage.getItem('jwtToken')}`,
                    },
                });

                if (!response.ok) {
                    throw new Error(`Error: ${response.status}`);
                }

                alert("Question deleted successfully!");
                await this.fetch_data(); // Refresh data
            } catch (error) {
                console.error("Error deleting question:", error);
            }
        },

        async deleteQuiz(quizId) {
            if (!confirm("Are you sure you want to delete this Quiz?")) return;

            try {
                const response = await fetch(`http://127.0.0.1:8080/delete_quiz/${quizId}`, {
                    method: "DELETE",
                    headers: {
                        'Authorization': `Bearer ${localStorage.getItem('jwtToken')}`,
                    },
                });

                if (!response.ok) {
                    throw new Error(`Error: ${response.status}`);
                }

                alert("Quiz deleted successfully!");
                await this.fetch_data(); // Refresh data
            } catch (error) {
                console.error("Error deleting question:", error);
            }
        },



    }
};
</script>
<style>
.quiz-management {
    max-width: 1200px;
    margin: auto;
}

.page-title {
    font-size: 2rem;
    font-weight: bold;
    color: #4e73df;
    text-align: center;
}

.add-quiz-btn {
    display: block;
    width: fit-content;
    margin: 1rem auto;
}

.quiz-card {
    border-radius: 10px;
    transition: transform 0.2s ease-in-out;
}

.quiz-card:hover {
    transform: scale(1.03);
}

.quiz-header {
    background: linear-gradient(90deg, #4e73df, #36b9cc);
    color: white;
    padding: 10px 15px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.quiz-title {
    text-decoration: none;
    color: white;
    font-weight: bold;
}

.quiz-actions button {
    margin-left: 5px;
}

.question-list {
    max-height: 200px;
    overflow-y: auto;
}

.add-question-btn {
    width: 100%;
    font-weight: bold;
}

.modal-overlay {
    display: block;
    background: rgba(0, 0, 0, 0.5);
}

.modal-content {
    border-radius: 10px;
    padding: 20px;
}
</style>
