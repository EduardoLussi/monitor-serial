import React, { Component } from 'react'
import io from 'socket.io-client';
import './FogDevice.css';

export default class FogDevice extends Component {
    state = {
        img: 'cpu.png',
        name: '',
        rate: 0,
        maxRate: 200,
        red: 0,
        green: 255,
        packetSize: 1,
    }

    async componentDidMount() {
        // if (String(this.props.address)[1] == 1) {
        //     var statusColor;
        //     var rate;

        //     if (String(this.props.address)[0] == 1) {
        //         rate = 5;
        //         statusColor = (rate / 200) * 510;
        //     } else if (String(this.props.address)[0] == 2) {
        //         rate = 50;
        //         statusColor = (rate / 200) * 510;
        //     } else {
        //         rate = 100;
        //         statusColor = (rate / 200) * 510;
        //     }
            
        //     this.setState({ rate,
        //         red: statusColor > 255 ? 255 : statusColor,
        //         green: statusColor > 255 ? -(statusColor - 510) : 255 });
            
        //     this.props.setRates(this.props.address, rate * 10);
            
        //     this.setState({ img: "fire-alarm.png", 
        //                     name: "Fire Alarm",
        //                     maxRate: 200,
        //                     packetSize: 10 });
        // } else if (String(this.props.address)[1] == 2)
        //     this.setState({ img: "rfid.png", 
        //                     name: "RFID",
        //                     maxRate: 50,
        //                     packetSize: 14 });
        // else
        //     this.setState({ img: "pipe.png", 
        //                     name: "Water Metering",
        //                     maxRate: 50,
        //                     packetSize: 14 });


        const res = await this.props.api.get(`device/${this.props.address}`);
        console.log(res.data);
        this.setState({ img: res.data.device.img, 
                        name: res.data.device.name,
                        maxRate: res.data.maxRate,
                        packetSize: res.data.device.packetSize });
        this.registerToSocket();
    }

    registerToSocket = () => {
        const socket = io(this.props.apiUrl);
        socket.on(`${this.props.address}Status`, data => {
            this.setState({ maxRate: data.maxRate });
        });
        socket.on(`${this.props.address}Payload`, data => {
            const statusColor = (data.rate / this.state.maxRate) * 510;
            this.setState({ rate: data.rate,
                            red: statusColor > 255 ? 255 : statusColor,
                            green: statusColor > 255 ? -(statusColor - 510) : 255 });
            this.props.setRates(this.props.address, data.rate * this.state.packetSize);
        });
    }

    render() {
        return (
            <li className="fog-device" style={{
                background: `linear-gradient(rgb(255,255,255), rgba(${this.state.red}, ${this.state.green}, 0, 0.05))`,
                "box-shadow": `0px 0px 5px 1px rgba(${this.state.red}, ${this.state.green}, 0, 0.3)`
            }}>
                <img src={require(`./img/${this.state.img}`)} alt={this.state.name} />
                <h2>{this.state.name}</h2>
                <p>{this.state.rate} pck/s</p>
            </li>
        )
    }
}
