import React, { Component } from 'react';
import api from '../api';
import './Device.css'
import imgClose from './img/close.png';
import imgSearch from './img/history.png';
import imgMore from './img/next.png';

export default class App extends Component {

    state = {
        isRunning: 'START',
        values: {
            flag: true
        }
    }

  async monitor(target) {
    while (true) {
        const res = await api.get(`http://localhost:8080/read/${this.props.id}`);
        if (res.data.payload === false) {
            alert("There is a problem with the reading");
            target.style.background = "#b8d9ff";
            this.setState({
                isRunning: 'START'
            });

            api.post(`http://localhost:8080/close/${this.props.id}`);
            break
        }

        if (res.data.payload === []) {
            continue
        }

        this.setState({
            values: res.data.payload
        });
        if (this.state.isRunning === 'START') break;
    }
  }

  start = (event) => {
    if (this.state.isRunning === 'START') {
        event.target.style.background = "#ff802b";
        this.setState({
            isRunning: 'STOP'
        });

        this.monitor(event.target);

    } else {
        event.target.style.background = "#b8d9ff";
        this.setState({
            isRunning: 'START'
        });

        api.post(`http://localhost:8080/close/${this.props.id}`);

    }
  }


  render() {
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
                                    <p>{this.state.values.flag ? '0' : this.state.values[attribute.name]}</p>
                                </li>
                            ))
                        }
                        </ul>
                    </div>

                    <div className="Search">
                        <div className="BtnSearch">
                            <img src={imgSearch} alt="Search"/>
                            <p>Search</p>
                        </div>
                        <input type="date"/>
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
