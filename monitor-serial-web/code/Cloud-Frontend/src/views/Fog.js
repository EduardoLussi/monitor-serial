import React, { Component } from 'react';
import './Fog.css';
import axios from 'axios';
import io from 'socket.io-client';
import FogDevice from './FogDevice';

export default class Fog extends Component {

  state = {
    devices: [],
    api: axios.create({ baseURL: this.props.fog.address }),
  }

  async componentDidMount() {
    this.registerToSocket();
    
    const res = await this.state.api.get("devices");
    console.log(res.data);
    this.setState({ devices: res.data });
  }

  registerToSocket = () => {
    const socket = io(this.props.fog.address);
    socket.on('devices', res => {
        this.setState({ devices: res.data });
    });
  }

  render() {
    return (
        <div className="Device fog">
            <div className="content">
                <div className="title fog-title">
                    <img src={require('./img/smart-home-colored.png')} alt="smart-home" />
                    <h1>{this.props.fog.name}</h1>
                </div>
                <div className="values">
                    <div className="fog-list-content">
                        <ul className="fog-list">
                            {this.state.devices.map(device => (
                                <FogDevice api={this.state.api} apiUrl={this.props.fog.address} address={device}/>
                            ))}
                        </ul>
                    </div>
                </div>
            </div>
        </div>
    );
  }
  
}
