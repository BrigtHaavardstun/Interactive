import React from "react";
import "./styles.css";
import { ParentComponent } from "./ParentComponent";
import 'bootstrap/dist/css/bootstrap.min.css';


export default () => {
  return (
    <div className="App">
      <h1>Interactive Chart, with python backend Demo</h1>
      <h2>By: Brigt</h2>
      <h10>Credit: based on https://github.com/sheykholeslam/React-Draggable-Chart-Example/tree/master</h10>
      <ParentComponent />
    </div>
  );
};