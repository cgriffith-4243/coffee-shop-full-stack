/* @TODO replace with your variables
 * ensure all variables on this page match your project
 */

export const environment = {
  production: false,
  apiServerUrl: 'http://127.0.0.1:5000', // the running FLASK api server url
  auth0: {
    url: 'thecoffeeshop-cg.us', // the auth0 domain prefix
    audience: 'coffee-shop-cg-endpoint', // the audience set for the auth0 app
    clientId: 'eeS0xYuZlUdDLSA7gC5008GyS8wJ3sx7', // the client id generated for the auth0 app
    callbackURL: 'http://localhost:8100', // the base url of the running ionic application. 
  }
};
