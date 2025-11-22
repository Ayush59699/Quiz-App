<template>
    <div>
        <AdminNavbar />


        <h3 class="mt-3">Chapter's Quiz Management</h3>

        <button class="btn btn-warning m-2" @click="this.$router.push('/add_quiz')"> Want to add more quiz to the list ?
            + Add Quiz</button>

        <p v-if="error" class="text-danger">{{ error }}</p>

        <div v-if="quizzes.length" class="row">
            <div v-for="quiz in quizzes" :key="quiz.id" class="col-md-4">
                <div class="card mb-3 shadow">
                    <div class="card-header bg-primary text-white">
                        <h5 class="mb-0">
                            <a href="#" @click.prevent="fetchQuizDetails(quiz.id)" class="text-white">
                                {{ quiz.quiz_name }}
                            </a>
                        </h5>
                    </div>
                    <div class="card-body">
                        <p><strong>Date:</strong> {{ quiz.date_of_quiz }}</p>
                        <p><strong>Duration:</strong> {{ quiz.time_duration }} sec</p>
                        <p><strong>Chapter ID:</strong> {{ quiz.chapter_id }}</p>


                        <h6 class="mt-3">Questions:</h6>
                        <ul v-if="quiz.questions.length" class="list-group">
                            <li v-for="question in quiz.questions" :key="question.id" class="list-group-item">
                                <span><strong>{{ question.question_statement }}</strong></span>
                                <div>


                                    <button class="btn btn-warning btn-sm me-2"
                                        @click="openEditModal(question)">Edit</button>

                                    <button class="btn btn-danger btn-sm" @click="deleteQuestion(question.id)">
                                        Delete
                                    </button>

                                </div>

                            </li>
                        </ul>
                        <p v-else class="text-muted">No questions available</p>

                        <button class="btn btn-success mt-3 w-100"
                            @click="$router.push({ path: '/add_question', query: { quiz_id: quiz.id, chapter_id: quiz.chapter_id } })">
                            <!--, subject_id: quiz.chapter.subject_id -->
                            + Add Question
                        </button>
                        <!-- EDIT ROUTE HERE-->


                    </div>

                </div>
            </div>
        </div>

        <p v-else>No quizzes found.</p>

        <!-- Modal for showing quiz details -->
        <div v-if="selectedQuiz" class="modal fade show" style="display: block; background: rgba(0,0,0,0.5)">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">{{ selectedQuiz.quiz_name }} Details</h5>
                        <button type="button" class="btn-close" @click="selectedQuiz = null"></button>
                    </div>
                    <div class="modal-body">
                        <p><strong>Quiz ID :</strong> {{ selectedQuiz.quiz_id }}</p>

                        <p><strong>Chapter ID :</strong> {{ selectedQuiz.chapter_id }}</p>
                        <p><strong>Chapter Name :</strong> {{ selectedQuiz.chapter_name }}</p>

                        <p><strong>Subject Name :</strong> {{ selectedQuiz.subject_name }}</p>
                        <p><strong>Quiz Date :</strong> {{ selectedQuiz.date_of_quiz }}</p>
                        <p><strong>Time Duration :</strong> {{ selectedQuiz.time_duration }} minutes</p>
                    </div>
                </div>
            </div>
        </div>

        <!-- Modal for Editing Questions-->
        <div v-if="editModalOpen" class="modal fade show" style="display: block; background: rgba(0,0,0,0.5)">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">Edit Question</h5>
                        <button type="button" class="btn-close" @click="editModalOpen = false"></button>
                    </div>
                    <div class="modal-body">
                        <label>Question Statement:</label>
                        <input v-model="editQuestionData.question_statement" type="text" class="form-control mb-2" />

                        <label>Option 1:</label>
                        <input v-model="editQuestionData.option1" type="text" class="form-control mb-2" />

                        <label>Option 2:</label>
                        <input v-model="editQuestionData.option2" type="text" class="form-control mb-2" />

                        <label>Option 3:</label>
                        <input v-model="editQuestionData.option3" type="text" class="form-control mb-2" />

                        <label>Option 4:</label>
                        <input v-model="editQuestionData.option4" type="text" class="form-control mb-2" />

                        <label>Correct Answer</label>

                        <input v-model.number="editQuestionData.correct_option" type="text" class="form-control mb-2" />
                    </div>
                    <div class="modal-footer">
                        <button class="btn btn-secondary" @click="editModalOpen = false">Cancel</button>
                        <button class="btn btn-primary" @click="updateQuestion">Save Changes</button>
                    </div>
                </div>
            </div>
        </div>

    </div>
</template>


<script>
import AdminNavbar from '@/components/AdminNavbar.vue';
export default {
    props: ['chapterId'],
    components: {
        AdminNavbar
    },
    name: 'ManageChapterQuizzes',
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

        };
    },
    async mounted() {
        const admin_name = localStorage.getItem('admin_name') || 'admin'
        this.admin_name = admin_name
        const chapterId = this.$route.params.chapterId;
        if (!chapterId) {
            console.log("Chapter id is undefined bhidu.....")
            this.error = 'Invalid Chapter ID'
            return;
        }
        await this.fetch_data(chapterId);


    },
    methods: {
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
            } catch (error) {
                console.error("Error fetching quiz details:", error);
            }
        },

        async fetch_data(chapterId) {
            console.log("Fetching QuIZZES for Chapter ID:", chapterId);
            try {
                const response = await fetch(`http://127.0.0.1:8080/manage_chapter_quizzes/${chapterId.replace(/-/g, "")}`, {
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

    }
};
</script>