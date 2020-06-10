<template>
    <v-container>
        <v-app-bar app color="secondary" dark>
                <router-link to="/" style="color: white; font-family: monospace">
                    <h1>Kubebana</h1>
                </router-link>
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
