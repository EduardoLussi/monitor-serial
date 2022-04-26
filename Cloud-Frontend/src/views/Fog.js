import React, { Component } from 'react';
import './Fog.css';
import axios from 'axios';
import io from 'socket.io-client';
import SerialPort from './SerialPort';

export default class Fog extends Component {

  state = {
    serialports: [],
    api: axios.create({ baseURL: this.props.fog.address }),
  }

  async componentDidMount() {
    this.registerToSocket();
    
    const res = await this.state.api.get("devices");
    console.log(res.data);
    this.setState({ serialports: res.data });
    // if (this.props.fog.name == "Complex 1")
    //   this.setState({ serialports: [[11], [12], [13]] })
    // else if (this.props.fog.name == "Complex 2")
    //   this.setState({ serialports: [[21], [22], [23]] })
    // else
    //   this.setState({ serialports: [[31], [32], [33]] })
  }

  registerToSocket = () => {
    const socket = io(this.props.fog.address);
    socket.on('devices', res => {
        this.setState({ serialports: res.data });
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
                            {this.state.serialports.map((devices, i) => (
                                <SerialPort 
                                  id={i}
                                  devices={devices} 
                                  api={this.state.api} 
                                  apiUrl={this.props.fog.address}/>
                            ))}
                        </ul>
                    </div>
                </div>
            </div>
        </div>
    );
  }
  
}
