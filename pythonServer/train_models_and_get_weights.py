from Blackbox_classifier_FCN.functionBased.Train_model import train_model, convert_to_lite
from Class_Activation_Mapping.functionBased.CAM_weights import training_weights_cam,test_weights_cam, joint_weights_cam




if __name__ == '__main__':

    dataSets = ["Chinatown", "ItalyPowerDemand", "Charging"]
    for dataSet in dataSets:
        train_model(dataSet,epochs=2000)
        convert_to_lite(dataSet)
        training_weights_cam(dataSet)
        test_weights_cam(dataSet)
        joint_weights_cam(dataSet)
    