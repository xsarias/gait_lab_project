from gaitLabEnv import GaitEnv
import pandas as pd

env = GaitEnv(data_file="Data/gait_lab_dataset.csv", train=True, use_dof_model=True)


simulated_df = env.df.copy()
simulated_df.to_csv("Data/simulated_patients.csv", index=False)
