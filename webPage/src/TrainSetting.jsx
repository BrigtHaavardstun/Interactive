import React, { useEffect, useState } from 'react';
import DraggableGraph from './DraggableData';
import axios from 'axios';
import BasicExample from "./MyProgressBar";


export const TrainSetting = ({modelName, datasetName, instanceNumber, cfMethod}) => {

    const cf_mode = cfMethod //native"//queryParameters.get("cf_mode") // native / artificial

    const color_class_map = {
        "0": "rgba(0,100,255,0.5)",
        "1": "rgba(217,2,250,0.5)"
    }
    const updateColor = (dataSet, colorSet) => {
        if (!dataSet || !modelName){
            return;
        }
        axios.get('http://localhost:3030/getClass', {
            params: {
                time_series: JSON.stringify(dataSet),
                data_set_name: datasetName,// Convert dataSet to a JSON string
                model_name: modelName
            }
        })
            .then((res) => {
                // Change the color based on the response
                colorSet(color_class_map[res.data]);


            })
            .catch((error) => {
                console.error('Error:', error);
            });
    };

    const updateData = (dataSet, setData) => {
        if (Array.isArray(dataSet)) {
            setData([...dataSet]);
        } else if(dataSet) {
            console.error('Error: updateData was called with a non-array value');
        } else {
            return;
        }
    }

    // To recall the orginal data
    const [lineColorOrg, setLineColorOrg] = useState(
        "rgba(159,159,171,0.25)"
    )
    const [dataSetOriginal, setDataSetOriginal] = useState(
        null // Replace with python call
    )
    const getOrgData = () => {
        axios.get('http://localhost:3030/getTS', {
            params: {
                data_set_name: datasetName,
                model_name: modelName,
                index: instanceNumber,//73=0 171=1// Convert dataSet to a JSON string
            }
        })
            .then((res) => {
                console.log(res.data);
                setDataSetOriginal(res.data);
            })
            .catch((error) => {
                console.error('Error:', error);
            });
    };

    useEffect(() => {
        getOrgData();
    }, [datasetName, instanceNumber]);





    // Movable data
    const [dataSetCurr, setDataSetCurr] = useState(null);
    const [lineColorCurr, setLineColorCurr] = useState( "rgba(159,159,171,0.25)");
    useEffect(() => { updateColor(dataSetCurr, setLineColorCurr); }, [dataSetCurr,modelName]);
    useEffect(() => { updateData(dataSetOriginal, setDataSetCurr); }, [dataSetOriginal]);

    // Counterfactual data
    const [dataSetCF, setDataSetCF] = useState(null)
    const [lineColorCF, setLineColorCF] = useState( "rgba(159,159,171,0.25)");

    const getCFData = () => {
        if (!dataSetCurr || !modelName){
            return;
        }
        axios.get('http://localhost:3030/cf', {
            params: {
                time_series: JSON.stringify(dataSetCurr),// Convert dataSet to a JSON string
                data_set_name: datasetName,
                model_name: modelName,
                cf_mode: cf_mode
            }
        })
            .then((res) => {

                console.log("CF from python:", res.data);

                // Display new counterfactual data
                setDataSetCF([...res.data]);


            })
            .catch((error) => {
                console.error('Error:', error);
            });
    };
    useEffect(() => { getCFData(); }, [dataSetCurr, modelName]);
    useEffect(() => { updateColor(dataSetCF, setLineColorCF) }, [dataSetCF, modelName]);



    const reset = () => {
        if (!dataSetOriginal) {
            updateData(dataSetOriginal, setDataSetCurr)
        }
    }
    const updateConfidence = (setConfidence, timeseries) => {
        if (!timeseries || !modelName){
            return;
        }
        axios.get('http://localhost:3030/confidence', {
            params: {
                time_series: JSON.stringify(timeseries),// Convert dataSet to a JSON string
                model_name: modelName,
                data_set_name: datasetName
            }
        })
            .then((res) => {
                console.log(res.data)
                // Display new counterfactual data
                const confidence = parseFloat(res.data) * 100; // Percentage
                const confidence_one_dec = Math.round(confidence * 10) / 10; // one decimal
                setConfidence(confidence_one_dec);


            })
            .catch((error) => {
                console.error('Error:', error);
            });
    };

    const [confidence, setConfidence] = useState(100);
    useEffect(() => {
        updateConfidence(setConfidence, dataSetCurr, modelName);
    }, [dataSetCurr, modelName]);

    return (
        <div>
            <BasicExample currValue={confidence} />
            <DraggableGraph dataSetCurrent={dataSetCurr} setDataCurrent={setDataSetCurr}
                dataSetOriginal={dataSetOriginal} updateData={updateData} dataSetCF={dataSetCF}
                lineColorCurr={lineColorCurr} lineColorOrg={lineColorOrg} lineColorCF={lineColorCF}
            />
            <button className={"button"} onClick={reset} >RESET TO PROTOTYPE</button>

        </div>
    );
};

