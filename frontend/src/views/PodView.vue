<template>
    <v-container>
        <v-row justify="center">
            <h2>Pod: '{{podName}}'</h2>
        </v-row>
        <v-row align="start">
            <v-textarea id="log-container" v-model="log" rows="40" readonly color="teal" clearable counter="100000"
                        :messages="message" outlined>
                <template v-slot:label>
                    <div>
                        Bio <small>(optional)</small>
                    </div>
                </template>
            </v-textarea>
        </v-row>
        <v-row>
            <v-col>
                <v-btn @click="scrollToNewest">Scroll to latest</v-btn>
            </v-col>
            <v-col>
                <v-btn disabled @click="tailLogs">Tail Logs</v-btn>
            </v-col>
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
            }
        },
        created() {
            this.fetchPodLog();
        },
        methods: {
            tailLogs() {

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
                    this.message = "Latest Updated: " + new Date().toString()
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
