<template>
    <div id="app">
        <v-card class="mx-auto" min-width="300" max-width="344" outlined>
            <v-list-item three-line>
                <v-list-item-content>
                    <div class="overline mb-4">POD</div>
                    <v-list-item-title class="headline mb-1">{{deployment}}</v-list-item-title>
                    <v-list-item-subtitle>{{podName}}</v-list-item-subtitle>
                    <v-spacer></v-spacer>
                    <v-list-item-subtitle>{{gridName}}</v-list-item-subtitle>
                </v-list-item-content>
                <v-list-item-avatar tile size="80" color="grey"></v-list-item-avatar>
            </v-list-item>
            <v-card-actions>
                <v-btn text>Logs</v-btn>
                <v-btn text>Details</v-btn>
            </v-card-actions>
        </v-card>
    </div>
</template>

<script>
    export default {
        name: 'PodsCard',
        props: {
            deployment: String,
            podName: String,
            gridName: String,
        },
    }
</script>
<style>
</style>

