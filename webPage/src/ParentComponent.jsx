import React, { useEffect, useState } from 'react';
import DraggableGraph from './DraggableData';
import axios from 'axios';
import BasicExample from "./MyProgressBar";


export const ParentComponent = () => {
    const queryParameters = new URLSearchParams(window.location.search)
    const dataSetName = queryParameters.get("domain")
    const instance = queryParameters.get("instance")
    const color_class_map = {
        "0": "rgba(0,100,255,0.5)",
        "1": "rgba(217,2,250,0.5)"
    }
    const updateColor = (dataSet,colorSet) => {
        axios.get('http://localhost:8765/getClass', {
            params: {
                timeSeries: JSON.stringify(dataSet),
                dataSet:dataSetName,// Convert dataSet to a JSON string
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
        } else {
            console.error('Error: updateData was called with a non-array value');
        }
    }

    // To recall the orginal data
     const [lineColorOrg, setLineColorOrg] = useState(
        "rgba(159,159,171,0.25)"
    )
    const [dataSetOriginal, setDataSetOriginal] = useState(
        [0,0] // Replace with python call
    )
    const getOrgData = () => {
        axios.get('http://localhost:8765/getTS',{
            params: {
                dataSet: dataSetName,
                index: parseInt(instance),//73=0 171=1// Convert dataSet to a JSON string
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
    }, []);





    // Movable data
    const [dataSetCurr, setDataSetCurr] = useState([...dataSetOriginal]);
    const [lineColorCurr, setLineColorCurr] = useState('green');
    useEffect(() => { updateColor(dataSetCurr,setLineColorCurr); }, [dataSetCurr]);
    useEffect(() => {
        updateData(dataSetOriginal, setDataSetCurr)
    }, [dataSetOriginal]);

    // Counterfactual data
    const [dataSetCF, setDataSetCF] = useState([...dataSetCurr])
    const [lineColorCF, setLineColorCF] = useState('green');

    const getCFData = () => {
        axios.get('http://localhost:8765/cf', {
            params: {
                timeSeries: JSON.stringify(dataSetCurr),// Convert dataSet to a JSON string
                dataSet: dataSetName
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
    useEffect(() => { getCFData(); }, [dataSetCurr]);
    useEffect(() => { updateColor(dataSetCF, setLineColorCF) }, [dataSetCF]);



    const reset = () => {
        updateData(dataSetOriginal, setDataSetCurr)
    }
    const updateConfidence = (setConfidence, dataset) => {
        axios.get('http://localhost:8765/confidence', {
            params: {
                timeSeries: JSON.stringify(dataset),// Convert dataSet to a JSON string
                dataSet: dataSetName
            }
        })
            .then((res) => {
                console.log(res.data)
                // Display new counterfactual data
                const confidence = parseFloat(res.data)*100; // Percentage
                const confidence_one_dec = Math.round(confidence*10)/10; // one decimal
                setConfidence(confidence_one_dec);


            })
            .catch((error) => {
                console.error('Error:', error);
            });
    };

    const [confidence, setConfidence] = useState(50);
    useEffect(() => {
        updateConfidence(setConfidence,dataSetCurr);
    }, [dataSetCurr]);

    return (
        <div>
            <h2> Probability of class 1</h2>
            <BasicExample currValue={confidence}/>
            <DraggableGraph  dataSetCurrent={dataSetCurr} setDataCurrent={setDataSetCurr} dataSetOriginal={dataSetOriginal} updateData={updateData} dataSetCF={dataSetCF} lineColorCurr={lineColorCurr} lineColorOrg={lineColorOrg}lineColorCF={lineColorCF} />
            <button style={{ fontSize: '20px', padding: '10px 20px' }}  onClick={reset}>Reset to orginal</button>
        </div>
    );
};

