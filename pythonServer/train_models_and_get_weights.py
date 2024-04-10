from Blackbox_classifier_FCN.functionBased.Train_model import train_model, convert_to_keras




if __name__ == '__main__':

    dataSets = ["Chinatown","Charging", "ItalyPowerDemand"]
    for dataSet in dataSets:
        train_model(dataSet,epochs=2000)
        #convert_to_lite(dataSet)
        convert_to_keras(dataSet)

    