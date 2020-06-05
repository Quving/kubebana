const apiHostProtocol = process.env.KUBEBANA_API_HOST_PROTO ?? 'http'
const apiHostPort = process.env.KUBEBANA_API_HOST_PORT ?? '5000';
const apiHost = process.env.KUBEBANA_API_HOST ?? 'localhost';
const envs = {
    apiHostUrl: `${apiHostProtocol}://${apiHost}:${apiHostPort}/`

}

exports.envs = envs;
