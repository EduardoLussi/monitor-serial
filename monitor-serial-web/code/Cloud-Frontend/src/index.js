import React from 'react';
import ReactDOM from 'react-dom';
import App from './views/App';
import './index.css';
import authConfig from './auth_config.json';

import { Auth0Provider } from '@auth0/auth0-react';

const domain = authConfig.domain;
const clientId = authConfig.clientId;

ReactDOM.render(
  <Auth0Provider
    domain={domain}
    clientId={clientId}
    redirectUri={window.location.origin}>
    <App />
  </Auth0Provider>,
  document.getElementById('root')
);
