<template>
    <div class="home">
        <v-layout row>
            <v-container>
                <v-container>
                    <v-row dense>
                        <v-col>
                            <v-checkbox
                                    v-model="hideSystemNamespaces"
                                    disabled
                                    label="Hide system namespaces">
                            </v-checkbox>
                        </v-col>
                        <v-col>
                            <v-row>
                                <v-btn
                                        class="ma-2"
                                        :loading="false"
                                        :disabled="false"
                                        color="success"
                                        @click="selectAllDeployments">
                                    Select All Deployments
                                </v-btn>
                                <v-btn
                                        class="ma-2"
                                        :loading="false"
                                        :disabled="false"
                                        color="success"
                                        @click="disselectAllDeployments">
                                    Disselect All Deployments
                                </v-btn>
                            </v-row>
                        </v-col>
                    </v-row>
                    <v-row dense>
                        <v-col>
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
                        <v-col>
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
                </v-container>
                <v-row dense justify="center">
                    <v-col v-for="pod in pods" :key="pod.uuid" cols="auto">
                        <PodsCard
                                :deployment="pod.deployment"
                                :pod-name="pod.name"
                                :namespace="pod.namespace"
                                :creation-timestamp="pod.creation_timestamp"
                                :docker-image="pod.image"
                        ></PodsCard>
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
                loading: true,
                pods: [],
                text: "Select all Deployments",
                namespaces: [],
                deployments: [],
                selectedNamespace: [],
                selectedDeployments: [],
            }
        },
        components: {
            PodsCard
        },
        watch: {
            '$route': 'fetchData',
            selectedNamespace: function () {
                this.storePreferences();
                this.fetchDeployments(this.selectedNamespace).then(() => {
                    if (this.toggleSelectAllDeployments) {
                        this.selectedDeployments = this.deployments
                        this.fetchPods()
                    }
                })
            },
            selectedDeployments: function () {
                const namespace = this.selectedNamespace
                const deployment = this.selectedDeployments.join(",")
                this.storePreferences();
                if (namespace && deployment)
                    this.fetchPods(namespace, deployment)
                else
                    this.pods = []
            },
        },
        created() {
            this.loadUserPreferences();
            this.fetchNamespaces();
        },
        methods: {
            storePreferences() {
                this.$store.dispatch('homeview', {
                    preferences: {
                        selectedDeployments: this.selectedDeployments,
                        selectedNamespace: this.selectedNamespace
                    }
                })
            },
            fetchNamespaces() {
                new Promise((resolve => {
                    axios.get(`${config.envs.apiHostUrl}/namespaces/`, {
                        auth: this.$store.getters.credentials
                    }).then((response) => {
                        this.namespaces = response.data;
                        this.selectedNamespace = (this.namespaces.includes(this.selectedNamespace)) ? this.selectedNamespace : "";
                        resolve();
                    })
                }));

            },
            loadUserPreferences() {
                const homePreferences = this.$store.getters.userHomePreferences;
                this.selectedDeployments = homePreferences.selectedDeployments ?? [];
                this.selectedNamespace = homePreferences.selectedNamespace ?? "";
            },
            fetchDeployments(namespace) {
                let params = {
                    namespace: namespace
                }

                return new Promise((resolve => {
                    axios.get(`${config.envs.apiHostUrl}/deployments/`, {
                        params: params,
                        auth: this.$store.getters.credentials
                    }).then((response) => {
                        this.deployments = response.data;
                        this.selectedDeployments = this.selectedDeployments.filter(x => this.deployments.includes(x));
                        resolve();
                    })
                }));

            },
            selectAllDeployments: function () {
                this.selectedDeployments = this.deployments;
            },
            disselectAllDeployments: function () {
                this.selectedDeployments = [];
            },
            fetchPods(namespaces, deployments) {
                let params = {
                    namespace: namespaces,
                    deployment: deployments
                }

                axios.get(`${config.envs.apiHostUrl}/pods/`, {
                    params: params,
                    auth: this.$store.getters.credentials
                }).then((response) => {
                    this.pods = response.data;
                })
            },
        },
    }
</script>
