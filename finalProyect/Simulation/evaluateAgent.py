import pandas as pd
from stable_baselines3 import DQN
from gaitLabEnv import GaitEnv
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score, precision_score, recall_score, f1_score
import matplotlib.pyplot as plt
import seaborn as sns

# Load the trained model
model = DQN.load("Models/gaitlab_dqn_model")

# Create the evaluation environment using 20% of the dataset
env = GaitEnv(train=False, use_dof_model=True)

true_labels = []
pred_labels = []

print("\n📊 Evaluating model on test patients...\n")
for i in range(len(env.df)):
    obs, _ = env.reset()
    action, _ = model.predict(obs, deterministic=True)
    pred = env.actions_list[action]
    true = env.df.iloc[env.current_index]["Recommendation"]
    pred_labels.append(pred)
    true_labels.append(true)
    print(f"🧍 Patient {i+1}: True → {true} | Predicted → {pred}")


# Save predictions to a CSV file
df_result = env.df.copy()
df_result["PredictedRecommendation"] = pred_labels
df_result.to_csv("Data/test_predictions.csv", index=False)
print("\n✅ Predictions saved to Data/test_predictions.csv")

# Print classification report
print("\n📋 Classification Report:")
print(classification_report(true_labels, pred_labels))

# Compute evaluation metrics
acc = accuracy_score(true_labels, pred_labels)
prec = precision_score(true_labels, pred_labels, average='weighted', zero_division=0)
rec = recall_score(true_labels, pred_labels, average='weighted', zero_division=0)
f1 = f1_score(true_labels, pred_labels, average='weighted', zero_division=0)

print(f"\n✅ Accuracy:  {acc:.2f}")
print(f"📐 Precision: {prec:.2f}")
print(f"📈 Recall:    {rec:.2f}")
print(f"🏆 F1 Score:  {f1:.2f}")

# Plot the confusion matrix
cm = confusion_matrix(true_labels, pred_labels, labels=env.actions_list)
plt.figure(figsize=(8, 6))
sns.heatmap(cm, annot=True, fmt="d", cmap="Blues",
            xticklabels=env.actions_list, yticklabels=env.actions_list)
plt.xlabel("Predicted")
plt.ylabel("True")
plt.title("Confusion Matrix")
plt.tight_layout()
plt.show()

env.evaluate_agent(model)