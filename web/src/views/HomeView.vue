<template>
    <div class="home">
        <v-layout row>
            <v-container>
                <v-row justify="center" dense>
                    <v-col cols="5">
                        <v-checkbox
                                v-model="hideSystemNamespaces"
                                disabled
                                label="Hide system namespaces">
                        </v-checkbox>
                        <v-select
                                v-model="selectedNamespace"
                                :items="namespaces"
                                :menu-props="{ maxHeight: '400' }"
                                label="Namespaces"
                                chips
                                deletable-chips
                                hint="Select a single namespace"
                                persistent-hint
                        ></v-select>
                    </v-col>
                    <v-col cols="5">
                        <v-checkbox
                                v-model="selectAllDeployments"
                                label="Select all deployments automatically">
                        </v-checkbox>
                        <v-select
                                v-model="selectedDeployments"
                                :items="deployments"
                                :menu-props="{ maxHeight: '400' }"
                                label="Deployments"
                                :disabled="!Boolean(selectedNamespace)"
                                multiple
                                deletable-chips
                                chips
                                hint="Select one or more deployment(s)"
                                persistent-hint
                        ></v-select>
                    </v-col>
                </v-row>
                <v-row dense justify="center">
                    <v-col v-for="pod in pods" :key="pod.uuid" cols="auto">
                        <PodsCard
                                :deployment="pod.deployment"
                                :pod-name="pod.name"
                                :namespace="pod.namespace"
                                :creation-timestamp="pod.creation_timestamp"
                                :docker-image="pod.image
                        ">
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

    const config = require('../config');
    const axios = require('axios');

    export default {
        name: 'Home',
        data() {
            return {
                hideSystemNamespaces: true,
                selectAllDeployments: false,
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
            selectAllDeployments: function(){
                this.selectedDeployments = this.deployments;
            },
            selectedNamespace: async function () {
                this.fetchDeployments(this.selectedNamespace).then(() => {
                        if (this.selectAllDeployments) {
                            this.selectedDeployments = this.deployments
                            this.fetchPods()
                        }
                    }
                )

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
            async fetchNamespaces() {
                new Promise((resolve => {
                    axios.get(`${config.envs.apiHostUrl}/namespaces/`).then((response) => {
                        this.namespaces = response.data;
                        resolve();
                    })
                }));

            },
            async fetchDeployments(namespace) {
                let params = {
                    namespace: namespace
                }

                return new Promise((resolve => {
                    axios.get(`${config.envs.apiHostUrl}/deployments/`, {params: params}).then((response) => {
                        this.deployments = response.data;
                        resolve();
                    })
                }));

            },
            async fetchPods(namespaces, deployments) {
                let params = {
                    namespace: namespaces,
                    deployment: deployments
                }

                axios.get(`${config.envs.apiHostUrl}/pods/`, {params: params}).then((response) => {
                    this.pods = response.data;
                })
            },
        },
    }
</script>
