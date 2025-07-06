import pandas as pd

class GaitlabAgent:
    def __init__(self):
        pass

    def run(self):
        self.load_data()
        self.define_features()

    def load_data(self):
        '''This method is to load gaitLab data.'''
        self.gldata = pd.read_csv('gait_lab_dataset.csv')
        print(self.gldata.head())

    def define_features(self):
        features = self.gldata[[
        "ID",
        "Age",
        "Height",
        "Weight",
        "EnergyExpenditure",
        "PreInjuries",
        "MedicalHistory",
        "FatigueLevel",
        "Force",
        "Moment",
        "EMG",
        "ElectricPotential",
        "GaitSpeed",
        "StepFrequency",
        "KneeAngle",
        "PelvicDeviation"
    ]]
        print(features.head())
        features.to_csv("features.csv", index=False)

sim = GaitlabAgent()
sim.run()   
