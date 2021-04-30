import React from 'react';
import './App.css';
import Header from './Header';
import Content from './Content';

import { useAuth0 } from '@auth0/auth0-react';

const App = () => {

  const { user, isAuthenticated } = useAuth0();

  return (
    <div className="App">
      <Header />
      <Content user={user} isAuthenticated={isAuthenticated}/>
    </div>
  );
}

export default App;
