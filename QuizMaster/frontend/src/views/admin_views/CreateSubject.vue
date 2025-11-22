<template>
    <div>
        <AdminNavbar />

        <div class="container py-4">
        <div class="col-md-6 mx-auto card border shadow">
            <div class="card-header bg-primary text-white">
                <h4 class="mb-0">Create Subject</h4>
            </div>
            <div class="card-body">
                <form @submit.prevent="create_subject">
                    <div class="mb-3">
                        <label for="subject_name" class="form-label">Subject Name:</label>
                        <input v-model="subject_name" type="text" id="subject_name" class="form-control" required />
                    </div>

                    <div class="mb-3">
                        <label for="subject_description" class="form-label">Subject Description:</label>
                        <textarea v-model="subject_description" id="subject_description" class="form-control" rows="3" required></textarea>
                    </div>

                    <button type="submit" class="btn btn-primary w-100">+ Create Subject</button>
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
    name: 'CreateSubject',
    data() {
        return {
            admin_name: '',
            subject_name: '',
            subject_description: '',
        };
    },
    async mounted() {
        const admin_name = localStorage.getItem('admin_name') || 'admin'
        this.admin_name = admin_name

    },
    methods: {
        async create_subject() {
            try {
                const response = await fetch("http://127.0.0.1:8080/create_subject", {
                    method: "POST",
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${localStorage.getItem('jwtToken')}`,
                    },
                    body: JSON.stringify({
                        subject_name: this.subject_name,
                        subject_description: this.subject_description

                    })
                });

                if (!response.ok) {
                    throw new Error(`HTTP error! Status: ${response.status}`);
                }

                const data = await response.json()
                alert(data.message)

                if (response.status === 201) {
                    this.$router.push('/admin_dashboard')
                }
            }
            catch (error) {
                console.log("Some error:", error);
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