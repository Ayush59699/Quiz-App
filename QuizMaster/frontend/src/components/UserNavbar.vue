<template>
    <nav class="navbar navbar-expand-lg bg-dark navbar-dark">
        <div class="container-fluid">
            <a class="navbar-brand" href="/user_dashboard">Quizzy</a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse"
                data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false"
                aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarSupportedContent">
                <ul class="navbar-nav me-auto mb-2 mb-lg-0">
                    <li class="nav-item">
                        <router-link to="/user_dashboard" class="nav-link active">Home</router-link>
                    </li>
                    <li class="nav-item">
                        <router-link to="/user_attempts" class="nav-link active">My Attempts </router-link>
                    </li>
                    <li class="nav-item">
                        <router-link to="/user_summary" class="nav-link active">Summary</router-link>
                    </li>

                    <li class="nav-item">
                        <router-link to="/get_user_profile_details" class="nav-link active">User Profile</router-link>
                    </li>
                    <li class="nav-item">
                        <router-link to="/user_leaderboard" class="nav-link active">LeaderBoard</router-link>
                    </li>

                    <li class="nav-item">
                        <router-link to="/generate_ai_content" class="nav-link active">Ai Agent </router-link>
                    </li>


                    <li class="nav-item">
                        <a class="nav-link" @click="logout" href="#">Logout</a>
                    </li>
                </ul>
                <form class="d-flex" @submit.prevent="search">
                    <input v-model="searchText" class="form-control me-2" type="search"
                        placeholder="Search (User, Subject, Quiz)" aria-label="Search">
                    <button class="btn btn-outline-success" type="submit">Search</button>
                </form>
            </div>
        </div>
    </nav>
</template>

<script>
export default {
    name: 'Navbar',
    data() {
        return {
            searchText: '',
        }
    },
    methods: {
        search() {
            if (this.searchText.trim() !== '') {
                this.$router.push(`/user_search/${this.searchText.trim()}`);
            }
        }
        ,
        async logout() {
            localStorage.removeItem('jwtToken');
            localStorage.removeItem('user_name');
            localStorage.removeItem('user_email');
            this.$router.push('/');
        }
    }
};
</script>

<style scoped>
.navbar {
    box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
}
</style>
