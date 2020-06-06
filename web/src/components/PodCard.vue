<template>
    <div id="app">
        <v-card class="mx-auto" min-width="300" max-width="300" outlined raised>
            <v-list-item>
                <v-list-item-content>
                    <div class="overline mb-4">POD</div>
                    <v-list-item-title class="headline mb-1">{{titleCase(deployment)}}</v-list-item-title>
                    <v-list-item-subtitle></v-list-item-subtitle>
                </v-list-item-content>
            </v-list-item>
            <v-divider></v-divider>
            <v-list-item>
                <v-list-item-content>
                    <v-list-item-title>PodName</v-list-item-title>
                    <v-list-item-subtitle>{{podName}}</v-list-item-subtitle>
                </v-list-item-content>
            </v-list-item>
            <v-list-item>
                <v-list-item-content>
                    <v-list-item-title>CreatedAt</v-list-item-title>
                    <v-list-item-subtitle>{{creationTimestamp}}</v-list-item-subtitle>
                </v-list-item-content>
            </v-list-item>
            <v-list-item>
                <v-list-item-content>
                    <v-list-item-title>Image</v-list-item-title>
                    <v-list-item-subtitle>{{dockerImage}}</v-list-item-subtitle>
                </v-list-item-content>
            </v-list-item>
            <v-card-actions align="right">
                <v-btn color="primary" @click="showLogView">Logs</v-btn>
                <v-btn disabled color="primary" @click="showDetails">Details</v-btn>
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
            dockerImage: String
        },
        methods: {
            showLogView: function () {
                this.$router.push(`/namespace/${this.namespace}/deployment/${this.deployment}/pod/${this.podName}`);
            },
            showDetails: function () {

            },
            titleCase: function (str) {
                str = str.toLowerCase().split(' ').map(function (word) {
                    return (word.charAt(0).toUpperCase() + word.slice(1));
                });
                return str.join(' ');
            }
        }
    }
</script>
<style>
</style>

