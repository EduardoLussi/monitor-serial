import React, { Component } from 'react';
import './Device.css'
import Chart from './Chart';
import imgMore from './img/next.png';
import io from 'socket.io-client';

export default class App extends Component {

    state = {
        config: {
            name: "",
            img: "cpu.png",
            attributes: []
        },
        rate: 0,
        inputClass: '',
        message: '',
        maxRate: 1000,
        from: '',
        to: '',
        attribute: '',
        showExpandData: true,
        payload: [],
        isReading: false
    }


    async componentDidUpdate(prevProps){ 
        if(this.props.id !== prevProps.id){
            this.registerToSocket();
            const res = await this.props.api.get(`device/${this.props.id}`);
            console.log(res.data);
            this.setState({ config: res.data.device, isReading: res.data.isReading });
        }
    }
    
    async componentDidMount() {
        this.registerToSocket();
        const res = await this.props.api.get(`device/${this.props.id}`);
        console.log(res.data);
        this.setState({ config: res.data.device, isReading: res.data.isReading });
    }

    registerToSocket = () => {
        const socket = io(this.props.apiUrl);
        
        socket.on(`${this.props.id}Payload`, data => {
            console.log(data);
            this.setState({ payload: data });
        });

        socket.on(`${this.props.id}Status`, data => {
            console.log(data);
            this.setState({ isReading: data.isReading, maxRate: data.maxRate, rate: data.rate });
        });
    }

  monitor(target) {
    
    if (this.state.maxRate > 1500) {
        this.state.maxRate = 1500;
    }

    this.props.api.post(`http://localhost:8080/read/${this.props.id}/${this.state.maxRate}`);

  }

  start = (event) => {
    if (this.state.isReading) this.props.api.post(`http://localhost:8080/close/${this.props.id}`);
    else this.monitor();
  }

  send = async () => {
      if (this.state.isReading === 'STOP') {
        const res = await this.props.api.get(`http://localhost:8080/send/${this.props.id}/${this.state.message}`);
        if (res.data) {
            alert('Message sent succesfully');
        }
      }
  }

  expandHandleClick = (e) => {
    if (this.state.showExpandData) {
        this.setState({showExpandData: false});
        e.target.style.transform = "rotate(180deg)";
    } else {
        this.setState({showExpandData: true});
        e.target.style.transform = "rotate(0deg)";
    }
  }

  render() {
    let inputSend = this.state.inputClass;
    return (
        <div className="Device">
            <div className="content">
                <div className="title">
                    <img src={require(`./img/${this.state.config.img}`)} alt={this.state.config.name}/>
                    <h1>{this.state.config.name}</h1>
                </div>
                <div className="values">
                    <div className="Props">
                        <ul>
                        {
                            this.state.config.attributes.map(attribute => (
                                <li key={attribute.id}>
                                    <p>{attribute.name}</p>
                                    <p>{this.state.payload[attribute.name]}{attribute.unit}</p>
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

                    <div className="maxRate">
                        <p>Max rate: </p>
                        <input 
                            type="range" 
                            min="1" max="1500" 
                            value={this.state.maxRate} 
                            onChange={e => this.setState({maxRate: e.target.value})}
                            className="rangeInput"
                        />

                        <input 
                            type="text"
                            value={this.state.maxRate}
                            onChange={e => this.setState({maxRate: e.target.value})}
                            className="rangeInputValue"
                        />
                    </div>

                </div>

                <div className="btnStart">
                    <button className={this.state.isReading ? "stop" : "start"} onClick={this.start}>
                        {this.state.isReading ? "STOP" : "START"}
                    </button>
                </div>
            </div>
            <div className="expand">
                <div className="btnExpand">
                    <img src={imgMore} alt="Expand" onClick={this.expandHandleClick}/>
                </div>
            </div>
            {
                this.state.showExpandData ? '' : 
                <div className="expand-data">
                    <div className="graph-container">
                        <div className="graph-content">
                            <div className="graph-attributes">
                                <ul>
                                    {
                                        this.state.config.attributes.map((attribute, index) => (
                                            <li key={attribute.id} onClick={() => {this.setState({attribute: attribute})}}>
                                                {index + 1}<span>{index + 1} - {attribute.name}</span>                
                                            </li>
                                        ))
                                    }
                                </ul>
                            </div>
                            <div className="graph">
                                <Chart 
                                id={this.props.id}
                                attribute={this.state.attribute} 
                                from={this.state.from} 
                                to={this.state.to}/>
                            </div>
                        </div>
                    </div>
                    <div className="graph-search">
                        <div className="from-to">
                            <div>
                                <p>From:</p>
                                <input type="datetime-local" step="1" onChange={e => this.setState({from: e.target.value.replace('T', ' ')})}/>
                            </div>
                            <div>
                                <p>To:</p>
                                <input type="datetime-local" step="1" onChange={e => this.setState({to: e.target.value.replace('T', ' ')})}/>
                            </div>
                        </div>
                    </div>
                </div>
            }
        </div>
    );
  }
}
