// src/store.js
import Vue from 'vue';
import Vuex from 'vuex';

Vue.use(Vuex);
export default new Vuex.Store({
    strict: true,
    state: {
        jwtToken: null,
    },
    getters: {
        isAuthenticated(state) {
            return state.jwtToken !== null;
        }
    },
    mutations: {
        authUser(state, userData) {
            state.jwtToken = userData.jwtToken;
        },
        clearAuthData(state) {
            state.jwtToken = null;
        }
    },
    actions: {
        login: ({commit}, authData) => {
            commit('authUser', {
                jwtToken: authData.jwtToken
            });
        },
        logout: ({commit}) => {
            commit('clearAuthData');
        }
    }
});
