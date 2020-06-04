<template>
    <v-app>
        <v-app-bar app color="secondary" dark>
            <div class="d-flex align-center">
                <h1>Kubebana</h1>
            </div>
            <v-spacer></v-spacer>
        </v-app-bar>
        <v-content>
            <Header></Header>
            <router-view></router-view>
            <Footer></Footer>
        </v-content>
    </v-app>
</template>

<script>
    import Header from './components/Header';
    import Footer from './components/Footer';

    export default {
        name: 'App',

        components: {
            Header,
            Footer
        },

        data: () => ({
            //
        }),
    };
</script>
