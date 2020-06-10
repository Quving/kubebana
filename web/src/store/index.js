// src/store.js
import Vue from 'vue';
import Vuex from 'vuex';
import Axios from 'axios';
import AuthService from "../services/AuthService";

Vue.use(Vuex);
export default new Vuex.Store({
    strict: true,
    state: {
        jwtToken: null,
    },
    getters: {
        isLoggedIn: state => !!state.token,
        getUser: state => {
            return state.user;
        }
    },
    mutations: {
        authUser(state, userData) {
            state.jwtToken = userData.token
        },
    },
    actions: {
        login: ({commit}, authData) => {
            AuthService.login(authData.username, authData.password)
                .then(response => {
                    commit('authUser', {
                        idToken: response.data.access_token
                    });
                    Axios.defaults.headers.common['Authorization'] = `JWT ${response.data.access_token}`;
                })
                .catch(error => console.log(error));
        },
        logout: ({commit}) => {
            commit('RESET', '');
        }
    }
});
