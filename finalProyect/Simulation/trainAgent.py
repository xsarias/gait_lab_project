from stable_baselines3 import DQN
from stable_baselines3.common.env_checker import check_env
from gaitLabEnv import GaitEnv 

# 1. Create the training environment using only patient data
train_env = GaitEnv(train=True, use_dof_model=True)

# 2. Check environment compatibility
check_env(train_env)

# 3. Train the DQN model
model = DQN(
    "MlpPolicy",
    train_env,
    verbose=1,
    learning_rate=0.001,
    buffer_size=10000,
    learning_starts=1000
)

model.learn(total_timesteps=50000)

# 4. Save the trained model
model.save("Models/gaitlab_dqn_model")

# 5. Evaluate the agent using test patients
print("\n📊 Evaluating the model with test patients...")
eval_env = GaitEnv(train=False, use_dof_model=True)
eval_env.evaluate_agent(model)
