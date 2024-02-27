import React, { useEffect, useState } from 'react';
import DraggableGraph from './DraggableData';
import axios from 'axios';
import BasicExample from "./MyProgressBar";
import DraggableDataTest from "./DraggableDataTest";


export const TestSetting = () => {
    const queryParameters = new URLSearchParams(window.location.search)
    const dataSetName = queryParameters.get("domain")
    const instance = queryParameters.get("instance")
    const color_class_map = {
        "0": "rgba(0,100,255,0.5)",
        "1": "rgba(217,2,250,0.5)"
    }
    const updateColor = (dataSet, colorSet) => {
        axios.get('http://158.42.185.235:8765/getClass', {
            params: {
                timeSeries: JSON.stringify(dataSet),
                dataSet: dataSetName,// Convert dataSet to a JSON string
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


    const [dataSetOriginal, setDataSetOriginal] = useState(
        [0, 0] // Replace with python call
    )
    const getOrgData = () => {
        axios.get('http://158.42.185.235:8765/getTS', {
            params: {
                data_set: dataSetName,
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







    return (
        <div>
            <DraggableDataTest dataSetOriginal={dataSetOriginal} />
        </div>
    );
};

