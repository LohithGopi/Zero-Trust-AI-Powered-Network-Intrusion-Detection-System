import re

file_path = r"E:\ML\frontend\src\pages\dashboard\ModelDetailsView.jsx"
with open(file_path, "r", encoding="utf-8") as f:
    text = f.read()

# Replace condition lines 193-200
old_cond = """  // Strict Requirement: Performance evaluation takes place ONLY after live detection of 2 or more models

  const canEvaluatePerformance = distinctLiveModelsCount >= 2;

  const hasLiveData = !!(liveReport && liveReport.has_data && liveReport.total_flows > 0 && canEvaluatePerformance);

  const shouldShowMetrics = canEvaluatePerformance;"""

new_cond = """  // Performance evaluation is active as soon as live detection traffic exists or a trained model is ready
  const hasLiveData = !!(liveReport && liveReport.has_data && liveReport.total_flows > 0);
  const canEvaluatePerformance = hasLiveData || distinctLiveModelsCount >= 1 || isTrained;
  const shouldShowMetrics = canEvaluatePerformance;"""

# Replace badge lines 298-304
old_badge = """              {canEvaluatePerformance

                ? `✓ Verified Live Telemetry (${distinctLiveModelsCount} Models Evaluated)`

                : `⚠️ ${distinctLiveModelsCount}/2 Models Evaluated Live (Evaluation Locked)`}"""

new_badge = """              {hasLiveData
                ? `✓ Verified Live Telemetry (${(liveReport?.total_flows || 0).toLocaleString()} Flows Evaluated)`
                : (canEvaluatePerformance
                    ? `✓ Offline Model Benchmark (${evalData.model_name || 'Trained Model'})`
                    : 'Awaiting Live Detection')}"""

old_cond_norm = old_cond.replace("\r\n", "\n")
new_cond_norm = new_cond.replace("\r\n", "\n")
text_norm = text.replace("\r\n", "\n")

# Use regex for safe replacement
text_norm = re.sub(
    r'// Strict Requirement: Performance evaluation takes place ONLY after live detection of 2 or more models\s*\n\s*const canEvaluatePerformance = distinctLiveModelsCount >= 2;\s*\n\s*const hasLiveData = !!\(liveReport && liveReport\.has_data && liveReport\.total_flows > 0 && canEvaluatePerformance\);\s*\n\s*const shouldShowMetrics = canEvaluatePerformance;',
    new_cond_norm,
    text_norm
)

text_norm = re.sub(
    r'\{canEvaluatePerformance\s*\n\s*\?\s*`[^`]*Verified Live Telemetry[^`]*`\s*\n\s*:\s*`[^`]*Models Evaluated Live[^`]*`\}',
    new_badge,
    text_norm
)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(text_norm)

print("SUCCESS: ModelDetailsView.jsx updated to unlock live detection immediately.")
