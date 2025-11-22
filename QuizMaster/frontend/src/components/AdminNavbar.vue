<template>
    <div>

        <nav class="navbar navbar-expand-lg  navbar-dark bg-dark">
            <div class="container-fluid">
                <a class="navbar-brand" href="/admin_dashboard">Quizzy</a>
                <button class="navbar-toggler" type="button" data-bs-toggle="collapse"
                    data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent"
                    aria-expanded="false" aria-label="Toggle navigation">
                    <span class="navbar-toggler-icon"></span>
                </button>
                <div class="collapse navbar-collapse" id="navbarSupportedContent">
                    <ul class="navbar-nav me-auto mb-2 mb-lg-0">
                        <li class="nav-item"><a href="/admin_dashboard" class="nav-link active"
                                aria-current="page">Home</a> </li>

                        <li class="nav-item">
                            <router-link to="/quiz_management" class="nav-link active">Quiz Management</router-link>

                        </li>

                        <li class="nav-item">
                            <router-link to="/admin_summary" class="nav-link active"> Summary</router-link>
                        </li>

                        <li class="nav-item">
                            <router-link to="/admin_export" class="nav-link active"> Export Data</router-link>
                        </li>


                        <li class="nav-item">
                            <a class="nav-link " @click="logout">Logout</a>
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
    </div>
</template>
<script>
export default {
    name: 'AdminNavbar',
    data() {
        return {
            searchText: ''
        }
    },

    methods: {
        search() {
            if (this.searchText.trim() !== '') {
                this.$router.push(`/admin_search/${this.searchText.trim()}`);
            }
        },


        logout() {
            localStorage.removeItem('jwtToken');
            localStorage.removeItem('admin_name');
            this.$router.push('/');
        }
    }
}</script>