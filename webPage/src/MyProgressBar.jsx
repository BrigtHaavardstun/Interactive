import ProgressBar from "@ramonak/react-progress-bar";

const BasicExample = ({ currValue }) => {
  return <div>
    <ProgressBar completed={currValue} customLabel={"AI confidence of Current class: " + currValue.toString() + "%"} />
  </div>
}

export default BasicExample