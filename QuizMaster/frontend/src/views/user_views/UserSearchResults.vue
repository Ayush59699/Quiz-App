<template>
    <div>
        <AdminNavbar />
        <div class="container mt-5">

            <div class="text-center mb-4">
                <h3 class="fw-bold text-primary">🔍 Search Results for "{{ query }}"</h3>
            </div>

            <!-- Loading Indicator -->
            <div v-if="loading" class="text-center">
                <div class="spinner-border text-primary" role="status">
                    <span class="visually-hidden">Loading...</span>
                </div>
            </div>

            <div v-else>
                <div v-if="results.length > 0">

                    <!-- Subjects Section -->
                    <div v-if="subjects.length > 0" class="mb-4">
                        <h5 class="fw-bold text-success">📚 Subjects</h5>
                        <ul class="list-group">
                            <li v-for="(subject, index) in subjects" :key="'subject-' + index"
                                class="list-group-item shadow-sm rounded mb-2">
                                <span class="fw-semibold">{{ subject.name }}</span>
                                <ul class="mt-2">
                                    <li v-for="chapter in subject.chapters" :key="chapter.id">
                                        📖 {{ chapter.name }}
                                    </li>
                                </ul>
                            </li>
                        </ul>
                    </div>

                    <!-- Chapters Section -->
                    <div v-if="chapters.length > 0" class="mb-4">
                        <h5 class="fw-bold text-primary">📖 Chapters</h5>
                        <ul class="list-group">
                            <li v-for="(chapter, index) in chapters" :key="'chapter-' + index"
                                class="list-group-item shadow-sm rounded mb-2">
                                <span class="fw-semibold">{{ chapter.name }}</span>
                                <p class="text-muted m-0"><strong>Subject:</strong> {{ chapter.subject_name }}</p>
                                <p class="m-0">{{ chapter.description }}</p>
                                <ul class="mt-2">
                                    <li v-for="quiz in chapter.quizzes" :key="quiz.id">
                                        🎯 {{ quiz.name }}
                                    </li>
                                </ul>
                            </li>
                        </ul>
                    </div>

                    <!-- Quizzes Section -->
                    <div v-if="quizzes.length > 0" class="mb-4">
                        <h5 class="fw-bold text-warning">📝 Quizzes</h5>
                        <ul class="list-group">
                            <li v-for="(quiz, index) in quizzes" :key="'quiz-' + index"
                                class="list-group-item shadow-sm rounded mb-2">
                                <span class="fw-semibold">{{ quiz.name }}</span>
                            </li>
                        </ul>
                    </div>

                    <!-- Questions Section -->
                    <div v-if="questions.length > 0" class="mb-4">
                        <h5 class="fw-bold text-danger">❓ Questions</h5>
                        <ul class="list-group">
                            <li v-for="(question, index) in questions" :key="'question-' + index"
                                class="list-group-item shadow-sm rounded mb-2">
                                <span class="fw-semibold">{{ question.name }}</span>
                            </li>
                        </ul>
                    </div>

                </div>


                <div v-else class="text-center">
                    <p class="text-danger fs-5">❌ No results found.</p>
                </div>

                <div class="text-center mt-4">
                    <router-link to="/admin_dashboard" class="btn btn-outline-primary px-4 py-2 fw-bold">
                        ⬅ Back to Dashboard
                    </router-link>
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

    name: 'UserSearchResults',
    data() {
        return {
            results: [],
            subjects: [],
            chapters: [],
            quizzes: [],
            questions: [],
            loading: true,
            query: ''
        };
    },
    async mounted() {
        this.query = this.$route.params.query;
        await this.fetchResults();
    },
    watch: {
        '$route.params.query': 'fetchResults'
    },
    methods: {
        async fetchResults() {
            this.loading = true;
            try {
                const response = await fetch(`http://127.0.0.1:8080/user_search/${this.query}`, {
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${localStorage.getItem('jwtToken')}`
                    }
                });
                if (!response.ok) {
                    throw new Error(`HTTP error! Status ${response.status}`);
                }
                const data = await response.json();
                console.log("Fetched data from search :", data)

                this.subjects = data.filter(item => item.type === "Subject");
                this.chapters = data.filter(item => item.type === "Chapter");
                this.quizzes = data.filter(item => item.type === "Quiz");
                this.questions = data.filter(item => item.type === "Question");

                this.results = data;

            } catch (error) {
                console.error('Error fetching search results:', error);
                this.results = [];
            } finally {
                this.loading = false;
            }
        }
    }
};
</script>
<style scoped>
.list-group-item {
    transition: all 0.1s ease-in-out;
    background: #f8f9fa;
    border: 1px solid #ddd;
}

.list-group-item:hover {
    transform: scale(1.02);
    background: #eef5ff;
}

h3 {
    text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.1);
}

.btn-outline-primary:hover {
    background: #0d6efd;
    color: white;
}
</style>