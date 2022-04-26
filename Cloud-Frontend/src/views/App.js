import React from 'react';
import './App.css';
import Header from './Header';
import Content from './Content';
import Dashboard from './Dashboard';
import { BrowserRouter as Router, Switch, Route } from 'react-router-dom';

import { useAuth0 } from '@auth0/auth0-react';

const App = () => {

  const { user, isAuthenticated } = useAuth0();

  return (
    <div className="App">
      <Router>
        <Header />
        <Switch>
          <Route path="/fog" 
                 render={(props) => <Content {...props} user={user} isAuthenticated={isAuthenticated}/>} />
          <Route path="/"
                 render={(props) => <Dashboard {...props} user={user} isAuthenticated={isAuthenticated}/>} />
        </Switch>
      </Router>
    </div>
  );
}

export default App;
