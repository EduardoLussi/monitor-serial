import React, { Component } from 'react';
import FogDevice from './FogDevice';
import './SerialPort.css';

export default class SerialPort extends Component {

    state = {
        rates: this.props.devices.map(() => 0),
        usage: 0
    }

    setRates = (address, rate) => {
        let { rates } = this.state;
        this.props.devices.map((device, i) => {
            if (device == address) {
                rates[i] = rate;
                this.setState({ rates });
            }
        });
        let totalRate = 0;
        this.state.rates.map(rate => {
            totalRate += rate;
        });
        this.setState({ usage: (totalRate / 144).toFixed(2) });
        console.log(totalRate)
    }

    render() {
        return (
            <li className="SerialPort">
                <div className="SerialPort-content">
                    <div className="sp-title">
                        <div>
                            <img src={require('./img/usb-port.png')} alt="SerialPort" />
                            <h2>Serial {this.props.id}</h2>
                        </div>
                        <p>{this.state.usage}% used</p>
                    </div>
                    <ul className="sp-device-list">
                        {this.props.devices.map(device => (
                            <FogDevice setRates={this.setRates} 
                                       api={this.props.api} 
                                       apiUrl={this.props.apiUrl} 
                                       address={device}/>
                        ))}
                    </ul>
                </div>
            </li>
        )
    }
}
