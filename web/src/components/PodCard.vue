<template>
    <div id="app">
        <v-card class="mx-auto" min-width="300" max-width="300" outlined raised>
            <v-list-item>
                <v-list-item-content>
                    <div class="overline mb-4">POD</div>
                    <v-list-item-title class="headline mb-1">{{deployment}}</v-list-item-title>
                    <v-list-item-subtitle></v-list-item-subtitle>
                </v-list-item-content>
            </v-list-item>
            <v-divider></v-divider>
            <v-list-item>
                <v-list-item-content>
                    <v-list-item-title>name:</v-list-item-title>
                    <v-list-item-subtitle>{{podName}}</v-list-item-subtitle>
                </v-list-item-content>
            </v-list-item>
            <v-list-item>
                <v-list-item-content>
                    <v-list-item-title>created at:</v-list-item-title>
                    <v-list-item-subtitle>{{creationTimestamp}}</v-list-item-subtitle>
                </v-list-item-content>
            </v-list-item>
            <v-card-actions>
                <v-btn @click="showLogView">View Logs</v-btn>
            </v-card-actions>
        </v-card>
    </div>
</template>

<script>
    export default {
        name: 'PodsCard',
        props: {
            deployment: String,
            namespace: String,
            podName: String,
            creationTimestamp: String,
        },
        methods: {
            showLogView: function () {
                this.$router.push(`/namespace/${this.namespace}/deployment/${this.deployment}/pod/${this.podName}`);
            }
        }
    }
</script>
<style>
</style>

