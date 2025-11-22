<template>
    <div>
        <AdminNavbar />
        <div class="container mt-5">

            <div class="text-center mb-4">
                <h3 class="fw-bold text-primary">🔍 Search Results for "{{ query }}"</h3>
            </div>

            <!-- Loading Indicator -->
            <div v-if="loading" class="text-center">
                <div class="spinner-border text-primary" role="status">
                    <span class="visually-hidden">Loading...</span>
                </div>
            </div>

            <div v-else>
                <div v-if="results.length > 0">
                    <ul class="list-group">
                        <li v-for="(item, index) in results" :key="index"
                            class="list-group-item shadow-sm rounded mb-2 d-flex justify-content-between align-items-center">
                            <span class="fw-semibold">{{ item.name }}</span>
                            <span class="badge bg-secondary text-uppercase">{{ item.type }}</span>
                        </li>
                    </ul>
                </div>

                <div v-else class="text-center">
                    <p class="text-danger fs-5">❌ No results found.</p>
                </div>

                <div class="text-center mt-4">
                    <router-link to="/admin_dashboard" class="btn btn-outline-primary px-4 py-2 fw-bold">
                        ⬅ Back to Dashboard
                    </router-link>
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

    name: 'SearchResults',
    data() {
        return {
            results: [],
            loading: true,
            query: ''
        };
    },
    async mounted() {
        this.query = this.$route.params.query;
        await this.fetchResults();
    },
    watch: {
        '$route.params.query': 'fetchResults'
    },
    methods: {
        async fetchResults() {
            this.loading = true;
            try {
                const response = await fetch(`http://127.0.0.1:8080/admin_search/${this.query}`, {
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${localStorage.getItem('jwtToken')}`
                    }
                });
                if (!response.ok) {
                    throw new Error(`HTTP error! Status ${response.status}`);
                }
                const data = await response.json();
                console.log("Fetched data:", data)

                this.results = data;


            } catch (error) {
                console.error('Error fetching search results:', error);
                this.results = [];
            } finally {
                this.loading = false;
            }
        }
    }
};
</script>
<style scoped>
.list-group-item {
    transition: all 0.1s ease-in-out;
    background: #f8f9fa;
    border: 1px solid #ddd;
}

.list-group-item:hover {
    transform: scale(1.02);
    background: #eef5ff;
}

h3 {
    text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.1);
}

.btn-outline-primary:hover {
    background: #0d6efd;
    color: white;
}
</style>