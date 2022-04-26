import React, { Component } from 'react';
import api from '../api';
import Devices from './Devices';
import './Content.css';
import axios from 'axios';

export default class App extends Component {

  state = {
    apiUrl: '',
    fogs: [],
    userId: 0,
    api: '',
  }

  async componentDidUpdate(prevProps) {
    if (this.props !== prevProps && this.props.isAuthenticated) {
      console.log(this.props.user);
      const res = await api.get(`/Fog/${this.props.user.email}`);
      console.log(res.data);
      if (res.data.length == 0) return;
      this.setState({
        apiUrl: res.data[0].address,
        fogs: res.data,
        api: axios.create({ baseURL: res.data[0].address })
      });
      console.log(res.data);
    }
  }

  resetDevices = () => {
    this.state.api.post("resetDevices");
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
                <div class="release-button" onClick={() => this.resetDevices()}>
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
