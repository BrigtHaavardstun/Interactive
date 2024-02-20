import React from "react";
import { Line } from "react-chartjs-2";
import "chartjs-plugin-dragdata";




const DraggableGraph = ({ dataSetOriginal}) => {
  console.log(dataSetOriginal)
  const data_label = Array.from({length: dataSetOriginal.length}, (_, i) => i);
  const state = {
    dataSet: [dataSetOriginal],
    labels: data_label,
    options: {
      tooltips: { enabled: true },
      scales: {
        xAxes: [
          {
            gridLines: { display: false, color: "grey" },
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
              min: -2,
              max: 2.5,
              stepSize: 0.01,
              //maxTicksLimit: 4,
              fontColor: "#9B9B9B",
              padding: 30,
              callback: function(value,index){
                const step_size =  10
                return index%step_size == 0 ? value : null;
              }
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
        display: true,

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
        updateData([...newDataSet], setDataCurrent);

      }.bind(this)
    }
  };

  //console.log("RENDER");
  const data = {
    labels: state.labels,
    datasets: [
        {
        label: "Original",
        data: state.dataSet[0],
        lineTension: 0,
        borderColor: "rgba(159,159,171,0.25)",
        borderWidth: 5,
        pointRadius: 1,
        pointHoverRadius: 1,
        pointBackgroundColor:  "rgba(159,159,171,0.25)",
        pointBorderWidth: 1,
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
