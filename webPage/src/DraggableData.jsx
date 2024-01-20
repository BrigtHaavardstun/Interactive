import React from "react";
import { Line } from "react-chartjs-2";
import "chartjs-plugin-dragdata";

const DraggableGraph = ({ dataSetOrg, setDataSet, lineColor, setRandomColor }) => {
  console.log("PROPS:", dataSetOrg);


  const state = {
    dataSet: dataSetOrg,
    labels: ["January", "February", "March", "April", "May", "June", "July"],
    options: {
      tooltips: { enabled: true },
      scales: {
        xAxes: [
          {
            gridLines: { display: false, color: "grey" },
            ticks: { fontColor: "#3C3C3C", fontSize: 14 }
          }
        ],
        yAxes: [
          {
            scaleLabel: {
              display: true,
              labelString: "Color Strength",
              fontSize: 14
            },
            ticks: {
              display: true,
              min: -5,
              max: 100,
              scaleSteps: 50,
              scaleStartValue: -50,
              maxTicksLimit: 4,
              fontColor: "#9B9B9B",
              padding: 30,
              callback: point => (point < 0 ? "" : point)
            },
            gridLines: {
              display: false,
              offsetGridLines: true,
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
        console.log("Start:", e);
      },
      onDrag: function (e, datasetIndex, index, value) {
        console.log("Drag:", datasetIndex, index, value);
      },
      onDragEnd: function (e, datasetIndex, index, value) {
        console.log("Drag End:", state.dataSet);
        const newDataSet = [...state.dataSet];
        newDataSet[datasetIndex][index] = value;
        console.log("DataSet:", newDataSet);
        setDataSet(newDataSet);
        setRandomColor();

      }.bind(this)
    }
  };

  console.log("RENDER");
  const data = {
    labels: state.labels,
    datasets: [
      {
        label: "Metric 1",
        data: state.dataSet[0],
        lineTension: 0.4,
        borderColor: "pink",
        borderWidth: 5,
        pointRadius: 10,
        pointHoverRadius: 10,
        pointBackgroundColor: lineColor,
        pointBorderWidth: 0,
        spanGaps: false,
        dragData: true
      },
      {
        label: "Metric 2",
        data: state.dataSet[1],
        lineTension: 0,
        borderColor: "9B9B9B",
        borderWidth: 5,
        pointRadius: 10,
        pointHoverRadius: 10,
        pointBackgroundColor: lineColor,
        pointBorderWidth: 0,
        spanGaps: false
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
