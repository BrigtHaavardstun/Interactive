import ProgressBar from "@ramonak/react-progress-bar";

const BasicExample = ({currValue})=> {
  return <div>
    <h2> Model confidence of current class</h2>
    <ProgressBar completed={currValue}/>
  </div>
}

export default BasicExample