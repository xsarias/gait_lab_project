# --- Heuristic Evaluator for sanity check ---
import pandas as pd

result_df = pd.read_csv("Data/simulated_patients.csv")
print(result_df.head())

print("\n🔎 Evaluating predictions with heuristic rules...")

def heuristic_recommendation(row):
    if row["Force"] < 0.3 or row["EMG"] < 0.3:
        return "Enhance muscle strength"
    elif row["KneeAngle"] > 0.7 or row["PelvicDeviation"] > 0.6:
        return "Improve posture"
    elif row["StepFrequency"] < 0.4:
        return "Increase cadence"
    elif row["GaitSpeed"] > 0.8 and row["FatigueLevel"] == "High":
        return "Adjust foot strike"
    else:
        return "Improve posture"  # default rule

result_df["HeuristicRecommendation"] = result_df.apply(heuristic_recommendation, axis=1)
result_df["Agreement"] = result_df["Recommendation"] == result_df["HeuristicRecommendation"]

accuracy = result_df["Agreement"].mean()
print(f"🤖 Agreement with heuristic rules: {accuracy * 100:.2f}%")

# Optional: save with heuristics
result_df.to_csv("Data/simulated_predictions_with_heuristics.csv", index=False)
print("📁 Saved with heuristic labels → Data/simulated_predictions_with_heuristics.csv  ||| ")
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
import matplotlib.pyplot as plt

# Cargar columnas relevantes
y_true = result_df["HeuristicRecommendation"]
y_pred = result_df["Recommendation"]

# Crear matriz de confusión
cm = confusion_matrix(y_true, y_pred, labels=sorted(result_df["HeuristicRecommendation"].unique()))
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=sorted(result_df["HeuristicRecommendation"].unique()))

# Mostrar
plt.figure(figsize=(8, 6))
disp.plot(cmap="Blues", xticks_rotation=45)
plt.title("Matriz de Confusión: Modelo vs. Heurística")
plt.tight_layout()
plt.show()