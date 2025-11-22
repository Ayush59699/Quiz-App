<template>
  <div>
    <AdminNavbar />

    <!-- Quiz Form -->
    <div class="container py-4">
      <div class="card shadow">
        <div class="card-header bg-primary text-white">
          <h2 class="h4 mb-0">Add Quiz</h2>
        </div>
        <div class="card-body">
          <form @submit.prevent="addQuiz" class="needs-validation" novalidate>
            <div class="mb-3">
              <label for="quizName" class="form-label">Quiz Title</label>
              <input type="text" class="form-control" id="quizName" v-model="quizName" placeholder="Enter quiz name"
                required>
              <div class="form-text">Give your quiz a descriptive title</div>
            </div>

            <div class="mb-3">
              <label for="quizDate" class="form-label">Quiz Date</label>
              <input type="date" class="form-control" id="quizDate" v-model="quizDate" required>
            </div>

            <div class="mb-3">
              <label for="quizDuration" class="form-label">Quiz Duration</label>
              <div class="input-group">
                <input type="number" class="form-control" id="quizDuration" v-model="quizDuration"
                  placeholder="Enter duration" min="1" required>
                <span class="input-group-text">seconds</span>
              </div>
            </div>

            <div class="mb-4">
              <label for="chapterId" class="form-label">Select Chapter</label>
              <select class="form-select" id="chapterId" v-model="chapterId" required>
                <option value="" disabled selected>Select Chapter</option>
                <option v-for="chapter in chapters" :key="chapter.id" :value="chapter.id">
                  {{ chapter.chapter_name }}
                </option>
              </select>
            </div>

            <div class="d-flex justify-content-between">
              <button type="button" class="btn btn-outline-secondary" @click="cancel">Cancel</button>
              <button type="submit" class="btn btn-primary">
                <i class="bi bi-plus-circle me-2"></i>Add Quiz
              </button>
            </div>
          </form>
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

  data() {
    return {
      quizName: '',
      quizDate: '',
      quizDuration: '',
      chapterId: '',
      chapters: []
    };
  },
  mounted() {
    this.fetchChapters();
  },
  methods: {
    async fetchChapters() {
      try {
        const response = await fetch('http://127.0.0.1:8080/get_get_chapters', {
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${localStorage.getItem('jwtToken')}`
          }
        });
        this.chapters = await response.json();
      } catch (error) {
        console.error("Error fetching chapters:", error);
      }
    },
    async addQuiz() {
      if (!this.chapterId || !this.quizName || !this.quizDate || !this.quizDuration) {
        alert("All fields are required!");
        return;
      }

      try {
        const response = await fetch('http://127.0.0.1:8080/add_quiz', {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            'Authorization': `Bearer ${localStorage.getItem('jwtToken')}`
          },

          body: JSON.stringify({
            chapter_id: this.chapterId,
            quiz_name: this.quizName,
            date_of_quiz: this.quizDate,
            time_duration: parseInt(this.quizDuration)
          })
        });

        if (response.ok) {
          alert("Quiz added successfully!");
          this.$router.push('/quiz_management')
          //setTimeout(() => location.reload(), 2000); // Refresh UI after 2 sec
        } else {
          const result = await response.json();
          alert("Error: " + result.error);
        }
      } catch (error) {
        console.error("Error adding quiz:", error);
      }
    }
  }
};
</script>
