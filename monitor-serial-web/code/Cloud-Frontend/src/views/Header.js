import React from 'react';
import './Header.css';
import home from './img/smart-home.png';

import { useAuth0 } from '@auth0/auth0-react';

import { Link } from 'react-router-dom';

function App() {

  const { loginWithRedirect, logout, user, isAuthenticated } = useAuth0();

  return (
    <header>
        <div className="home">
            <img src={home} alt="home"/>
            <Link to="/" style={{"text-decoration": "none", color:"white"}} onClick={() => {window.location.href="/"}}>
              <h1>My Home - CIoT</h1>
            </Link>
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
