<template>
    <div>
        <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
            <div class="container-fluid">
                <a class="navbar-brand" href="#">Quizzy</a>
                <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav"
                    aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
                    <span class="navbar-toggler-icon"></span>
                </button>
                <div class="collapse navbar-collapse" id="navbarNav">
                    <ul class="navbar-nav ms-auto">
                        <li class="nav-item">
                            <router-link to="/" class="nav-link active"> Home</router-link>
                        </li>
                    </ul>
                </div>
            </div>
        </nav>

        <div class="container mt-5" style="background: linear-gradient(135deg, #e4e4e4, #f6f6f6);">
            <h2 class="text-center mb-4">User Registration</h2>

            <div v-if="error" class="alert alert-danger">{{ error }}</div>
            <div v-if="successMessage" class="alert alert-success">{{ successMessage }}</div>

            <form @submit.prevent="registerUser">
                <div class="mb-3">
                    <label for="name" class="form-label">Full Name</label>
                    <input type="text" class="form-control" id="name" v-model="user_name" required>
                </div>

                <div class="mb-3">
                    <label for="email" class="form-label">Email address</label>
                    <input type="email" class="form-control" id="email" v-model="user_email" required>
                </div>

                <div class="mb-3">
                    <label for="password" class="form-label">Password</label>
                    <input type="password" class="form-control" id="password" v-model="user_password" required>
                </div>

                <div class="mb-3">
                    <label for="qualification" class="form-label">Qualification</label>
                    <input type="text" class="form-control" id="qualification" v-model="user_qualification" required>
                </div>

                <div class="mb-3">
                    <label for="dob" class="form-label">Date of Birth</label>
                    <input type="date" class="form-control" id="dob" v-model="user_dob" required>
                </div>

                <button type="submit" class="btn btn-success w-100">Register</button>
            </form>

            <p class="text-center mt-3">
                Already have an account? <router-link to="/user_login">Login here</router-link>
            </p>
        </div>
    </div>


</template>

<script>
export default {
    data() {
        return {
            user_name: "",
            user_email: "",
            user_password: "",
            user_qualification: "",
            user_dob: "",
            error: null,
            successMessage: null
        };
    },
    methods: {
        async registerUser() {
            this.error = null;
            this.successMessage = null;

            try {
                const response = await fetch("http://127.0.0.1:8080/user_register", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({
                        user_name: this.user_name,
                        user_email: this.user_email,
                        user_password: this.user_password,
                        user_qualification: this.user_qualification,
                        user_dob: this.user_dob
                    })
                });

                const data = await response.json();

                if (!response.ok) {
                    throw new Error(data.message || "Failed to register.");
                }

                this.successMessage = "Registration successful! Redirecting to login...";
                setTimeout(() => this.$router.push("/user_login"), 2000);
            } catch (error) {
                this.error = error.message;
            }
        }
    }
};
</script>

<style scoped>
.container {
    max-width: 500px;
}
</style>
