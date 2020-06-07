<template>
    <div id="app">
        <v-card class="mx-auto" min-width="350" max-width="350" min-height="400" max-height="900" outlined raised>
            <v-list-item>
                <v-list-item-content>
                    <div class="overline mb-4">POD</div>
                    <v-list-item-title class="headline mb-1">
                        <strong>{{deployment.toUpperCase()}}</strong>
                    </v-list-item-title>
                    <v-list-item-subtitle></v-list-item-subtitle>
                </v-list-item-content>
            </v-list-item>
            <v-divider></v-divider>
            <v-list-item v-for="(v,k) in listItems" :key="v">
                <v-list-item-content>
                    <v-list-item-title>{{k}}</v-list-item-title>
                    <v-list-item-subtitle>{{v}}</v-list-item-subtitle>
                </v-list-item-content>
            </v-list-item>
            <v-divider></v-divider>
            <v-card-actions>
                <v-btn color="primary" @click="showLogView">Logs</v-btn>
            </v-card-actions>
        </v-card>
    </div>
</template>

<script>
    export default {
        name: 'PodsCard',
        data() {
            return {
                listItems: {
                    "CreatedAt": new Date(this.creationTimestamp).toLocaleString(),
                    "DockerImage": this.dockerImage,
                    "Namespace": this.namespace,
                    "PodName": this.podName,
                }
            }
        },
        props: {
            creationTimestamp: String,
            deployment: String,
            dockerImage: String,
            namespace: String,
            podName: String,
        },
        methods: {
            showLogView: function () {
                let route = this.$router.resolve(`/namespace/${this.namespace}/deployment/${this.deployment}/pod/${this.podName}`);
                window.open(route.href, '_blank');
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

