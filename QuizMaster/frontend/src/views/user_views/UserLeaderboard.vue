<template>
    <div>
        <UserNavbar />
        <div class="container mt-4">

            <div class="card shadow p-4">
                <h2 class="text-center mb-4">🏆Leaderboard </h2>


                <div v-if="leaderboard.length">
                    <table class="table table-striped table-hover">
                        <thead class="table-dark">
                            <tr>
                                <th>Rank</th>
                                <th>User Name</th>
                                <th>Total Score</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="(entry, index) in leaderboard" :key="index"
                                :class="{ 'table-warning': entry.user_name === loggedInUser }">
                                <td>{{ index + 1 }}</td>
                                <td>{{ entry.user_name }}</td>
                                <td>{{ entry.total_score }} pts</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
                <div v-else class="alert alert-info text-center">
                    No leaderboard data available.
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import UserNavbar from '@/components/UserNavbar.vue';

export default {
    name: 'UserLeaderboard',
    components: { UserNavbar },
    data() {
        return {
            leaderboard: [],
            loggedInUser: localStorage.getItem('user_name')

        };
    },
    async created() {
        try {
            const leaderboardRes = await fetch('http://127.0.0.1:8080/user_leaderboard', {
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${localStorage.getItem('jwtToken')}`
                }
            });

            if (leaderboardRes.ok) {
                const data = await leaderboardRes.json();
                console.log(data)
                this.leaderboard = data.leaderboard;
            } else {
                console.error("Failed to fetch leaderboard.");
            }
        } catch (error) {
            console.log('Error fetching leaderboard:', error);
        }
    }
};
</script>

<style scoped>
.card {
    max-width: 600px;
    margin: auto;
}
</style>