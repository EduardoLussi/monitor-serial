import React from 'react';
import './Header.css';
import home from './img/smart-home.png';

import { useAuth0 } from '@auth0/auth0-react';

function App() {

  const { loginWithRedirect, logout, user, isAuthenticated } = useAuth0();

  return (
    <header>
        <div className="home">
            <img src={home} alt="home"/>
            <h1>My Home - CIoT</h1>
            <div className="login">
              {!isAuthenticated ? (<button className="login" onClick={() => loginWithRedirect()}>Login</button>) : (
                <div>
                  <p className="user">{user.given_name}</p>
                  <p onClick={() => logout()} className="logout">Logout</p>
                </div>
              )}
            </div>
        </div>
    </header>
  );
}

export default App;
