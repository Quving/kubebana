<template>
    <v-container>
        <v-app-bar app color="secondary" dark>
            <div class="d-flex align-center">
                <router-link to="/" style="color: white ">
                    <h1>Kubebana</h1>
                </router-link>
            </div>
            <v-spacer></v-spacer>
            <v-btn v-if="isAuthenticated" @click="logout">
                Logout
                <v-icon>mdi-exit-to-app</v-icon>
            </v-btn>
        </v-app-bar>
        <v-row justify="center">
        </v-row>
    </v-container>
</template>
<script>
    import store from '../store/index';

    export default {
        computed: {
            isAuthenticated() {
                return store.getters.isAuthenticated
            }
        },
        methods: {
            logout: function () {
                this.$store.dispatch('logout');
            }
        }
    }
</script>
