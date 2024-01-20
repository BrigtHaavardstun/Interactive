import React, { useEffect, useState } from 'react';
import axios from 'axios';

export const Swr = () => {
    const [response, setResponse] = useState(null);

    useEffect(() => {
        const ys = [1, 2, 3, 4, 5]; // Your list of numbers
        const params = new URLSearchParams({ ys: JSON.stringify(ys) });

        axios.get('http://localhost:8765?' + params.toString())
            .then((res) => {
                setResponse(res.data);
            })
            .catch((error) => {
                console.error('Error:', error);
            });
    }, []);

    return (
        <div>
            <p>Response from server: {response}</p>
        </div>
    );
};


export const SwrRandom = ({ setLineColor }) => {  // Receive setLineColor as a prop
    useEffect(() => {
        axios.get('http://localhost:8765/random')
            .then((res) => {
                // Change the color based on the response
                if (res.data > 50) {
                    setLineColor('green');
                } else {
                    setLineColor('red');
                }
            })
            .catch((error) => {
                console.error('Error:', error);
            });
    }, []);

    // No need to return anything as this component is only used for the side effect
};
