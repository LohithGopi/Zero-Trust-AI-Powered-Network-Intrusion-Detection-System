live_det_file = r"E:\ML\frontend\src\pages\dashboard\LiveDetectionView.jsx"
with open(live_det_file, "r", encoding="utf-8") as f:
    live_text = f.read()

target_str = """                <select
                  value={csvFlowCount}
                  disabled={isIngestingCsv}
                  onChange={(e) => setCsvFlowCount(Number(e.target.value))}
                  className="w-full bg-slate-50 border border-slate-200 rounded-lg p-1.5 text-xs text-slate-800"
                >
                  <option value={25}>25 Flows</option>
                  <option value={50}>50 Flows</option>
                  <option value={100}>100 Flows</option>
                  <option value={200}>200 Flows</option>
                  <option value={500}>500 Flows (Max Sliding Window)</option>
                </select>"""

replacement_str = """                <select
                  value={csvFlowCount}
                  disabled={isIngestingCsv}
                  onChange={(e) => setCsvFlowCount(Number(e.target.value))}
                  className="w-full bg-slate-50 border border-slate-200 rounded-lg p-1.5 text-xs text-slate-800 font-mono"
                >
                  <option value={500}>500 Flows</option>
                  <option value={1000}>1,000 Flows</option>
                  <option value={2500}>2,500 Flows</option>
                  <option value={5000}>5,000 Flows</option>
                  <option value={10000}>10,000 Flows</option>
                  <option value={25000}>25,000 Flows</option>
                  <option value={50000}>50,000 Flows</option>
                </select>"""

if target_str in live_text:
    live_text = live_text.replace(target_str, replacement_str)
    with open(live_det_file, "w", encoding="utf-8") as f:
        f.write(live_text)
    print("LiveDetectionView successfully updated with all tiers (500 to 50,000)!")
else:
    print("Target string still not matched")
