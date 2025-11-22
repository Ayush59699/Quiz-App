<template>
    <div>
        <IndexNavbar />

        <!-- Hero Section -->
        <div class="hero-section text-center text-dark">
            <h1 class="fw-bold">Welcome to Quizzy!</h1>
            <p class="fs-5 text-dark-50">The ultimate platform to test your knowledge and compete with others!</p>

            <div class="container mt-3">
                <div class="row justify-content-center">
                    <div class="col-md-8">
                        <p class="fs-6 text-secondary">
                            ⏳ Timed quizzes to test your speed and accuracy.<br>
                            🏆 Compete on leaderboards and challenge your friends.<br>
                            📊 Track your progress and improve over time.<br>
                            🌟 Take quizzes on a wide range of subjects, from all subjects.<br>

                        </p>
                    </div>
                </div>
            </div>

            <router-link to="/user_register">
                <button class="btn btn-success btn-lg mt-3">Start Now</button>
            </router-link>
        </div>

        <!-- Login Section -->
        <div class="container text-center my-4">
            <h3 class="fw-bold">Already Registered?</h3>
            <p class="text-secondary">Login to continue</p>
            <router-link to="/admin_login">
                <button class="btn btn-info m-2">Admin Login</button>
            </router-link>
            <router-link to="/user_login">
                <button class="btn btn-info m-2">User Login</button>
            </router-link>
        </div>

        <!-- Features Section -->
        <div class="container my-5">
            <h2 class="text-center fw-bold mb-3">Why Choose Quizzy?</h2>
            <div class="row text-center">
                <div class="col-md-4">
                    <div class="card feature-card">
                        <h5><i class="bi bi-star-fill text-warning"></i> Wide Range of Quizzes</h5>
                        <p>Explore various topics and challenge yourself.</p>
                    </div>
                </div>
                <div class="col-md-4">
                    <div class="card feature-card">
                        <h5><i class="bi bi-people-fill text-primary"></i> Leaderboards</h5>
                        <p>Compete with friends and rise to the top.</p>
                    </div>
                </div>
                <div class="col-md-4">
                    <div class="card feature-card">
                        <h5><i class="bi bi-clock-fill text-danger"></i> Timed Quizzes</h5>
                        <p>Test your speed and accuracy under pressure.</p>
                    </div>
                </div>
            </div>
        </div>

        <Contact />

        <!-- Footer -->
        <footer class="bg-dark text-white text-center py-3">
            <p class="mb-0">&copy; 2023 Quizzy. All rights reserved.</p>
        </footer>
    </div>
</template>

<script>
import IndexNavbar from '../components/IndexNavbar.vue';
import Contact from '@/components/Contact.vue';

export default {
    components: { IndexNavbar, Contact },
    name: 'Home'
};
</script>

<style scoped>
/* Hero Section - Tight, No Weird Gaps */
.hero-section {
    padding: 50px 20px;
    height: 410px;
    background: linear-gradient(135deg, #e4e4e4, #f6f6f6);
}

/* Feature Cards */
.feature-card {
    border-color: rgb(57, 188, 79);
    padding: 20px;
    border-radius: 10px;
    background: #f8f9fa;
    transition: transform 0.2s;
}

.feature-card:hover {
    transform: scale(1.05);
}
</style>
