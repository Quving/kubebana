// src/services/AuthService.js
import axios from 'axios';

const config = require('../config');

export default {
    login(username, password) {
        const credentials = {
            username: username,
            password: password
        }
        const url = config.envs.apiHostUrl + '/auth/';
        return axios.get(url, {auth: credentials})
    },
};
