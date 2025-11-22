<template>
    <div>
        <AdminNavbar />

        <div class="container py-4">
        <div class="col-md-6 mx-auto card border shadow">
            <div class="card-header bg-success text-white">
                <h4 class="mb-0">Create Chapter</h4>
            </div>
            <div class="card-body">
                <form @submit.prevent="createChapter">
                    <div class="mb-3">
                        <label for="chapter_name" class="form-label">Chapter Name:</label>
                        <input v-model="chapter_name" type="text" id="chapter_name" class="form-control" required />
                    </div>

                    <div class="mb-3">
                        <label for="chapter_description" class="form-label">Chapter Description:</label>
                        <textarea v-model="chapter_description" id="chapter_description" class="form-control" rows="3" required></textarea>
                    </div>

                    <button type="submit" class="btn btn-success w-100">+ Create Chapter</button>
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

    name: 'CreateChapter',
    data() {
        return {
            admin_name: '',
            chapter_name: '',
            chapter_description: '',
            subject_id: '',
            users: [],
            subjects: [],
        };
    },
    async mounted() {
        const admin_name = localStorage.getItem('admin_name') || 'admin'
        this.admin_name = admin_name

        this.subject_id = this.$route.params.subjectId;
        console.log('Subject ID:', this.subject_id);

    },
    methods: {

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


        async createChapter() {
            try {
                const response = await fetch("http://127.0.0.1:8080/create_chapter", {
                    method: "POST",
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${localStorage.getItem('jwtToken')}`,
                    },
                    body: JSON.stringify({
                        chapter_name: this.chapter_name,
                        chapter_description: this.chapter_description,
                        subject_id: this.subject_id

                    })
                });

                const data = await response.json()

                if (!response.ok) { throw new Error(`HTTP error! Status: ${response.status}`); }
                alert(data.message)

                await this.fetch_data()

                if (response.status === 201) {
                    this.$router.push('/admin_dashboard')
                }

            }
            catch (error) {
                console.log("Error Creating Chapter:", error.message);
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