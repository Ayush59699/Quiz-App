<template>
    <div>
        <div class="sidebar">
            <ul>
                <li @click="selectSection('overview')" :class="{ active: selectedSection === 'overview' }">Profile
                    Overview
                </li>
                <li @click="selectSection('performance')" :class="{ active: selectedSection === 'performance' }">Quiz
                    Performance</li>
                <li @click="selectSection('settings')" :class="{ active: selectedSection === 'settings' }">Settings</li>
                <li @click="selectSection('downloads')" :class="{ active: selectedSection === 'downloads' }">DOWNLOAD
                    REPORTS</li>

                <li @click="logout" class="logout">Logout</li>
            </ul>
        </div>

        <button class="btn btn-primary" type="button" data-bs-toggle="offcanvas" data-bs-target="#offcanvasRight"
            aria-controls="offcanvasRight">Toggle right offcanvas</button>

        <div class="offcanvas offcanvas-end" tabindex="-1" id="offcanvasRight" aria-labelledby="offcanvasRightLabel">
            <div class="offcanvas-header">
                <h5 class="offcanvas-title" id="offcanvasRightLabel">Offcanvas right</h5>
                <button type="button" class="btn-close" data-bs-dismiss="offcanvas" aria-label="Close"></button>
            </div>
            <div class="offcanvas-body">
                ...
            </div>
        </div>
    </div>









</template>

<script>
export default {
    props: ['selectedSection'],
    methods: {
        selectSection(section) {
            this.$emit('update-section', section);
        },
        logout() {
            localStorage.removeItem('jwtToken');
            this.$router.push('/');
        }
    }
}
</script>

<style scoped>
.sidebar {
    width: 250px;
    height: 100vh;
    background: #2c4b6b;
    color: white;
    padding: 20px;
    position: fixed;
}

ul {
    list-style: none;
    padding: 0;
}

li {
    padding: 15px;
    cursor: pointer;
    border-radius: 5px;
}

li:hover,
.active {
    background: #1abc9c;
}

.logout {
    margin-top: 20px;
    color: red;
}
</style>