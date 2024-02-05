import React from "react";
import { Line } from "react-chartjs-2";
import "chartjs-plugin-dragdata";




const DraggableGraph = ({ dataSetOrg, updateOrgData, dataSetCF }) => {
  //console.log("PROPS:", dataSetOrg);
  const data_label = Array.from({length: dataSetOrg.length}, (_, i) => i);


  const state = {
    dataSet: [dataSetOrg, dataSetCF],
    labels: data_label,
    options: {
      tooltips: { enabled: true },
      scales: {
        xAxes: [
          {
            gridLines: { display: true, color: "grey" },
            ticks: {
              fontColor: "#3C3C3C",
              fontSize: 14,
              callback: function(value,index){
                const step_size =  2
                return index%step_size == 0 ? value : null;
              }
            }
          }
        ],
        yAxes: [
          {
            scaleLabel: {
              display: true,
              labelString: "Domain Spesific Y label",
              fontSize: 14
            },
            ticks: {
              display: true,
              min: -100,
              max: 100,
              stepSize: 20,
              //maxTicksLimit: 4,
              fontColor: "#9B9B9B",
              padding: 30,
              callback: point => point
            },
            gridLines: {
              display: true,
              offsetGridLines: false,
              color: "3C3C3C",
              tickMarkLength: 4
            }
          }
        ]
      },
      legend: {
        display: true
      },
      dragData: true,
      dragOptions: {
        showTooltip: true
      },
      dragDataRound: 1,
      onDragStart: function (e) {
        //console.log("Start:", e);
      },
      onDrag: function (e, datasetIndex, index, value) {
        //console.log("Drag:", datasetIndex, index, value);
      },
      onDragEnd: function (e, datasetIndex, index, value) {
        //console.log("Drag End:", state.dataSet);
        const newDataSet = state.dataSet[0];
        newDataSet[index] = value;
        console.log("DataSet:", dataSetOrg);
        updateOrgData([...newDataSet]);
        //console.log("new Dataset:", dataSetOrg);

      }.bind(this)
    }
  };

  //console.log("RENDER");
  const data = {
    labels: state.labels,
    datasets: [
      {
        label: "Orginal 1",
        data: state.dataSet[0],
        lineTension: 0,
        borderColor: "rgba(255,0,100,0.5)",
        borderWidth: 5,
        pointRadius: 10,
        pointHoverRadius: 10,
        pointBackgroundColor: "rgba(255,0,100,0.5)",
        pointBorderWidth: 0,
        spanGaps: false,
        dragData: true,
        fill: false
      },
      {
        label: "Counterfactual 2",
        data: state.dataSet[1],
        lineTension: 0,
        borderColor: "rgba(0,0,255,0.5)",
        borderWidth: 5,
        pointRadius: 10,
        pointHoverRadius: 10,
        pointBackgroundColor: "rgba(0,0,255,0.5)",
        pointBorderWidth: 0,
        spanGaps: false,
        dragData: false,
        fill: false

      }
    ]
  };
  return (
    <div>
      <Line data={data} options={state.options} />
    </div>
  );
};

export default DraggableGraph;
