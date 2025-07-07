from stable_baselines3 import DQN
from gaitLabEnv import GaitEnv

# 1. Load the trained model
model = DQN.load("gaitlab_dqn_model")

# 2. Create the test environment
eval_env = GaitEnv(train=False)

# 3. Evaluate the agent on test data
print("\n📊 Evaluating the model with test patients...")
eval_env.evaluate_agent(model)
