import React,  { useEffect, useState } from "react";
import "./styles.css";
import { TrainSetting } from "./TrainSetting";
import {ModelUploadComponent} from "./ModelManager"
import {DatasetUploadComponent} from "./DatasetManager"


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
    const [modelName, setModelName] = useState(null);
    const [datasetName, setDatasetName] = useState(null);
    const [instanceNumber, setInstanceNumber] = useState(0);

    const setModelNameFunc = (name) => {
        setModelName(name);
        console.log(name)
    }
    const setDatasetNameFunc = (name) => {
        setDatasetName(name);
        console.log(name)
    }
    const setInstanceNumberFunc = (number) => {
        setInstanceNumber(number);
    }


    console.log(modelName)
    console.log(datasetName)
    return (
    <div className="App">
        <div className="float-container">

            <div className="float-left">
                <ModelUploadComponent setModelNameFunc={setModelNameFunc}/>
            </div>

            <div className="float-right">
                <DatasetUploadComponent setDatasetNameFunc={setDatasetNameFunc}/>
            </div>

            <div className="float-right">
                <h3>Select instance number</h3>
                <input type="number" defaultValue={instanceNumber} onInput={(event) => {setInstanceNumberFunc(event.target.value)}}/>
            </div>
        </div>
        <div className="InteractiveTool">
            {(modelName && datasetName) ? <TrainSetting modelName={modelName} datasetName={datasetName} instanceNumber={instanceNumber}/>: <div/>}
        </div>
    </div>
   );
};


