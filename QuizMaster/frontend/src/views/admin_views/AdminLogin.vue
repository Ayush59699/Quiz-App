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



        <div class="container py-4">
            <div class="row justify-content-center">
                <div class="col-md-6">
                    <div class="card border">
                        <div class="card-header bg-primary text-white">
                            <h4 class="mb-0">Admin Login</h4>
                        </div>
                        <div class="card-body">
                            <div v-if="error_msg" class="alert alert-danger" role="alert">
                                {{ error_msg }}
                            </div>

                            <form @submit.prevent="admin_login">
                                <div class="mb-3">
                                    <label class="form-label" for="admin_username">Admin Email</label>
                                    <input class="form-control" type="email" id="admin_username" v-model="admin_email"
                                        required />
                                </div>

                                <div class="mb-3">
                                    <label class="form-label" for="admin_password">Password</label>
                                    <input class="form-control" type="password" id="admin_password"
                                        v-model="admin_password" required />
                                </div>

                                <div class="mb-3 form-check">
                                    <input class="form-check-input" type="checkbox" id="rememberMe" />
                                    <label class="form-check-label" for="rememberMe">
                                        Remember me
                                    </label>
                                </div>

                                <button type="submit" class="btn btn-primary">
                                    Login
                                </button>
                            </form>
                        </div>
                    </div>
                </div>
            </div>
        </div>





    </div>
</template>


<script>
export default {
    name: 'AdminLogin',
    data() {
        return {
            admin_email: '',
            admin_password: '',
            admin_name: '',
            error_msg: ''
        };
    },
    methods: {
        async admin_login() {
            try {
                const response = await fetch("http://127.0.0.1:8080/admin_login", {
                    method: "POST",
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        admin_email: this.admin_email,
                        admin_password: this.admin_password,
                        admin_name: this.admin_name
                    }),
                });
                const data = await response.json()
                if (data.access_token) {
                    console.log(data.access_token)
                    localStorage.setItem('jwtToken', data.access_token);
                    localStorage.setItem('admin_name', this.admin_name);
                    this.$router.push('/admin_dashboard')
                }
                else {
                    this.error_msg = data.message
                }
            }
            catch {
                (error)
                console.log("Some error")
            }
        }
    }
}
</script>

<style>
.navbar {
    border: 2px solid rgb(153, 168, 194);
}
</style>