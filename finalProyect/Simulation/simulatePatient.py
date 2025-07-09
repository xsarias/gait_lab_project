from stable_baselines3 import DQN
from gaitLabEnv import GaitEnv

# Load trained model
model = DQN.load("Models/gaitlab_dqn_model")

# Create environment with simulated patient data
env = GaitEnv(data_file="Data/simulated_patients.csv", train=False, use_dof_model=True)

# Predict recommendation for each simulated patient
print("\n📢 Predicted Recommendations for Simulated Patients:")
for i in range(len(env.df)):
    obs, _ = env.reset()
    action, _ = model.predict(obs, deterministic=True)
    recommended = env.actions_list[action]
    print(f"🧍 Patient {i+1}: {recommended}")

