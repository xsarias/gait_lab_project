import gymnasium as gym
from gymnasium import spaces
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
from stable_baselines3 import DQN

# Multi-DOF leg model for gait simulation
class MultiDOFLeg:
    def __init__(self, dt=0.02):
        self.dt = dt
        self.reset()

    def reset(self):
        self.state = np.array([
            np.random.uniform(-0.2, 0.2), 0.0,
            np.random.uniform(-0.1, 0.1), 0.0,
            np.random.uniform(-0.1, 0.1), 0.0
        ], dtype=np.float32)
        return self.state

    def step(self, torques):
        hip_torque, knee_torque, ankle_torque = torques
        I = 1.0
        hip_acc = hip_torque / I
        knee_acc = knee_torque / I
        ankle_acc = ankle_torque / I

        self.state[1] += hip_acc * self.dt
        self.state[0] += self.state[1] * self.dt

        self.state[3] += knee_acc * self.dt
        self.state[2] += self.state[3] * self.dt

        self.state[5] += ankle_acc * self.dt
        self.state[4] += self.state[5] * self.dt

        return self.state

class GaitEnv(gym.Env):
    def __init__(self, data_file="Data/gait_lab_dataset.csv", train=True, test_size=0.2, use_dof_model=False):
        super(GaitEnv, self).__init__()
        self.use_dof_model = use_dof_model

        df = pd.read_csv(data_file)
        df.fillna("Unknown", inplace=True)

        if "Recommendation" in df.columns:
            self.actions_list = df["Recommendation"].unique().tolist()
        else:
            self.actions_list = ["Improve posture", "Increase cadence", "Enhance muscle strength", "Adjust foot strike"]

        self.action_space = spaces.Discrete(len(self.actions_list))

        self.numeric_features = [
            "Age", "Height", "Weight", "EnergyExpenditure", "Force", "Moment",
            "EMG", "ElectricPotential", "GaitSpeed", "StepFrequency", "KneeAngle", "PelvicDeviation"
        ]
        self.categorical_features = ["PreInjuries", "MedicalHistory", "FatigueLevel"]

        df[self.numeric_features] = df[self.numeric_features].apply(lambda col: col.fillna(col.mean()))

        features = df[self.numeric_features + self.categorical_features]

        if "Recommendation" in df.columns:
            labels = df["Recommendation"]
            features_train, features_eval, labels_train, labels_eval = train_test_split(
                features, labels, test_size=test_size, random_state=42, stratify=labels
            )
            self.df = features_train.copy() if train else features_eval.copy()
            self.df["Recommendation"] = labels_train.values if train else labels_eval.values
        else:
            self.df = features.copy()

        self.preprocessor = ColumnTransformer([
            ("num", MinMaxScaler(), self.numeric_features),
            ("cat", OneHotEncoder(handle_unknown="ignore", sparse_output=False), self.categorical_features)
        ])

        self.processed_features = self.preprocessor.fit_transform(
            self.df[self.numeric_features + self.categorical_features]
        )

        if self.use_dof_model:
            obs_dim = self.processed_features.shape[1] + 6
            low = np.concatenate([np.zeros(self.processed_features.shape[1]), -np.ones(6)])
            high = np.concatenate([np.ones(self.processed_features.shape[1]), np.ones(6)])
        else:
            obs_dim = self.processed_features.shape[1]
            low = np.zeros(obs_dim)
            high = np.ones(obs_dim)

        self.observation_space = spaces.Box(low=low, high=high, dtype=np.float32)
        self.leg_model = MultiDOFLeg() if self.use_dof_model else None

        self.current_index = 0
        self.rewards = []
        self.correct_flags = []

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        self.current_index = np.random.randint(0, len(self.df))
        obs_patient = self.processed_features[self.current_index].astype(np.float32)

        if self.use_dof_model:
            obs_leg = self.leg_model.reset()
            return np.concatenate([obs_patient, obs_leg]), {}
        else:
            return obs_patient, {}

    def step(self, action):
        row = self.df.iloc[self.current_index]
        obs_patient = self.processed_features[self.current_index].astype(np.float32)

        if self.use_dof_model:
            torque_vector = np.array([action - 1, action - 1, action - 1], dtype=np.float32)
            obs_leg = self.leg_model.step(torque_vector)
            obs = np.concatenate([obs_patient, obs_leg])
        else:
            obs = obs_patient

        
        if "Recommendation" in self.df.columns:
            correct_action = self.actions_list.index(row["Recommendation"])
            reward = 1.0 if action == correct_action else -0.1
            info = {"correct": action == correct_action}
        else:
            correct_action = -1
            reward = 0.0  # No way to evaluate correctness
            info = {"correct": False}

        terminated = True
        truncated = False
        info = {"correct": action == correct_action} if correct_action != -1 else {"correct": False}

        self.current_index = (self.current_index + 1) % len(self.df)
        self.rewards.append(reward)
        self.correct_flags.append(info["correct"])

        return obs, reward, terminated, truncated, info

    def evaluate_agent(self, model):
        self.rewards = []
        self.correct_flags = []
        correct_predictions = 0
        total_patients = len(self.df)

        for i in range(total_patients):
            obs, _ = self.reset()
            action, _ = model.predict(obs, deterministic=True)
            _, reward, _, _, info = self.step(action)
            if info["correct"]:
                correct_predictions += 1

        accuracy = correct_predictions / total_patients
        print(f"\n✅ Final accuracy on all patients: {accuracy * 100:.2f}%")

        plt.figure(figsize=(12, 5))
        plt.subplot(1, 2, 1)
        labels = ['Correct', 'Incorrect']
        values = [sum(self.correct_flags), len(self.correct_flags) - sum(self.correct_flags)]
        plt.bar(labels, values, color=['green', 'red'])
        plt.title("Model Predictions")
        plt.ylabel("Number of Patients")

        plt.subplot(1, 2, 2)
        plt.plot(self.rewards, marker='o')
        plt.title("Reward per Patient")
        plt.xlabel("Patient Index")
        plt.ylabel("Reward")
        plt.tight_layout()
        plt.show()

# --- Simulate patients and save predictions ---

if __name__ == "__main__":
    model = DQN.load("Models/gaitlab_dqn_model")
    sim_env = GaitEnv(data_file="Data/simulated_patients.csv", train=False, use_dof_model=True)

    predictions = []
    print("\n🦿 Simulating new patients and predicting recommendations...\n")
    for i in range(len(sim_env.df)):
        obs, _ = sim_env.reset()
        action, _ = model.predict(obs, deterministic=True)
        recommended_label = sim_env.actions_list[action]
        print(f"🧍 Patient {i+1}: Recommended Action → {recommended_label}")
        predictions.append(recommended_label)

    # Save predictions to new CSV file
    result_df = sim_env.df.copy()
    result_df["PredictedRecommendation"] = predictions
    result_df.to_csv("Data/simulated_predictions.csv", index=False)
    print("\n📁 Saved predictions to Data/simulated_predictions.csv")
