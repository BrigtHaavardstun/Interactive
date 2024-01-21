import React, { useEffect, useState } from 'react';
import DraggableGraph from './DraggableData';
import axios from 'axios';


export const ParentComponent = () => {

    const [lineColorOrg, setLineColorOrg] = useState('green');
    const [dataSetOrg, setDataSetOrg] = useState([
        [65, 59, 80, 81, 56, 55, 40],
        [35, 39, 50, 91, 46, 85, 10],
    ]);
    console.log("Test dataset", dataSetOrg);
    const updateColorOrg = () => {  // Receive setLineColor as a prop
        axios.get('http://localhost:8765/getCol', {
            params: {
                dataSet: JSON.stringify(dataSetOrg)  // Convert dataSet to a JSON string
            }
        })
            .then((res) => {
                // Change the color based on the response

                if (res.data == 1) {
                    setLineColorOrg("green");
                }
                else {
                    setLineColorOrg("red")
                }

            })
            .catch((error) => {
                console.error('Error:', error);
            });
    };
    useEffect(() => { updateColorOrg(); }, [dataSetOrg]);

    const [dataSetCF, setDataSetCF] = useState([
        [65, 59, 80, 81, 56, 55, 40],
        [35, 39, 50, 91, 46, 85, 10],
    ]);
    const [lineColorCF, setLineColorCF] = useState('green');

    const getCFData = () => {
        axios.get('http://localhost:8765/cf', {
            params: {
                dataSet: JSON.stringify(dataSetOrg)  // Convert dataSet to a JSON string
            }
        })
            .then((res) => {

                // Display new counterfactual data
                setDataSetCF(res.data);

            })
            .catch((error) => {
                console.error('Error:', error);
            });
    };

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
    useEffect(() => { updateCFColor() }, [dataSetOrg]);




    return (
        <div>
            <DraggableGraph dataSetOrg={dataSetOrg} setDataSet={setDataSetOrg} lineColor={lineColorOrg} setRandomColor={updateColorOrg} />
            <DraggableGraph dataSetOrg={dataSetCF} setDataSet={setDataSetCF} lineColor={lineColorCF} setRandomColor={updateCFColor} />
        </div>
    );
};

