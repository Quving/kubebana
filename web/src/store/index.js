// src/store.js
import Vue from 'vue';
import Vuex from 'vuex';
import createPersistedState from "vuex-persistedstate";

Vue.use(Vuex);
export default new Vuex.Store({
    strict: true,
    plugins: [createPersistedState()],
    state: {
        credentials: null,
        homePreferences: {
            selectedNamespace: null,
            selectedDeployments: null
        }
    },
    getters: {
        isAuthenticated(state) {
            return state.credentials !== null;
        },
        credentials(state) {
            return state.credentials;
        },
        userHomePreferences(state) {
            return state.homePreferences;
        }
    },
    mutations: {
        authUser(state, userData) {
            state.credentials = userData.credentials;
        },
        homePreferences(state, data) {
            state.homePreferences = data.preferences;
        },
        clearUserData(state) {
            state.credentials = null;
            state.homePreferences = {
                selectedNamespace: null,
                selectedDeployments: null
            };
        }

    },
    actions: {
        homeview: ({commit}, data) => {
            commit('homePreferences', {
                preferences: data.preferences
            });
        },
        login: ({commit}, data) => {
            commit('authUser', {
                credentials: data.credentials,
            });
        },
        logout: ({commit}) => {
            commit('clearUserData');
        }
    }
});
