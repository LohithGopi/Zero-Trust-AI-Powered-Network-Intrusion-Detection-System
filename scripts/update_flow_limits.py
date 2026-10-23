import os

# 1. Update CompareView.jsx
compare_file = r"E:\ML\frontend\src\pages\dashboard\CompareView.jsx"
with open(compare_file, "r", encoding="utf-8") as f:
    text = f.read()

# Replace testSamplesLimit options
old_benchmark_opts = """                    <option value={500}>500 test records</option>
                    <option value={1000}>1,000 test records</option>
                    <option value={2500}>2,500 test records</option>
                    <option value={5000}>5,000 test records</option>"""

new_benchmark_opts = """                    <option value={500}>500 test records</option>
                    <option value={1000}>1,000 test records</option>
                    <option value={2500}>2,500 test records</option>
                    <option value={5000}>5,000 test records</option>
                    <option value={10000}>10,000 test records</option>
                    <option value={25000}>25,000 test records</option>
                    <option value={50000}>50,000 test records</option>"""

old_live_opts = """                    <option value={25}>25 recent live flows</option>
                    <option value={50}>50 recent live flows</option>
                    <option value={100}>100 recent live flows</option>
                    <option value={200}>200 recent live flows</option>"""

new_live_opts = """                    <option value={500}>500 recent live flows</option>
                    <option value={1000}>1,000 recent live flows</option>
                    <option value={2500}>2,500 recent live flows</option>
                    <option value={5000}>5,000 recent live flows</option>
                    <option value={10000}>10,000 recent live flows</option>
                    <option value={25000}>25,000 recent live flows</option>
                    <option value={50000}>50,000 recent live flows</option>"""

if old_benchmark_opts in text:
    text = text.replace(old_benchmark_opts, new_benchmark_opts)
    print("CompareView benchmark options updated!")
else:
    print("Warning: old_benchmark_opts not matched")

if old_live_opts in text:
    text = text.replace(old_live_opts, new_live_opts)
    print("CompareView live options updated!")
else:
    print("Warning: old_live_opts not matched")

with open(compare_file, "w", encoding="utf-8") as f:
    f.write(text)

# 2. Update LiveDetectionView.jsx
live_det_file = r"E:\ML\frontend\src\pages\dashboard\LiveDetectionView.jsx"
with open(live_det_file, "r", encoding="utf-8") as f:
    live_text = f.read()

old_csv_opts = """                    <option value={25}>25 Flows</option>
                    <option value={50}>50 Flows</option>
                    <option value={100}>100 Flows</option>
                    <option value={200}>200 Flows</option>
                    <option value={500}>500 Flows (Max Sliding Window)</option>"""

new_csv_opts = """                    <option value={500}>500 Flows</option>
                    <option value={1000}>1,000 Flows</option>
                    <option value={2500}>2,500 Flows</option>
                    <option value={5000}>5,000 Flows</option>
                    <option value={10000}>10,000 Flows</option>
                    <option value={25000}>25,000 Flows</option>
                    <option value={50000}>50,000 Flows</option>"""

if old_csv_opts in live_text:
    live_text = live_text.replace(old_csv_opts, new_csv_opts)
    print("LiveDetectionView CSV flow options updated!")
else:
    print("Warning: old_csv_opts not matched")

with open(live_det_file, "w", encoding="utf-8") as f:
    f.write(live_text)

print("Flow limits update script finished.")
