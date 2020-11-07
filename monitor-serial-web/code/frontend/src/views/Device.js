import React, { Component } from 'react';
import api from '../api';
import './Device.css'
import imgClose from './img/close.png';
import imgMore from './img/next.png';

export default class App extends Component {

    state = {
        isRunning: 'START',
        values: {
            flag: true
        },
        rate: 0,
        inputClass: '',
        message: ''
    }

  async monitor(target) {
    
    await api.post(`http://localhost:8080/read/${this.props.id}`);

    while (true) {
        const res = await api.get(`http://localhost:8080/read/${this.props.id}`);
        if (res.data.payload === false) {
            target.style.background = "#b8d9ff";
            this.setState({
                isRunning: 'START',
                inputClass: ''
            });

            api.post(`http://localhost:8080/close/${this.props.id}`);
            alert("There is a problem with the reading");
            break
        }

        if (res.data.payload === []) {
            continue
        }

        this.setState({
            values: res.data.payload,
            rate: res.data.rate
        });

        if (this.state.isRunning === 'START') break;
    }
  }

  start = (event) => {
    if (this.state.isRunning === 'START') {
        event.target.style.background = "#ff802b";
        this.setState({
            isRunning: 'STOP',
            inputClass: 'active-button'
        });

        this.monitor(event.target);

    } else {
        event.target.style.background = "#b8d9ff";
        this.setState({
            isRunning: 'START',
            inputClass: ''
        });

        api.post(`http://localhost:8080/close/${this.props.id}`);

    }
  }

  send = async () => {
      if (this.state.isRunning === 'STOP') {
        const res = await api.get(`http://localhost:8080/send/${this.props.id}/${this.state.message}`);
        if (res.data) {
            alert('Message sent succesfully');
        }
      }
  }

  render() {
    let inputSend = this.state.inputClass;
    return (
        <div className="Device">
            <div className="content">
                <div className="title">
                    <img src={require(`./img/${this.props.img}`)} alt={this.props.name}/>
                    <h1>{this.props.name}</h1>
                </div>
                <div className="values">
                    <div className="Props">
                        <ul>
                        {
                            this.props.attributes.map(attribute => (
                                <li key={attribute.id}>
                                    <p>{attribute.name}</p>
                                    <p>{this.state.values.flag ? '0' : this.state.values[attribute.name]}{attribute.unit}</p>
                                </li>
                            ))
                        }
                        </ul>
                    </div>

                    <div className="send">
                        <input type="text" className={inputSend} onChange={e => this.state.message = e.target.value}/>
                        <button onClick={this.send}><img src={require(`./img/send.png`)} alt="Send"/></button>
                    </div>

                    <div className="rate">
                        <p>Rate: </p>
                        <p>{this.state.rate} pck/s</p>
                    </div>

                </div>

                <div className="btnStart">
                    <button className="Start" onClick={this.start}>
                        {this.state.isRunning}
                    </button>
                </div>
            </div>
            <div className="expand">
                <div className="Close">
                    <img src={imgClose} alt="Close"/>
                </div>
                <div className="btnExpand">
                    <img src={imgMore} alt="Expand" />
                </div>
            </div>
        </div>
    );
  }
}
