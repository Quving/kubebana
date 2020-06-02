<template>
    <v-app>
        <v-app-bar app color="secondary" dark>
            <div class="d-flex align-center">
                <h1>Kubebana</h1>
            </div>
            <v-spacer></v-spacer>
        </v-app-bar>

        <v-content>
            <HomeView/>
        </v-content>
    </v-app>
</template>

<script>
    import HomeView from './views/HomeView';

    export default {
        name: 'App',

        components: {
            HomeView,
        },

        data: () => ({
            //
        }),
    };
</script>
