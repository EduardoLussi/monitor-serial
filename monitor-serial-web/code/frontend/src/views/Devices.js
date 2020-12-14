import React, { Component } from 'react';
import Device from './Device';
import Chart from './Chart';
import './Devices.css';
import api from '../api';

export default class App extends Component {

  state = {
    devices: []
  }

  async componentDidMount() {
    const res = await api.get('devices');
    this.setState({
      devices: res.data.devices
    });
    // this.setState({
    //     devices: [
    //         {
    //             name: 'Fire Alarm',
    //             img: 'fire-alarm.png',
    //             attributes: [
    //                 {
    //                     id: 1,
    //                     name: 'humidity',
    //                     unit: '%'
    //                 },
    //                 {
    //                     id: 2,
    //                     name: 'temperature',
    //                     unit: 'ºC'
    //                 },
    //                 {
    //                     id: 3,
    //                     name: 'gas',
    //                     unit: '%'
    //                 },
    //                 {
    //                     id: 4,
    //                     name: 'flames',
    //                 }
                    
    //             ]
    //         },
    //         {
    //             name: 'RFID',
    //             img: 'rfid.png',
    //             attributes: [
    //                 {
    //                     id: 1,
    //                     name: 'tag',
    //                     unit: '  '
    //                 }
    //             ]
    //         },
    //         {
    //             name: 'Water Metering',
    //             img: 'pipe.png',
    //             attributes: [
    //                 {
    //                     id: 1,
    //                     name: 'consume',
    //                     unit: ' '
    //                 }
    //             ]
    //         }
    //     ]
    //   });
  }
  
  render() {
    return (
      <div className="Devices">
          <ul className="DevicesList">
              {this.state.devices === false ? <li></li> : this.state.devices.map(device => (
                <li>
                  <Device id={this.state.devices.indexOf(device)} 
                          name={device.name} 
                          img={device.img} 
                          attributes={device.attributes} />
                </li>
              ))}
              {/* <li>
                  <div className="Device">
                <div className="content">
                    <div className="title">
                        <img src={require(`./img/pipe.png`)}/>
                        <h1>Water Metering</h1>
                    </div>
                    <div className="values">
                        <div className="Props">
                            <ul>
                              <li>
                                <p>Water Consumption</p>
                                <p>4 L</p>
                              </li>
                              <li>
                                <p>Time Last 5 L Consuming</p>
                                <p>12:02:23</p>
                              </li>
                              <li>
                                <p>Daily Consumption</p>
                                <p>150 L</p>
                              </li>
                            </ul>
                        </div>

                        <div className="send">
                            <input type="text" />
                            <button><img src={require(`./img/send.png`)} alt="Send"/></button>
                        </div>

                        <div className="maxRate">
                            <p>Last 3 minutes: </p>
                            <input 
                                type="range" 
                                min="1" max="60" 
                                value="3"
                                className="rangeInput"
                            />
                        </div>

                        <div className="maxRate">
                            <p>Time Last 5 L Consuming: </p>
                            <input 
                                type="range" 
                                min="1" max="50" 
                                value="5"
                                className="rangeInput"
                            />
                        </div>

                    </div>

                    <div className="btnStart">
                        <button className="Start">
                            START
                        </button>
                    </div>
                </div>
                <div className="expand">
                    <div className="Close">
                        <img src={require(`./img/close.png`)} alt="Close"/>
                    </div>
                    <div className="btnExpand">
                        <img src={require(`./img/next.png`)} alt="Expand" />
                    </div>
                </div>
                <div className="expand-data">
                    <div className="graph-container">
                        <div className="graph-content">
                            <div className="graph-attributes">
                                <ul>
                                    <li>
                                        1<span>1 - Water Consumption</span>                
                                    </li>
                                </ul>
                            </div>
                            <div className="graph">
                                <Chart />
                            </div>
                        </div>
                    </div>
                    <div className="graph-search">
                        <div className="from-to">
                            <div>
                                <p>From:</p>
                                <input type="datetime-local"/>
                            </div>
                            <div>
                                <p>To:</p>
                                <input type="datetime-local"/>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
              </li> */}
          </ul>
      </div>
    );
  }
}
