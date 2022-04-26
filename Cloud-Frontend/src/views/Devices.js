import React, { Component } from 'react';

import axios from 'axios';

import Device from './Device';
import './Devices.css';
import io from 'socket.io-client';

export default class App extends Component {

  state = {
    devices: [],
    api: axios.create({ baseURL: this.props.apiUrl }),
  }  

  async componentDidMount() {
    this.registerToSocket();
    const res = await this.state.api.get("devices");
    let devicesList = [];
    res.data.map(sp => {
      sp.map(device => {
        devicesList.push(device);
      });
    });
    this.setState({ devices: devicesList });
  }

  async componentDidUpdate(prevProps) {
    if(this.props.apiUrl !== prevProps.apiUrl) {
      const newapi = axios.create({ baseURL: this.props.apiUrl });
      this.setState({ 
        devices: [],
        api: newapi
      });
      const res = await newapi.get("devices");
      this.registerToSocket();
      this.setState({ devices: res.data });
    } 
  }

  registerToSocket = () => {
    const socket = io(this.props.apiUrl);
    socket.on('devices', data => {
      let devicesList = [];
      data.map(sp => {
        sp.map(device => {
          devicesList.push(device);
        });
      });
      this.setState({ devices: devicesList });
    });
  }
  
  render() {
    return (
      <div className="Devices">
          <ul className="DevicesList">
              {this.state.devices.lenght === 0 ? <li></li> : this.state.devices.map(device => (
                <li>
                  <Device key={device.id} id={device} api={this.state.api} apiUrl={this.props.apiUrl} />
                </li>
              ))}
          </ul>
      </div>
    );
  }
}
