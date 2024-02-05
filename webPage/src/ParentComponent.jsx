import React, { useEffect, useState } from 'react';
import DraggableGraph from './DraggableData';
import axios from 'axios';


export const ParentComponent = () => {

    // Original data TODO: Get this from python script
    const originalData = [35, 39, 50, 91, 46, 85, 10,20,56,92,42,42,42,42,42,70,10]

    // Movable data
    const [lineColorOrg, setLineColorOrg] = useState('green');
    const [dataSetOrg, setDataSetOrg] = useState(
        [...originalData],
    );
    const updateOrgData = (dataSet) => {
        if (Array.isArray(dataSet)) {
            console.log("Updating dataset");
            setDataSetOrg(dataSet);
        } else {
            console.error('Error: updateOrgData was called with a non-array value');
        }
    }
    useEffect(() => {
        console.log("Data set org was updated")
    }, [dataSetOrg]);

    const updateColorOrg = () => {  // Receive setLineColor as a prop
        axios.get('http://localhost:8765/getCol', {
            params: {
                dataSet: JSON.stringify(dataSetOrg),  // Convert dataSet to a JSON string
            }
        })
            .then((res) => {
                // Change the color based on the response

                if (res.data == 1) {
                    setLineColorOrg("green");
                }
                else {
                    setLineColorOrg("red");
                }

            })
            .catch((error) => {
                console.error('Error:', error);
            });
    };
    useEffect(() => {
        console.log("WARNING WARNING! Dataset update!")
    }, [dataSetOrg]);
    useEffect(() => { updateColorOrg(); }, [dataSetOrg]);

    // Counterfactual data
    const [dataSetCF, setDataSetCF] = useState(
        [...dataSetOrg] // Replace with call to python script
    )
    const [lineColorCF, setLineColorCF] = useState('green');

    const getCFData = () => {
        console.log("CF get called");
        axios.get('http://localhost:8765/cf', {
            params: {
                dataSet: JSON.stringify(dataSetOrg)  // Convert dataSet to a JSON string
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
    useEffect(() => {
        console.log("Updated dataSetOrg!");
    }, [dataSetOrg]);
    useEffect(() => { getCFData(); }, [dataSetOrg]);

    const updateCFColor = () => {  // Receive setLineColor as a prop
        axios.get('http://localhost:8765/getCol', {
            params: {
                dataSet: JSON.stringify(dataSetCF)  // Convert dataSet to a JSON string
            }
        })
            .then((res) => {
                // Change the color based on the response

                if (res.data == 1) {
                    setLineColorCF("green");
                }
                else {
                    setLineColorCF("red")
                }

            })
            .catch((error) => {
                console.error('Error:', error);
            });
    };
    useEffect(() => { updateCFColor() }, [dataSetCF]);


    useEffect(
        () => {
            console.log("CF",dataSetCF);
        }, [dataSetCF]
    )


    return (
        <div>
            <DraggableGraph dataSetOrg={dataSetOrg} updateOrgData={updateOrgData} dataSetCF={dataSetCF} />
        </div>
    );
};

