<template>
    <v-container>
        <v-row justify="center">
            <h2 style="color: grey"> {{podName}}</h2>
        </v-row>
        <v-row>
            <v-textarea background-color="black" loader-height="5" :loading="loading"
                        id="log-container" v-model="log" rows="40" dense readonly
                        :messages="message" outlined>
            </v-textarea>
        </v-row>
        <v-row justify="center">
            <v-btn class="ma-3" color="primary" @click="scrollToNewest">Scroll to latest</v-btn>
            <v-btn class="ma-3" color="primary" @click="fetchPodLog">Refresh</v-btn>
            <v-btn class="ma-3" color="primary" disabled @click="tailLogs">Enable Autorefresh</v-btn>
            <v-btn class="ma-3" color="primary" @click="clearLogs">Clear Logs</v-btn>
        </v-row>
    </v-container>
</template>

<script>
    const config = require('../config');
    const axios = require('axios');

    export default {
        data() {
            return {
                podName: this.$route.params.podName,
                namespace: this.$route.params.namespace,
                deployment: this.$route.params.deployment,
                log: "",
                message: "",
                loading: false,
            }
        },
        created() {
            this.fetchPodLog();
        },
        methods: {
            tailLogs() {

            },
            clearLogs() {
                this.log = '';
            },
            scrollToNewest() {
                const element = document.getElementById('log-container');
                if (element) element.scrollTop = element.scrollHeight;
            },
            fetchPodLog: function () {
                this.loading = true;
                const params = {
                    pod_name: this.podName,
                    namespace: this.namespace,
                    session_id: "randomUUID"
                };
                axios.get(`${config.envs.apiHostUrl}/logs`, {params: params}).then((response) => {
                    this.loading = false;
                    this.log = response.data.log;
                    this.message = "Last Update: " + new Date().toString()
                    this.scrollToNewest();
                })
            }
        },
        watch: {
            // Make sure to make this View is reactive.
            '$route'(to, from) {
                from;
                this.podName += to.params.podName;
            }
        }
    }
</script>
<style>
    #log-container {
        font-family: monospace;
        font-size: 14px;
        color: white;
    }
</style>
