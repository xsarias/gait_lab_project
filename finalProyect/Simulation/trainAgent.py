from stable_baselines3 import DQN
from stable_baselines3.common.env_checker import check_env
from gaitLabEnv import GaitEnv

# 1. Create the training environment with training data
train_env = GaitEnv(train=True)

# 2. Check environment compatibility
check_env(train_env)

# 3. Train the DQN model
model = DQN("MlpPolicy", train_env, verbose=1, learning_rate=0.001, buffer_size=10000, learning_starts=1000)
model.learn(total_timesteps=50000)

# 4. Save the trained model
model.save("gaitlab_dqn_model")

# 5. Evaluate the model using test data
print("\n📊 Evaluating the model with training patients...")
eval_env = GaitEnv(train=False)
eval_env.evaluate_agent(model)
