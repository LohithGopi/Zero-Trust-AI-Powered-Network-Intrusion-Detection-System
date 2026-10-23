import re

file_path = r"E:\ML\frontend\src\pages\dashboard\ModelDetailsView.jsx"
with open(file_path, "r", encoding="utf-8") as f:
    text = f.read()

text = re.sub(r'false_positive_rate:\s*0\.0184', 'false_positive_rate: 0.0142', text)
text = re.sub(r'accuracy:\s*0\.9681', 'accuracy: 0.9685', text)
text = re.sub(r'precision:\s*0\.9694', 'precision: 0.9710', text)
text = re.sub(r'recall:\s*0\.9681', 'recall: 0.9669', text)
text = re.sub(r'f1_score:\s*0\.9685', 'f1_score: 0.9689', text)
text = re.sub(r'normal_identification_rate:\s*0\.9816', 'normal_identification_rate: 0.9858', text)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(text)

print("SUCCESS: ModelDetailsView.jsx regex update applied.")
