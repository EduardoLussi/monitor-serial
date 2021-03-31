import React, { Component } from 'react';
import Device from './Device';
import Chart from './Chart';
import './Devices.css';
import api from '../api';
import io from 'socket.io-client';

export default class App extends Component {

  state = {
    devices: []
  }  

  async componentDidMount() {
    this.registerToSocket();  
    
    const res = await api.get("devices");
    console.log(res.data);
    this.setState({ devices: res.data });
    
  }

  registerToSocket = () => {
    const socket = io("http://localhost:8080");
    socket.on('devices', data => {
        console.log(data);
        this.setState({ devices: data });
    });
  }

  resetDevices = () => {
    api.post("resetDevices");
  }
  
  render() {
    console.log("Rerendering devices");
    return (
      <div className="Devices">
          <button onClick={this.resetDevices}>ATUALIZAR</button>
          <ul className="DevicesList">
              {this.state.devices.lenght === 0 ? <li></li> : this.state.devices.map(device => (
                <li>
                  <Device key={device.id} id={device} />
                </li>
              ))}
          </ul>
      </div>
    );
  }
}
