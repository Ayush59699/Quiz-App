<template>
  <div class="admin-dashboard">
    <!-- Navbar -->
    <AdminNavbar />

    <!-- Welcome Section -->
    <div class="container text-center my-3">
      <h2 class="fw-bold text-primary">Welcome, {{ admin_name }}</h2>
      <p class="text-muted">Effortlessly manage subjects, chapters, and quizzes.</p>
    </div>

    <!-- Add Subject Button -->
    <div class="container text-end mb-1">
      <router-link to="/create_subject" class="btn btn-lg btn-primary shadow-sm">
        + Add Subject
      </router-link>
    </div>

    <!-- Subjects Grid -->
    <div class="container" style="max-width: 1350px;">
      <div class="row">
        <div v-for="subject in subjects" :key="subject.id" class="col-md-6 col-lg-4">
          <div class="card shadow-lg subject-card">
            <!-- Subject Header -->
            <div class="card-header bg-primary text-white d-flex justify-content-between">
              <h5 class="mb-0">{{ subject.subject_name }}</h5>
              <div>
                <button class="btn btn-light btn-sm me-2" @click="openEditSubjectModal(subject)">
                  ✏️ Edit
                </button>
                <button class="btn btn-danger btn-sm" @click="deleteSubject(subject.id)">
                  🗑 Delete
                </button>
              </div>
            </div>

            <!-- Subject Description -->
            <div class="card-body">
              <p class="text-muted">{{ subject.subject_description }}</p>

              <!-- Chapters List -->
              <div class="chapters-list">
                <div v-for="chapter in subject.chapters" :key="chapter.id" class="chapter-card">
                  <div class="d-flex justify-content-between align-items-center">
                    <div>
                      <strong>{{ chapter.chapter_name }}</strong>
                      <p class="text-muted small">{{ chapter.chapter_description }}</p>
                    </div>
                    <div>
                      <button @click="editChapter(chapter)" class="btn btn-outline-success btn-sm me-2">✏️ Edit</button>
                      <button @click="deleteChapter(chapter.id)" class="btn btn-outline-danger btn-sm me-2">🗑</button>
                      <router-link :to="`/manage_chapter_quizzes/${chapter.id}`" class="btn btn-outline-info btn-sm">
                        📚 Quizzes
                      </router-link>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Add Chapter Button -->
            <div class="card-footer bg-light text-end">
              <router-link :to="`/create_chapter/${subject.id}`" class="btn btn-success btn-sm">
                + Add Chapter
              </router-link>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Edit Chapter Modal -->
    <div class="modal fade" :class="{ 'show d-block': editModalOpen }" tabindex="-1">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content">
          <div class="modal-header bg-primary text-white">
            <h5 class="modal-title">Edit Chapter</h5>
            <button type="button" class="btn-close" @click="editModalOpen = false"></button>
          </div>
          <div class="modal-body">
            <label>Chapter Name:</label>
            <input v-model="editChapterData.chapter_name" type="text" class="form-control mb-2" />

            <label>Chapter Description:</label>
            <textarea v-model="editChapterData.chapter_description" class="form-control mb-2"></textarea>
          </div>
          <div class="modal-footer">
            <button class="btn btn-secondary" @click="editModalOpen = false">Cancel</button>
            <button class="btn btn-primary" @click="updateChapter">Save Changes</button>
          </div>
        </div>
      </div>
    </div>

    <!-- Edit Subject Modal -->
    <div class="modal fade" :class="{ 'show d-block': editSubjectModalOpen }" tabindex="-1">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content">
          <div class="modal-header bg-primary text-white">
            <h5 class="modal-title">Edit Subject</h5>
            <button type="button" class="btn-close" @click="editSubjectModalOpen = false"></button>
          </div>
          <div class="modal-body">
            <label>Subject Name:</label>
            <input v-model="editSubjectData.subject_name" type="text" class="form-control mb-2" />

            <label>Subject Description:</label>
            <textarea v-model="editSubjectData.subject_description" class="form-control mb-2"></textarea>
          </div>
          <div class="modal-footer">
            <button class="btn btn-secondary" @click="editSubjectModalOpen = false">Cancel</button>
            <button class="btn btn-primary" @click="saveUpdatedSubject">Save Changes</button>
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

  name: 'AdminDashboard',
  data() {
    return {
      admin_name: '',
      users: [],
      subjects: [],
      subjectId: '',
      editModalOpen: false,
      editChapterData: {
        chapter_id: null,
        chapter_name: "",
        chapter_description: ""
      },
      editSubjectModalOpen: false,
      editSubjectData: {
        subject_id: null,
        subject_name: '',
        subject_description: ''
      }

    };
  },
  async mounted() {
    const admin_name = localStorage.getItem('admin_name') || 'admin'
    this.admin_name = admin_name
    this.fetch_data();


  },
  methods: {
    async deleteSubject(subid) {
      if (!subid) {
        console.error("Error: SUBJECT ID IS MISSING")
        return
      }
      const sure = confirm("Are you sure you want to DELETE this SUBJECT and all it's CHAPTERS??");
      if (!sure) {
        return;
      }
      try {
        const response = await fetch("http://127.0.0.1:8080/delete_subject", {
          method: 'DELETE',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${localStorage.getItem('jwtToken')}`,
          },
          body: JSON.stringify({ subject_id: subid })
        });
        const data = await response.json()
        if (!response.ok) throw new Error(data.message || "Failed to delete subject")

        console.log("Subject and it's Chapters deleted Suvvessfully!!")
        this.subjects = this.subjects.filter(subject => subject.id != subid)

      }

      catch (error) {
        console.log('Error while deleting subject', error)
      }
    },

    openEditSubjectModal(subject) {
      if (!subject) {
        console.error("Error: SUBJECT DATA IS MISSING");
        return;
      }

      this.editSubjectData = {
        subject_id: subject.id,
        subject_name: subject.subject_name,
        subject_description: subject.subject_description
      };
      this.editSubjectModalOpen = true;
    },

    async saveUpdatedSubject() {
      if (!this.editSubjectData.subject_id) {
        alert("Subject ID is missing!");
        return;
      }

      try {
        const response = await fetch("http://127.0.0.1:8080/update_subject", {
          method: "PUT",
          headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${localStorage.getItem("jwtToken")}`,
          },
          body: JSON.stringify(this.editSubjectData),
        });

        const result = await response.json();
        alert(result.message);

        if (response.ok) {
          // Update the UI with new subject details
          const subjectIndex = this.subjects.findIndex(subject => subject.id === this.editSubjectData.subject_id);

          if (subjectIndex !== -1) {
            this.subjects[subjectIndex].subject_name = this.editSubjectData.subject_name;
            this.subjects[subjectIndex].subject_description = this.editSubjectData.subject_description;
          }

          this.editSubjectModalOpen = false; // Close the modal
        }
      } catch (error) {
        console.error("Error updating subject:", error);
      }
    },

    goToCreateChapter(subjectId) {
      if (!subjectId) {
        console.error("Subject id is missssingggg..");
        return;
      }
      this.$router.push(`/create_chapter/${subjectId}`);
    },

    async fetch_data() {
      try {
        const response = await fetch("http://127.0.0.1:8080/admin_dashboard", {
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

    async editChapter(chapter) {

      if (!chapter) { alert("Chapter is missing"); return; }// MUST

      try {
        this.editChapterData = {
          chapter_id: chapter.id,
          chapter_name: chapter.chapter_name,
          chapter_description: chapter.chapter_description
        };
        this.editModalOpen = true

      } catch (error) {
        console.error("Error updating chapter:", error);
      }
    },

    async updateChapter() {
      if (!this.editChapterData.chapter_id) {
        alert("Chapter ID is missing!");
        return;
      }
      try {
        const response = await fetch("http://127.0.0.1:8080/update_chapter", {
          method: "PUT",
          headers: {
            "Content-Type": "application/json",
            'Authorization': `Bearer ${localStorage.getItem('jwtToken')}`,
          },
          body: JSON.stringify(this.editChapterData),
        });

        const result = await response.json();
        alert(result.message);

        if (response.ok) {
          // Update the UI with the new chapter details
          const subjectIndex = this.subjects.findIndex(subject =>
            subject.chapters.some(ch => ch.id === this.editChapterData.chapter_id)
          );

          if (subjectIndex !== -1) {
            const chapterIndex = this.subjects[subjectIndex].chapters.findIndex(ch => ch.id === this.editChapterData.chapter_id);

            if (chapterIndex !== -1) {
              this.subjects[subjectIndex].chapters[chapterIndex].chapter_name = this.editChapterData.chapter_name;
              this.subjects[subjectIndex].chapters[chapterIndex].chapter_description = this.editChapterData.chapter_description;
            }
          }

          this.editModalOpen = false; // Close the modal
        }
      } catch (error) {
        console.error("Error updating chapter:", error);
      }

    },

    async deleteChapter(chapterId) {

      if (!chapterId) { console.log("Error: CHAPTER ID IS MISSING"); return; }

      const isConfirmed = confirm("Are you sure you want to delete this chapter?");
      if (!isConfirmed) return;

      try {
        const response = await fetch('http://127.0.0.1:8080/delete_chapter', {
          method: 'DELETE',
          headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${localStorage.getItem("jwtToken")}`,
          },
          body: JSON.stringify({ chapter_id: chapterId }),
        });
        const data = await response.json();

        if (!response.ok) { throw new Error(data.message || "Failed to delete Chapter"); }
        console.log("Chapter deleted successfully!");
        //setTimeout(() => {location.reload();}, 2000);

        await this.fetch_data();

        this.subjects = this.subjects.map(subject => ({
          ...subject,
          chapters: subject.chapters.filter(chapter => chapter.id !== chapterId),
        }));

        this.$router.push("/admin_dashboard");


      }
      catch (error) {
        console.log('Error deleting chapter', error)
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
/* Main Dashboard Styling */
.admin-dashboard {
  background-color: #f8f9fa;
  min-height: 100vh;
  font-family: 'Poppins', sans-serif;
  padding-bottom: 2rem;
}

/* Navbar Enhancement */
.navbar {
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  background: linear-gradient(135deg, #4e73df 0%, #224abe 100%);
}

/* Welcome Section Styling */
.container.text-center.my-5 h2 {
  font-size: 2.5rem;
  background: linear-gradient(90deg, #4e73df, #36b9cc);
  background-clip: text;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  margin-bottom: 1rem;
}

.text-muted {
  color: #6c757d !important;
}

/* Add Subject Button Styling */
.btn-primary {
  background: linear-gradient(135deg, #4e73df 0%, #224abe 100%);
  border: none;
  transition: all 0.3s;
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(78, 115, 223, 0.4);
}

/* Subject Card Styling - MODIFIED FOR BETTER SPACING */
.subject-card {
  border-radius: 15px;
  overflow: hidden;
  transition: all 0.3s;
  margin-bottom: 2.5rem;
  border: none;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.08);
}

/* Adjust grid layout to show 2 cards per row */
.container .row .col-md-6 {
  flex: 0 0 50%;
  max-width: 90%;
  padding: 0 1.5rem;
}

/* Remove the lg-4 class effect to ensure 2 cards per row */
.container .row .col-lg-4 {
  flex: 0 0 50%;
  max-width: 50%;
}

.subject-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.15);
}

.card-header {
  border-bottom: none;
  padding: 1.5rem;
  background: linear-gradient(135deg, #4e73df 0%, #224abe 100%);
}

.card-header h5 {
  font-weight: 600;
  font-size: 1.2rem;
}

.card-body {
  padding: 1.75rem;
  min-height: 250px;
}


.chapters-list {
  margin-top: 1.75rem;
}

.chapter-card {
  padding: 1.25rem;
  border-radius: 10px;
  background-color: #f8f9fa;
  margin-bottom: 1.25rem;
  border-left: 4px solid #36b9cc;
  transition: all 0.2s;
}

.chapter-card:hover {
  background-color: #f1f3f5;
  transform: translateX(5px);
}

.chapter-card strong {
  font-size: 1.1rem;
  color: #3a3b45;
  display: block;
  margin-bottom: 0.5rem;
}

.chapter-card .text-muted {
  margin-top: 0.5rem;
  margin-bottom: 0.5rem;
  line-height: 1.4;
}

.chapter-card .d-flex {
  gap: 1rem;
}


.btn {
  border-radius: 50px;
  padding: 0.375rem 1.25rem;
  font-weight: 500;
  transition: all 0.2s;
}

.btn-sm {
  padding: 0.3rem 0.8rem;
  font-size: 0.8rem;
}

.btn-light {
  background-color: rgba(255, 255, 255, 0.2);
  border: none;
  color: white;
}

.btn-light:hover {
  background-color: rgba(255, 255, 255, 0.3);
  color: white;
}

.btn-danger,
.btn-outline-danger {
  background: linear-gradient(135deg, #e74a3b 0%, #c0392b 100%);
  border: none;
  color: white;
}

.btn-danger:hover,
.btn-outline-danger:hover {
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(231, 74, 59, 0.4);
}

.btn-success,
.btn-outline-success {
  background: linear-gradient(135deg, #1cc88a 0%, #13855c 100%);
  border: none;
  color: white;
}

.btn-success:hover,
.btn-outline-success:hover {
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(28, 200, 138, 0.4);
}



/* Chapter Button Container */
.chapter-card .d-flex div:last-child {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  align-items: center;
}

/* Card Footer Styling */
.card-footer {
  border-top: 1px solid rgba(0, 0, 0, 0.05);
  background-color: #ffffff;
  padding: 1.25rem 1.75rem;
}



textarea.form-control {
  min-height: 100px;
}

/* Add some animations */
@keyframes fadeIn {
  from {
    opacity: 0;
  }

  to {
    opacity: 1;
  }
}

.fade-in {
  animation: fadeIn 0.5s ease-in-out;
}



@media (max-width: 768px) {
  .card-header {
    flex-direction: column;
    align-items: start;
  }

}
</style>