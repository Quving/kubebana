<template>
    <v-app>
        <v-container fluid>
            <v-layout row wrap>
                <v-flex xs12 class="text-center" mt-5>
                    <h1>Login</h1>
                </v-flex>
                <v-flex xs12 sm6 offset-sm3 mt-3>
                    <form @submit.prevent="submit" autocomplete="on">
                        <v-layout column>
                            <v-flex>
                                <v-text-field
                                        name="username"
                                        label="Username"
                                        id="username"
                                        autocomplete="username"
                                        v-model="username"
                                        required>
                                </v-text-field>
                            </v-flex>
                            <v-flex>
                                <v-text-field
                                        name="password"
                                        label="Password"
                                        value="your-password"
                                        id="password"
                                        type="password"
                                        autocomplete="password"
                                        v-model="password"
                                        required>
                                </v-text-field>
                            </v-flex>
                            <v-flex class="text-center" mt-5>
                                <v-btn color="primary"
                                       type="submit"
                                >Sign In
                                </v-btn>
                            </v-flex>
                            <v-flex class="text-center" mt-5>
                                <v-alert dense v-if='status' v-bind:type="alert_type">{{ status }}</v-alert>
                            </v-flex>
                        </v-layout>
                    </form>
                </v-flex>
            </v-layout>
        </v-container>
    </v-app>
</template>

<script>
    import AuthService from "../services/AuthService";
    import Axios from "axios";

    export default {
        data: function () {
            return {
                username: '',
                password: '',
                alert_type: '',
                status: ''
            };
        },
        methods: {
            submit: function () {
                AuthService.login(this.username, this.password)
                    .then(response => {
                        this.$store.dispatch('login', {jwtToken: response.data.access_token});
                        Axios.defaults.headers.common['Authorization'] = `JWT ${response.data.access_token}`;
                        this.$router.push('/');
                        this.alert_type = 'success';
                        this.status = 'Login successful.';
                    })
                    .catch(error => {
                        this.alert_type = 'error';
                        if (error.response.status === 401) {
                            this.status = 'User cannot be found.';
                        } else {
                            this.status = 'Error occured. Please try it later again.';
                        }
                    });
            }
        }
    };
</script>
