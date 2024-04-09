import React from "react";
import "./styles.css";
import { TrainSetting } from "./TrainSetting";
//import 'bootstrap/dist/css/bootstrap.min.css';
import { TestSetting } from "./TestSetting";


// <h3>The Prototype is now Interactive.</h3>
// <h3>See if you manage to change the color of Interactive. Note Counterfactual is updated based on your changes of Interactive, and you can see the AI confidence at the top. </h3>
// <h3>Note you can press "Reset to Prototype" at the bottom whenever you want.</h3>
// <h3>When you are done, CLOSE this tab/window, and go back and press Next. </h3>
const Header = () => (
  <div className="header">
    <h3>The Prototype (a typical example) is now Interactive.</h3>
    <h3>Click and drag on the black dots to change the Interactive time series.</h3>
    <h3>When you are done, CLOSE this window. </h3>
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
