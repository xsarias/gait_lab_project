import gymnasium as gym
from gymnasium import spaces
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

# Inverted pendulum algorithm integrated
class InvertedPendulum:
    def __init__(self, g=9.81, L=1.0, m=1.0, dt=0.02):
        self.g = g
        self.L = L
        self.m = m
        self.dt = dt
        self.reset()

    def reset(self):
        self.theta = np.random.uniform(-0.2, 0.2)
        self.theta_dot = 0.0
        return np.array([self.theta, self.theta_dot], dtype=np.float32)

    def step(self, torque):
        theta_ddot = - (self.g / self.L) * np.sin(self.theta) + (torque / (self.m * self.L**2))
        self.theta_dot += theta_ddot * self.dt
        self.theta += self.theta_dot * self.dt
        self.theta = np.clip(self.theta, -np.pi/2, np.pi/2)
        self.theta_dot = np.clip(self.theta_dot, -10, 10)
        return np.array([self.theta, self.theta_dot], dtype=np.float32)

# Custom Gym environment combining gait data and inverted pendulum
class GaitEnv(gym.Env):
    def __init__(self, data_file="Data/gait_lab_dataset.csv", train=True, test_size=0.2):
        super(GaitEnv, self).__init__()

        df = pd.read_csv(data_file)

        df["PreInjuries"] = df["PreInjuries"].fillna("Unknown")
        df["MedicalHistory"] = df["MedicalHistory"].fillna("Unknown")
        df["FatigueLevel"] = df["FatigueLevel"].fillna("Unknown")
        df["Recommendation"] = df["Recommendation"].fillna("Unknown")

        self.actions_list = df["Recommendation"].unique().tolist()
        self.action_space = spaces.Discrete(len(self.actions_list))

        self.numeric_features = [
            "Age", "Height", "Weight", "EnergyExpenditure", "Force", "Moment",
            "EMG", "ElectricPotential", "GaitSpeed", "StepFrequency", "KneeAngle", "PelvicDeviation"
        ]
        self.categorical_features = ["PreInjuries", "MedicalHistory", "FatigueLevel"]

        df[self.numeric_features] = df[self.numeric_features].apply(lambda col: col.fillna(col.mean()))
        df[self.categorical_features] = df[self.categorical_features].fillna("Unknown")

        features = df[self.numeric_features + self.categorical_features]
        labels = df["Recommendation"]

        features_train, features_eval, labels_train, labels_eval = train_test_split(
            features, labels, test_size=test_size, random_state=42, stratify=labels
        )

        if train:
            self.df = features_train.copy()
            self.df["Recommendation"] = labels_train.values
        else:
            print("Train with eval")
            self.df = features_eval.copy()
            self.df["Recommendation"] = labels_eval.values

        self.preprocessor = ColumnTransformer([
            ("num", MinMaxScaler(), self.numeric_features),
            ("cat", OneHotEncoder(handle_unknown="ignore", sparse_output=False), self.categorical_features)
        ])

        self.processed_features = self.preprocessor.fit_transform(self.df[self.numeric_features + self.categorical_features])

        obs_dim = self.processed_features.shape[1] + 2
        low = np.concatenate([np.zeros(self.processed_features.shape[1], dtype=np.float32), [-np.pi/2, -10]])
        high = np.concatenate([np.ones(self.processed_features.shape[1], dtype=np.float32), [np.pi/2, 10]])

        self.observation_space = spaces.Box(low=low, high=high, dtype=np.float32)

        self.pendulum = InvertedPendulum()
        self.current_index = 0
        self.rewards = []
        self.correct_flags = []

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        self.current_index = np.random.randint(0, len(self.df))
        obs_patient = self.processed_features[self.current_index].astype(np.float32)
        obs_pendulum = self.pendulum.reset()
        return np.concatenate([obs_patient, obs_pendulum]), {}

    def step(self, action):
        row = self.df.iloc[self.current_index]
        obs_patient = self.processed_features[self.current_index].astype(np.float32)

        torque = (action - len(self.actions_list)//2) * 2
        obs_pendulum = self.pendulum.step(torque)

        correct_action = self.actions_list.index(row["Recommendation"])
        reward = 1.0 if action == correct_action else -0.1

        terminated = True
        truncated = False
        info = {"correct": action == correct_action}

        self.current_index = (self.current_index + 1) % len(self.df)
        obs = np.concatenate([obs_patient, obs_pendulum])

        self.rewards.append(reward)
        self.correct_flags.append(info["correct"])

        return obs, reward, terminated, truncated, info

    def render(self):
        pass

    def evaluate_agent(self, model):
        self.rewards = []
        self.correct_flags = []
        correct_predictions = 0
        total_patients = len(self.df)

        for i in range(total_patients):
            obs, _ = self.reset()
            action, _ = model.predict(obs, deterministic=True)
            _, reward, _, _, info = self.step(action)

            print(f"Patient {i} | Action: {action} | Correct: {info['correct']} | Reward: {reward}")

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
