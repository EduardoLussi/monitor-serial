import React, { Component } from 'react';
import Device from './Device';
import './Devices.css';
import api from '../api';

export default class App extends Component {

  state = {
    devices: []
  }

  async componentDidMount() {
    const res = await api.get('ports');
    this.setState({
      devices: res.data
    });
  }
  
  render() {
    return (
      <div className="Devices">
          <ul className="DevicesList">
              {this.state.devices.map(device => (
                <li><Device id={this.state.devices.indexOf(device)} name={device.name} img={device.img} pdu={device.pduType} /></li>
              ))}
          </ul>
      </div>
    );
  }
}
