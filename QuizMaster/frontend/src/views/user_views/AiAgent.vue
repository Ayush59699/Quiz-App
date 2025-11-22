<template>
    <div class="user-summary">
        <UserNavbar />

        <div class="container" style="max-width: 1350px;">
            <h2 class="page-title text-center">📊 AI Search Page</h2>

            <div class="p-4">
                <h2 class="text-2xl font-bold mb-4">AI Content Generator</h2>

                <input v-model="topic" type="text" placeholder="Enter a topic..."
                    class="border p-2 rounded w-full mb-2" />

                <button @click="fetchAIContent" class="bg-dark text-white px-4 py-2 rounded" :disabled="loading">
                    {{ loading ? "Generating..." : "Generate AI Content" }}
                </button>

                <div v-if="aiResponse" class="mt-4 p-4 border rounded bg-gray-100">
                    <h3 class="text-xl font-semibold">AI Generated Content:</h3>
                    <p class="mt-2">{{ aiResponse }}</p>
                </div>

                <div v-if="error" class="text-red-500 mt-2">{{ error }}</div>
            </div>

            <div class="back-btn-container text-center mt-4">
                <router-link to="/user_dashboard" class="btn btn-primary">⬅ Back to Dashboard</router-link>
            </div>

        </div>
    </div>
</template>


<script>
import UserNavbar from '@/components/UserNavbar.vue'

export default {
    name: 'AiAgent',
    components: {
        UserNavbar,

    },
    data() {
        return {
            topic: '',
            aiResponse: null,
            loading: false,
            error: null,

        }
    },
    mounted() {

    },

    methods: {
        async fetchAIContent() {
            if (!this.topic) {
                this.error = 'Please enter a topic first.'
                return;
            }

            this.error = null
            this.loading = true
            this.aiResponse = null

            try {
                const response = await fetch('http://127.0.0.1:8080/generate_ai_content', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${localStorage.getItem('jwtToken')}`
                    },
                    body: JSON.stringify({ topic: this.topic })
                })
                if (!response.ok) {
                    throw new Error("Failed to fetch AI Content bro")
                }
                const data = await response.json()
                this.aiResponse = data.content
            }
            catch (error) {
                console.log("Getting this error bro", error)
            }
            finally {
                this.loading = false
            }












        }

    }
}

</script>
