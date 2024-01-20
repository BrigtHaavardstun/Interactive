import React, { useState } from 'react';
import DraggableGraph from './DraggableData';
import axios from 'axios';


export const ParentComponent = () => {
    const [lineColor, setLineColor] = useState('green');
    const [dataSet, setDataSet] = useState([
        [65, 59, 80, 81, 56, 55, 40],
        [35, 39, 50, 91, 46, 85, 10],
    ]);

    console.log("Test dataset", dataSet);
    const setColorColor = () => {  // Receive setLineColor as a prop
        axios.get('http://localhost:8765/random', {
            params: {
                dataSet: JSON.stringify(dataSet)  // Convert dataSet to a JSON string
            }
        })
            .then((res) => {
                // Change the color based on the response

                if (res.data == 1) {
                    setLineColor("green");
                }
                else {
                    setLineColor("red")
                }

            })
            .catch((error) => {
                console.error('Error:', error);
            });
    };
    setColorColor();

    return (
        <div>
            <DraggableGraph dataSetOrg={dataSet} setDataSet={setDataSet} lineColor={lineColor} setRandomColor={setColorColor} />
        </div>
    );
};

