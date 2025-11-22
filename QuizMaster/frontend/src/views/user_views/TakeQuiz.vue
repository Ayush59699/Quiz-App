<template>
    <div class="container">
        <div class="container mt-5">
            <div v-if="showScore" class="card text-center p-4">
                <h2 class="card-title">Quiz Complete!</h2>
                <p class="fs-4">Your final score: {{ score }} out of {{ questions.length }}</p>
                <button class="btn btn-primary mt-3" @click="restartQuiz">Try Again</button>
            </div>

            <div v-else class="card p-4">
                <h2 class="card-title">Here is your Quiz</h2>
                <p class="text-muted">Question {{ currentQuestion + 1 }} of {{ questions.length }}</p>
                <p class="text-muted">Score: {{ score }}</p>
                <p class="fw-bold text-danger">{{ timeLeft }} seconds remaining</p>

                <h3 class="mt-3" v-if="questions.length > 0 && questions[currentQuestion]">
                    {{ questions[currentQuestion].question_statement }}
                </h3>
                <div class="d-grid gap-2" v-if="questions.length > 0 && questions[currentQuestion]">
                    <button v-for="option in [
                        questions[currentQuestion]?.option1,
                        questions[currentQuestion]?.option2,
                        questions[currentQuestion]?.option3,
                        questions[currentQuestion]?.option4
                    ]" :key="option" class="btn"
                        :class="selectedAnswers[currentQuestion] === option ? 'btn-primary' : 'btn-outline-secondary'"
                        @click="handleAnswer(option)">
                        {{ option }}
                    </button>
                </div>

                <div class="d-flex justify-content-between mt-4">
                    <button class="btn btn-secondary" @click="previousQuestion" :disabled="currentQuestion === 0">
                        Previous
                    </button>
                    <button class="btn btn-secondary" @click="nextQuestion"
                        :disabled="currentQuestion === questions.length - 1">
                        Next
                    </button>
                </div>

                <div class="text-center mt-4">
                    <button class="btn btn-success" @click="submitQuiz">Submit Quiz</button>
                </div>
            </div>
        </div>
        <button class="btn btn-danger position-absolute top-0 end-0 m-3" @click="exitExam()">Exit Quiz</button>

    </div>
</template>

<script>
export default {
    name: 'TakeQuiz',
    data() {
        return {
            currentQuestion: 0,
            score: 0,
            showScore: false,
            selectedAnswers: Array(5).fill(null),

            quizId: '',
            qtn: [],
            timeLeft: 60,
            questions: [],
        };
    },

    mounted() {
        this.quizId = this.$route.params.quizId;
        if (this.quizId) {
            this.fetch_data();
            //this.startTimer();
        } else {
            console.log('QUIZ ID IS MISSING')
        }

    },

    methods: {
        async fetch_data() {
            try {
                const response = await fetch(`http://127.0.0.1:8080/take_quiz/${this.quizId}`, {
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${localStorage.getItem('jwtToken')}`
                    },
                });

                if (!response.ok) {
                    throw new Error("Failed to fetch incoming questions");
                }

                const data = await response.json()
                if (!data) {
                    console.log("Data missing")
                }

                this.questions = data.questions;
                console.log(this.questions)
                this.timeLeft = data.time_duration; // Set time dynamically
                console.log("Quiz Time Duration:", this.timeLeft, "seconds");

                this.startTimer();

            }
            catch (error) {
                console.log('Error', error)
            }
        },

        startTimer() {
            this.timer = setInterval(() => {
                if (this.timeLeft > 0 && !this.showScore) {
                    this.timeLeft--;
                } else {
                    this.showScore = true;
                    clearInterval(this.timer);
                }
            }, 1000);
        },

        handleAnswer(option) {
            this.selectedAnswers[this.currentQuestion] = option;
        },
        nextQuestion() {
            if (this.currentQuestion < this.questions.length - 1) {
                this.currentQuestion++;
            }
        },
        previousQuestion() {
            if (this.currentQuestion > 0) {
                this.currentQuestion--;
            }
        },
        submitQuiz() {
            this.score = this.questions.filter((q, index) => q.correct_option === this.selectedAnswers[index]).length;
            this.showScore = true;
            clearInterval(this.timer);

            this.saveQuizScore(); // send score to backend
        },

        async saveQuizScore() {
            const quiz_id = this.quizId?.trim(); // Ensure it's a valid UUID string

            console.log("Attempting to send quiz_id:", quiz_id, "(Type:", typeof quiz_id, ")");


            try {
                const response = await fetch(`http://127.0.0.1:8080/save_score`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${localStorage.getItem('jwtToken')}`
                    },
                    body: JSON.stringify({
                        quiz_id: this.quizId,
                        total_score: this.score
                    })
                });
                const data = await response.json()
                console.log('Saved data', data)
            }
            catch (error) {
                console.log(error)
            }
        },

        restartQuiz() {
            this.currentQuestion = 0;
            this.score = 0;
            this.showScore = false; 
            this.selectedAnswers = Array(this.questions.length).fill(null);
            this.timeLeft = this.questions.length > 0 ? this.timeLeft : 60;
            clearInterval(this.timer);
            this.startTimer();
        },
        exitExam() {
            if (confirm("Are you sure you want to exit the quiz? Your progress will not be saved!")) {
                this.$router.push('/user_dashboard')
            }
        }

    }
}

</script>
<style>
.card {
    max-width: 600px;
    margin: auto;
}
</style>