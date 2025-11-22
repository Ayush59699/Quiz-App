<template>
    <div>
        <UserNavbar />

        <div class="profile-container">

            <UserProfileSidebar class="sidebar" :selectedSection="selectedSection"
                @update-section="selectedSection = $event" />


            <div class="content">
                <div v-if="selectedSection === 'overview'">
                    <h3>👤Welcome, this is {{ profile.user_name }}'s Profile</h3>
                    <h3>Profile Overview</h3><br>
                    <p>📝 <strong>Name:</strong> {{ profile.user_name }}</p>
                    <p>📧 <strong>Email:</strong> {{ profile.user_email }}</p>
                    <p>🎓 <strong>Qualification:</strong> {{ profile.user_qualification }}</p>
                    <p>🎂 <strong>Date of Birth:</strong> {{ profile.user_dob }}</p>
                    <button @click="editModalOpen = true" class="btn btn-primary">Update Profile</button>
                </div>

                <div v-if="selectedSection === 'performance'">
                    <h3>📊 Quiz Performance</h3><br>
                    <p>📝 <b>Total Quizzes Attempted:</b> {{ totalQuizzes }}</p>
                    <p>⭐ <b>Average Score:</b> {{ averageScore }}</p>
                </div>


                <div v-if="selectedSection === 'downloads'">
                    <h3>📊 Get CSV formatted report.</h3><br>
                    <button @click="exportCSV" class="btn btn-primary">Export Quiz Data</button>
                    <br>
                    <div v-if="download_link">
                        <p>✅ Your export is ready! If it didn't download on itself, Click below to download:</p>
                        <a :href="download_link" class="btn btn-success" target="_blank" download>Download CSV</a>
                    </div>

                    <div>
                        <h3>You can also download PDF report from below:</h3>
                        <button @click="downloadReport" class="bg-dark text-white px-4 py-2 rounded">
                            Download Monthly Report
                        </button>
                    </div>

                </div>


                <div v-if="selectedSection === 'settings'">
                    <h3>⚙️ Settings</h3><br>
                    <label>Click here to change your password. </label><br>
                    <button @click="passwordModalOpen = true" class="btn btn-warning">🔑 Change
                        Password</button><br><br>
                    <label>Click here to change your Daily Reminder Time. </label><br>
                    <button @click="reminderModalOpen = true" class="btn btn-success">⏰ Set Reminder Time</button>
                </div>
            </div>
        </div>

        <!-- Update Profile Modal -->
        <div class="modal fade" :class="{ 'show d-block': editModalOpen }" tabindex="-1">
            <div class="modal-dialog modal-dialog-centered">
                <div class="modal-content shadow-lg border-0 rounded-3">
                    <div class="modal-header bg-primary text-white">
                        <h5 class="modal-title">Edit Profile</h5>
                        <button type="button" class="btn-close" @click="editModalOpen = false"></button>
                    </div>
                    <div class="modal-body p-4">
                        <form>
                            <div class="mb-3">
                                <label class="form-label fw-bold">Email:</label>
                                <input v-model="profile.user_email" disabled type="text"
                                    class="form-control bg-light border-0" />
                            </div>
                            <div class="mb-3">
                                <label class="form-label fw-bold">Name:</label>
                                <input v-model="profile.user_name" type="text" class="form-control"
                                    placeholder="Enter your name" />
                            </div>
                            <div class="mb-3">
                                <label class="form-label fw-bold">Qualification:</label>
                                <input type="text" v-model="profile.user_qualification" class="form-control"
                                    placeholder="Enter qualification" />
                            </div>
                            <div class="mb-3">
                                <label class="form-label fw-bold">Date of Birth:</label>
                                <input type="date" v-model="profile.user_dob" class="form-control" />
                            </div>
                        </form>
                    </div>
                    <div class="modal-footer bg-light border-0">
                        <button class="btn btn-secondary px-4" @click="editModalOpen = false">Cancel</button>
                        <button class="btn btn-primary px-4" @click="updateProfile">Save Changes</button>
                    </div>
                </div>
            </div>
        </div>


        <!-- Change Password Modal -->
        <div class="modal fade" :class="{ 'show d-block': passwordModalOpen }" tabindex="-1">
            <div class="modal-dialog modal-dialog-centered">
                <div class="modal-content shadow-lg border-0 rounded-3">
                    <div class="modal-header bg-danger text-white">
                        <h5 class="modal-title">🔑 Change Password</h5>
                        <button type="button" class="btn-close" @click="passwordModalOpen = false"></button>
                    </div>
                    <div class="modal-body">
                        <label class="form-label">New Password:</label>
                        <input type="password" v-model="newPassword" class="form-control" />

                        <label class="form-label mt-2">Confirm Password:</label>
                        <input type="password" v-model="confirmPassword" class="form-control" />
                    </div>
                    <div class="modal-footer">
                        <button class="btn btn-secondary" @click="passwordModalOpen = false">Cancel</button>
                        <button class="btn btn-danger" @click="changePassword">Update Password</button>
                    </div>
                </div>
            </div>
        </div>

        <!-- Set Reminder Modal -->
        <div class="modal fade" :class="{ 'show d-block': reminderModalOpen }" tabindex="-1">
            <div class="modal-dialog modal-dialog-centered">
                <div class="modal-content shadow-lg border-0 rounded-3">
                    <div class="modal-header bg-success text-white">
                        <h5 class="modal-title">⏰ Set Reminder</h5>
                        <button type="button" class="btn-close" @click="reminderModalOpen = false"></button>
                    </div>
                    <div class="modal-body">
                        <label class="form-label">Reminder Time:</label>
                        <input type="time" v-model="reminderTime" class="form-control" />
                    </div>
                    <div class="modal-footer">
                        <button class="btn btn-secondary" @click="reminderModalOpen = false">Cancel</button>
                        <button @click="setReminder" class="btn btn-success">⏰ Set Reminder Time</button>

                    </div>
                </div>
            </div>
        </div>


    </div>
