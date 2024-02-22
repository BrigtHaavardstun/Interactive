import ProgressBar from "@ramonak/react-progress-bar";

const BasicExample = ({currValue})=> {
  return <div>
    <ProgressBar completed={currValue} customLabel={"Model confidence of current class: " + currValue.toString() + "%"}/>
  </div>
}

export default BasicExample