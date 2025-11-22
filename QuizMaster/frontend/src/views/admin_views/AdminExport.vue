<template>
    <div>
        <AdminNavbar />
        <div class="container mt-4"><br><br><br>
            <button @click="exportQuizCSV" class="btn-lg btn btn-primary">Export User Data</button>

            <div v-if="exportStatus === 'pending'" class="mt-2 text-warning">Exporting... Please wait</div>
            <br><br>
            <div v-if="exportStatus === 'completed'" class="mt-2">
                <p class="text-dark">You can also download from this link below:</p>
                <a :href="csvUrl" class="text-success text-decoration-underline" download>Download
                    CSV</a>
            </div>

            <br><br>
            <div v-if="exportStatus === 'failed'" class="mt-2 text-danger">Export Failed. Try again.</div>
            <div class="mt-6 p-4 bg-gray-50 rounded-lg">
                <h4 class="font-semibold text-gray-800">💡 How It Works</h4>
                <p class="text-sm text-gray-600">
                    - Click "Export Data" to generate a CSV file.<br>
                    - The download will start automatically.<br>
                    - Once completed, download the file from the link.<br>
                </p>
            </div>
        </div>


    </div>
</template>

<script>
import AdminNavbar from '@/components/AdminNavbar.vue'

export default {
    components: { AdminNavbar },
    name: "AdminExport",
    data() {
        return {
            exportStatus: null,
            jobId: null,
            csvUrl: null,
            fileSize: '',
        }
    },
    methods: {
        async exportQuizCSV() {
            try {
                this.exportStatus = 'pending';

                const response = await fetch('http://127.0.0.1:8080/admin_export_quiz_csv', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${localStorage.getItem('jwtToken')}`
                    },
                });

                if (!response.ok) throw new Error("Failed to generate CSV!");

                const data = await response.json();
                this.jobId = data.job_id;
                console.log("Export job has started, JOB ID:", this.jobId);

                // Poll for job status
                const checkStatus = async () => {
                    try {
                        const statusResponse = await fetch(`http://127.0.0.1:8080/export_status/${this.jobId}`, {
                            method: 'GET',
                            headers: {
                                'Content-Type': 'application/json',
                                'Authorization': `Bearer ${localStorage.getItem('jwtToken')}`
                            }
                        });

                        if (!statusResponse.ok) throw new Error("Failed to fetch job status");

                        const statusData = await statusResponse.json();
                        console.log('Job Status:', statusData.status);

                        if (statusData.status === 'completed') {
                            clearInterval(interval);
                            this.exportStatus = 'completed';
                            this.csvUrl = statusData.csv_url;
                            this.fileSize = statusData.file_size || "Unknown size";
                            console.log('Download URL:', this.csvUrl);
                            alert('The download is ready. Click OK.');
                            window.location.href = statusData.csv_url

                        } else if (statusData.status === 'failed') {
                            clearInterval(interval);
                            this.exportStatus = 'failed';
                            console.log('Export Job Failed.');
                            alert("CSV Export Failed! Please Try again later");
                        }
                    } catch (err) {
                        clearInterval(interval);
                        console.error("Error checking job status:", err);
                        alert("Error checking export status. Please refresh and try again.");
                    }
                };

                const interval = setInterval(checkStatus, 3000);

                // Stop polling after 30 seconds if no success
                setTimeout(() => {
                    clearInterval(interval);
                    if (this.exportStatus !== 'completed') {
                        this.exportStatus = 'failed';
                        console.error("30 seconds passed, stopping polling.");
                    }
                }, 30000);
            } catch (error) {
                console.error("Error exporting CSV:", error);
                this.exportStatus = 'failed';
                alert("Error exporting CSV. Please try again.");
            }
        },
    }
}
</script>
