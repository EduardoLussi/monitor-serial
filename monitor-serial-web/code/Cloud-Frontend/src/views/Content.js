import React, { Component } from 'react';
import api from '../api';
import Devices from './Devices';
import './Content.css';

export default class App extends Component {

  state = {
    apiUrl: '',
    fogs: [],
    userId: 0
  }

  async componentDidUpdate(prevProps) {
    if (this.props !== prevProps && this.props.isAuthenticated) {
      console.log(this.props.user);
      const res = await api.get(`/Fog/${this.props.user.email}`);
      this.setState({
        apiUrl: res.data[0].address,
        fogs: res.data,
      });
      console.log(res.data);
    }
  }

  render() {
    if (this.state.apiUrl !== '') {
      return (
        <div className="page-content">
            <div class="side-menu">
                <div className="side-menu-content">
                  <button><img src={require(`./img/open-menu.png`)} alt="Open Menu"/></button>
                  <ul>
                      {this.state.fogs.map(fog => (
                        <li onClick={() => {this.setState({ apiUrl: fog.address })}}>{fog.name}</li>
                      ))}
                  </ul>
                </div>
                <div class="release-button">
                  <img src={require('./img/refresh.png')} alt="release"/>
                </div>
            </div>
            <Devices apiUrl={this.state.apiUrl}/>
        </div>
      );
    } else {
      return (<div></div>);
    }
  }
}
