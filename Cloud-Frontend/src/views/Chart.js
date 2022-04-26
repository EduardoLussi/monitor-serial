import React, { Component } from 'react';

import api from '../api';

import CanvasJSReact from '../assets/canvasjs.react';
var CanvasJSChart = CanvasJSReact.CanvasJSChart;

export default class Chart extends Component {

    setDataSet() {
        const id = this.props.attribute == 'rate' ? 0 : this.props.attribute.id;
        api.get(`http://localhost:8080/getValues/${this.props.id}/${this.props.from}/${this.props.to}/${id}`)
        .then(res => {
            console.log(res);
            if (res.data !== false) {    
                let dataPoints = [];
                for (let i = 0; i < res.data.values.length; i++) {
                    let obj = {
                        x: res.data.dates[i] * 1000,
                        y: res.data.values[i]
                    }
                    console.log(obj);
                    dataPoints.push(obj);
                }
                this.setState({
                    dataPoints
                });
            }

            this.chart.render();
        })
        .catch(() => {
            this.setState({
                dataPoints: []
            });
            this.chart.render();
        });

        
    }

    state = {
        dataPoints: []
    }

    componentDidUpdate(prevProps) {
        if (JSON.stringify(prevProps) !== JSON.stringify(this.props)) {
          this.setDataSet();
        }
      }

    render() {			
        const options = {
			animationEnabled: true,
			exportEnabled: true,
			theme: "light2", // "light1", "dark1", "dark2",
			title:{
				text: this.props.attribute.name
            },
            toolTip:{   
                content: "{x}: {y}",
            },
            axisX:{
                valueFormatString: "DD-MM HH:mm:ss"
            },
			data: [{
                type: "line",
                xValueType: "dateTime",
                xValueFormatString: "DD-MM HH:mm:ss:fff",
				dataPoints: this.state.dataPoints
			}]
        }

		return (
            <div>
                <CanvasJSChart options = {options} 
                    onRef={ref => this.chart = ref}
                />
            </div>
		);
    }
}