</template>



<script>
import UserNavbar from '@/components/UserNavbar.vue'
import UserProfileSidebar from '@/components/UserProfileSidebar.vue'

export default {
    components: {
        UserNavbar,
        UserProfileSidebar,

    },
    name: "UserProfile",
    data() {
        return {
            profile: {
                user_id: '',
                user_name: '',
                user_email: '',
                user_qualification: '',
                user_dob: '',
                last_visited_time: ''
            },

            editModalOpen: false,
            passwordModalOpen: false,
            reminderModalOpen: false,

            selectedSection: 'overview',
            scores: [],
            averageScore: 0,
            totalQuizzes: 0,
            newPassword: '',
            confirmPassword: '',
            reminderTime: "",
            download_link: '',


        }
    },
    mounted() {
        this.fetchProfile()
        this.fetchScores()
    },
    methods: {

        async downloadReport() {
            const userId = this.profile.user_id
            console.log("User ID (Without dashes):", userId);
            window.location.href = `http://127.0.0.1:8080/download_report/${userId}`;
        },

        async fetchProfile() {
            try {
                const response = await fetch("http://127.0.0.1:8080/get_user_profile_details", {
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${localStorage.getItem('jwtToken')}`
                    }
                })

                const data = await response.json()
                if (!response.ok) {
                    throw new Error('error', response.status)
                }
                this.profile = data
                console.log("RECEIVED USER PROFILE DATA:", data)
            }
            catch (error) {
                console.log("Error", error)
            }

        },

        async updateProfile() {
            if (!this.profile.user_name) {
                alert("USER ID & NAME IS MISSING")
                return
            }

            try {
                const response = await fetch("http://127.0.0.1:8080/get_user_profile_details", {
                    method: 'PUT',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${localStorage.getItem('jwtToken')}`
                    },
                    body: JSON.stringify(this.profile)
                })
                const result = await response.json()
                if (!response.ok) {
                    const errorData = await response.json();
                    console.error("Error updating profile:", errorData);
                    alert("❌ Failed to update profile: " + errorData.message);
                    return;
                } else {
                    console.log('Profile Updates Successfully')
                    alert('Profile Updates Successfully')
                    this.editModalOpen = false
                }
            }
            catch (error) {
                console.log('Got error:', error)
            }
        },

        async fetchScores() {
            try {
                const response = await fetch('http://127.0.0.1:8080/user/scores', {
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${localStorage.getItem('jwtToken')}`
                    }
                })
                const data = await response.json()
                console.log(data)
                if (response.ok) {
                    this.scores = data;
                    this.totalQuizzes = data.length;

                    if (this.totalQuizzes > 0) {
                        const totalScore = data.reduce((sum, score) => sum + score.total_score, 0);
                        this.averageScore = (totalScore / this.totalQuizzes).toFixed(2); // 2 decimal places
                    }
                } else {
                    console.error("Error fetching scores:", data.error);
                }
            }
            catch (error) {
                console.log('Error', error)
            }
        },

        async changePassword() {
            if (this.newPassword !== this.confirmPassword) {
                alert('Passwords dont match.')
                return
            }
            try {
                const response = await fetch("http://127.0.0.1:8080/user/change_password", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        "Authorization": `Bearer ${localStorage.getItem('jwtToken')}`
                    },
                    body: JSON.stringify({ new_password: this.newPassword }),
                });

                const data = await response.json();
                if (response.ok) {
                    alert("✅ Password updated successfully!");
                    this.passwordModalOpen = false;
                } else {
                    alert("❌ " + data.error);
                }
            } catch (error) {
                console.error("Error changing password:", error);
            }
        },

        async setReminder() {
            if (!this.reminderTime) {
                alert("❌ Reminder time is required bhisu");
                return;
            }
            console.log("Setting reminder for:", this.reminderTime);

            try {
                const response = await fetch("http://127.0.0.1:8080/user/set_reminder", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        "Authorization": `Bearer ${localStorage.getItem('jwtToken')}`
                    },
                    body: JSON.stringify({ reminder_time: this.reminderTime }),
                });
                const data = await response.json();

                if (response.ok) {
                    alert("✅ Reminder set for " + this.reminderTime);
                    this.reminderModalOpen = false;
                } else {
                    alert("❌ pata nahi kya horha " + data.error);
                }
            } catch (error) {
                console.error("Error setting reminder:", error);
            }
        },

        async exportCSV() {
            try {
                const response = await fetch('http://127.0.0.1:8080/export_quiz_csv', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${localStorage.getItem('jwtToken')}`
                    },
                })
                const data = await response.json()
                if (!response.ok) {
                    throw new Error("Failed to generate csv bro!")
                }
                const jobId = data.job_id
                console.log("Export job started, JOB ID IS :", jobId) // logs job id of async batch job
                console.log(data)

                const checkStatus = async () => {
                    try {
                        const statusResponse = await fetch(`http://127.0.0.1:8080/export_status/${jobId}`, {
                            method: 'GET',
                            headers: {
                                'Content-Type': 'application/json',
                                'authorization': `Bearer ${localStorage.getItem('jwtToken')}`
                            }
                        })
                        if (!statusResponse.ok) {
                            throw new Error("Failed to fetch job status")
                        }
                        const statusData = await statusResponse.json()
                        this.download_link = statusData.csv_url
                        console.log(statusData.csv_url)

                        console.log('Job Status hai :', statusData.status)


                        if (statusData.status === 'completed') {
                            clearInterval(interval)
                            console.log('Download URL:', statusData.csv_url)
                            alert('The download is ready. Click OK.')
                            window.location.href = statusData.csv_url // download CSV once READY
                        }

                        else if (statusData.status == 'failed') {
                            clearInterval(interval)
                            console.log('Export Job Failed bro.')
                            alert("CSV Export Failed! Please Try again later")
                        }

                    } catch (err) {
                        clearInterval(interval) // Stop checking on error
                        console.error("Error checking job status:", err)
                        alert("Error checking export status. Please refresh and try again.")

                    }

                }
                const interval = setInterval(checkStatus, 3000);
                setTimeout(() => {  // ✅ Auto-stop after 30s if no success
                    clearInterval(interval)
                    console.error("10 seconds passed, stopping polling.")
                }, 30000)


            }
            catch (error) {
                console.error("GETTING THIS ERROR", error)
                alert("Error exporting CSV. Please try again.")
            }
        }

    }
}




</script>
<style>
.profile-container {
    display: flex;
    min-height: 100vh;
    /* Full-page height */
    padding-top: 60px;
}

.sidebar {
    width: 250px;
    background-color: #f8f9fa;
    padding: 20px;
    height: calc(100vh - var(--navbar-height, 60px));

    position: fixed;
    left: 0;
    top: var(--navbar-height, 60px);
    transition: top 0.3s ease-in-out;
    overflow-y: auto;
}

.content {
    flex-grow: 1;
    margin-left: 260px;
    /* Adjust based on sidebar width */
    padding: 20px;
    width: calc(100% - 260px);
}

.modal-content {
    border-radius: 10px;
}

.btn {
    border-radius: 5px;
}
</style>