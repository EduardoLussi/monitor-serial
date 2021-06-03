import React, { Component } from 'react'
import io from 'socket.io-client';

export default class FogDevice extends Component {
    state = {
        img: 'cpu.png',
        name: '',
        rate: 0,
        maxRate: 1000,
        red: 0,
        green: 255,
    }

    async componentDidMount() {
        const res = await this.props.api.get(`device/${this.props.address}`);
        console.log(res.data);
        this.setState({ img: res.data.device.img, 
                        name: res.data.device.name,
                        maxRate: res.data.maxRate });
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
        });
    }

    render() {
        return (
            <li style={{
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
