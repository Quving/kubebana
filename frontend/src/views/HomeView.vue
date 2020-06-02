<template>
    <div class="home">
        <v-layout row wrap>
            <v-container fluid>
                <v-row dense justify="center" align="center">
                    <v-col v-for="pod in pods" :key="pod.uuid" cols="auto">
                        <PodsCard
                                :deployment="pod.deployment"
                                :pod-name="pod.name"
                                :grid-name="pod.creation_timestamp">
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
                pods: []
            }
        },
        components: {
            PodsCard
        },
        watch: {
            // call again the method if the route changes
            '$route': 'fetchData'
        },
        created() {
            this.fetchData();
        },
        methods: {
            fetchData() {
                this.loading = true
                let url = 'http://localhost:5000/pods/?namespace=testing'
                axios.get(url).then((response) => {
                    this.loading = false;
                    console.log(response.data)
                    this.pods = response.data;
                })
            }
        },
    }
</script>
