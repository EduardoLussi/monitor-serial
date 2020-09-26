import React from 'react';
import './Header.css';
import home from './img/smart-home.png';

function App() {
  return (
    <header>
        <div className="home">
            <img src={home} alt="home"/>
            <h1>My Home</h1>
        </div>
    </header>
  );
}

export default App;
