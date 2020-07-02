// src/store.js
import Vue from 'vue';
import Vuex from 'vuex';
import createPersistedState from "vuex-persistedstate";

Vue.use(Vuex);
export default new Vuex.Store({
    strict: true,
    plugins: [createPersistedState()],
    state: {
        jwtToken: null,
    },
    getters: {
        isAuthenticated(state) {
            return state.jwtToken !== null;
        },
        jwtToken(state) {
            return state.jwtToken;
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
