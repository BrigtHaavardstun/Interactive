import React from "react";
import "./styles.css";
import { TrainSetting } from "./TrainSetting";
import 'bootstrap/dist/css/bootstrap.min.css';
import { TestSetting } from "./TestSetting";

const Header = () => (
  <div className="header">
    <h1>Survey on time series</h1>
    <h2>By: MT4XAI project</h2>
  </div>
);

export default () => {
  const queryParameters = new URLSearchParams(window.location.search);
  const mode = queryParameters.get("mode");


  return (
    <div className="App">
      <Header />
      {mode === "train" ?
        <div className="TrainData"><TrainSetting /></div> :
        <div className="TestData"><TestSetting /></div>}
    </div>
  );
};
