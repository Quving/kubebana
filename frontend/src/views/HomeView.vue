<template>
    <div class="home">
        <v-layout row wrap>
            <v-container>
                <v-row align="center">
                    <v-col cols="12" sm="6">
                        <v-select
                                v-model="selectedNamespace"
                                :items="namespaces"
                                :menu-props="{ maxHeight: '400' }"
                                label="Namespaces"
                                chips
                                hint="Select a single namespace"
                                persistent-hint
                        ></v-select>
                    </v-col>
                    <v-col cols="12" sm="6">
                        <v-select
                                v-model="selectedDeployments"
                                :items="deployments"
                                :menu-props="{ maxHeight: '400' }"
                                label="Deployments"
                                :disabled="!Boolean(selectedNamespace)"
                                multiple
                                chips
                                hint="Select one or more deployment(s)"
                                persistent-hint
                        ></v-select>
                    </v-col>
                </v-row>
            </v-container>
            <v-divider class="mx-4" :inset="inset" vertical></v-divider>
            <v-container fluid>
                <v-row dense justify="center" align="left">
                    <v-col v-for="pod in pods" :key="pod.uuid" cols="auto">
                        <PodsCard
                                :deployment="pod.deployment"
                                :pod-name="pod.name"
                                :creation-timestamp="pod.creation_timestamp">
                        </PodsCard>
                    </v-col>
                </v-row>
            </v-container>
            <v-footer class="mt-12"></v-footer>
        </v-layout>
    </div>
</template>

<script>
    import PodsCard from "../components/PodCard";

    const axios = require('axios');

    export default {
        name: 'Home',
        data() {
            return {
                loading: true,
                pods: [],
                deployments: [],
                selectedDeployments: [],
                selectedNamespace: "",
                namespaces: []
            }
        },
        components: {
            PodsCard
        },
        watch: {
            '$route': 'fetchData',
            selectedNamespace: function () {
                this.fetchDeployments(this.selectedNamespace)
            },
            selectedDeployments: function () {
                const namespace = this.selectedNamespace
                const deployment = this.selectedDeployments.join(",")

                if (namespace && deployment)
                    this.fetchPods(namespace, deployment)
                else
                    this.pods = []
            },
        },
        created() {
            this.fetchNamespaces()
        },
        methods: {
            fetchNamespaces() {
                const apiHost = 'http://localhost:5000'
                axios.get(`${apiHost}/namespaces/`).then((response) => {
                    this.namespaces = response.data;
                })

            },
            fetchDeployments(namespace) {
                const apiHost = 'http://localhost:5000'
                let params = {
                    namespace: namespace
                }

                axios.get(`${apiHost}/deployments/`, {params: params}).then((response) => {
                    this.deployments = response.data;
                })

            },
            fetchPods(namespaces, deployments) {
                const apiHost = 'http://localhost:5000'
                let params = {
                    namespace: namespaces,
                    deployment: deployments
                }

                axios.get(`${apiHost}/pods/`, {params: params}).then((response) => {
                    this.pods = response.data;
                })
            },
            fetchData() {
                this.loading = true
                this.fetchDeployments(
                    this.selectedNamespace.join(",")
                );
                this.fetchNamespaces();
                this.fetchPods();
                this.loading = false;
            }
        },
    }
</script>
