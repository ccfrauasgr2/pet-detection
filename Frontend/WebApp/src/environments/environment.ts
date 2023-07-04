/// <reference types="node" />

export const environment = {
    production: true,
    //backendIP: '$BACKEND_IP'
    backendIP: window['process']['env']['BACKEND_IP'] //env['BACKEND_IP']
    //backendPort: process.env.BACKEND_PORT || '<backend-port>'

};