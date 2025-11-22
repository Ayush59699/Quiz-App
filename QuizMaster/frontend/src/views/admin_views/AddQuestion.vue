<template>
  <div>
    <AdminNavbar />

    <div class="container py-4">
      <div class="card shadow">
        <div class="card-header bg-primary text-white">
          <h2 class="h4 mb-0">Add Question</h2>
        </div>
        <div class="card-body">
          <div class="mb-4">
            <p class="mb-2"><strong>Admin Name:</strong> <span class="fw-bold">{{ admin_name }}</span></p>
            <p class="mb-2"><strong>Chapter Name:</strong> <span class="fw-bold">{{ chapterName }}</span></p>
          </div>

          <form @submit.prevent="addQuestion">
            <div class="mb-3">
              <label for="questionStatement" class="form-label">Question Statement</label>
              <input type="text" class="form-control" id="questionStatement" v-model="new_question.question_statement"
                placeholder="Enter question statement" required />
            </div>

            <div class="mb-3">
              <label for="option1" class="form-label">Option 1</label>
              <input type="text" class="form-control" id="option1" v-model="new_question.option1"
                placeholder="Enter option 1" required />
            </div>

            <div class="mb-3">
              <label for="option2" class="form-label">Option 2</label>
              <input type="text" class="form-control" id="option2" v-model="new_question.option2"
                placeholder="Enter option 2" required />
            </div>

            <div class="mb-3">
              <label for="option3" class="form-label">Option 3</label>
              <input type="text" class="form-control" id="option3" v-model="new_question.option3"
                placeholder="Enter option 3" required />
            </div>

            <div class="mb-3"><label for="option4" class="form-label">Option 4</label>
              <input type="text" class="form-control" id="option4" v-model="new_question.option4"
                placeholder="Enter option 4" required />
            </div>

            <div class="mb-4">
              <label for="correctOption" class="form-label">Correct Answer</label><input type="text"
                class="form-control" id="correctOption" v-model="new_question.correct_option"
                placeholder="Enter Correct Answer" required />
            </div>

            <div class="d-grid">
              <button type="submit" class="btn btn-primary">Add Question</button>
            </div>


            <!-- Toast Notification -->
            <div v-if="showToast" class="toast-container ">
              <div class="toast-content">
                <p>✅ Question added successfully!</p>
              </div>
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
  name: 'AddQuestion',
  data() {
    return {
      showToast: false,
      admin_name: '',
      quiz_id: '',
      chapter_id: '',
      chapterName: '',
      new_question: {
        quiz_id: '',
        question_statement: '',
        option1: '',
        option2: '',
        option3: '',
        option4: '',
        correct_option: '',
      },

    };
  },
  async mounted() {
    const admin_name = localStorage.getItem('admin_name') || 'admin'
    this.admin_name = admin_name

    const urlParams = new URLSearchParams(window.location.search);
    this.quiz_id = urlParams.get('quiz_id')
    this.chapter_id = urlParams.get('chapter_id')

    if (this.quiz_id) console.log('QUIZ ID:', this.quiz_id)
    if (this.quiz_id) this.new_question.quiz_id = this.quiz_id;

    if (this.chapter_id) console.log('Chapter ID:', this.chapter_id)
    await this.fetchChapterName();



  },
  methods: {
    async fetchChapterName() {
      try {
        const response = await fetch(`http://127.0.0.1:8080/get_chapter/${this.chapter_id}`, {
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${localStorage.getItem('jwtToken')}`
          }

        });

        if (!response.ok) throw new Error(`HTTP error! Status: ${response.status}`);
        const data = await response.json();
        this.chapterName = data.chapter_name;
      }
      catch (error) {
        console.error("Error fetching chapter:", error);
      }
    },

    async addQuestion() {
      try {
        const response = await fetch("http://127.0.0.1:8080/add_question", {
          method: 'POST',
          headers: {
            "Content-Type": 'application/json',
            'Authorization': `Bearer ${localStorage.getItem('jwtToken')}`
          },
          body: JSON.stringify(this.new_question)
        });

        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }
        //alert("Question added successfully!");

        this.showToast = true;
        setTimeout(() => {
          this.showToast = false;
          this.$router.push("/quiz_management");
        }, 3000)

      }
      catch (error) {
        console.error("Error adding question:", error);
        alert("Failed to add question.");
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
    }
  }
};
</script>
<style>
.toast-container {
  position: fixed;
  bottom: 20px;
  right: 20px;
  background-color: #28a745;
  color: white;
  padding: 12px 20px;
  border-radius: 5px;
  box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
  animation: fadeOut 3s forwards;
}

@keyframes fadeOut {
  0% {
    opacity: 1;
  }

  70% {
    opacity: 1;
  }

  100% {
    opacity: 0;
  }
}
</style>