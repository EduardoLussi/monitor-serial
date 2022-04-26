import React, { Component } from 'react';
import api from '../api';
import './Dashboard.css';
import Fog from './Fog';
import { Link } from 'react-router-dom';

export default class Dashboard extends Component {

  state = {
    fogs: [/*{name: "Complex 1"}, {name: "Complex 2"}, {name: "Complex 3"}*/]
  }

  async componentDidUpdate(prevProps) {
    if (this.props !== prevProps && this.props.isAuthenticated) {
      const res = await api.get(`/Fog/${this.props.user.email}`);
      console.log(res.data);
      if (res.data.length == 0) return;
      this.setState({
        fogs: res.data,
      });
    }
  }

  render() {
    return (
        <div className="Devices">
          <ul className="DevicesList">
              {this.state.fogs.lenght === 0 ? <li></li> : this.state.fogs.map(fog => (
                <li>
                  <Link to="/fog" style={{"text-decoration": "none", color:"black"}} onClick={() => window.location.href="/fog"}>
                    <Fog key={fog.id} fog={fog} />
                  </Link>
                </li>
              ))}
          </ul>
      </div>
    );
  }
  
}
