import os

# 1. Update LiveDetectionView.jsx
live_view_file = r"E:\ML\frontend\src\pages\dashboard\LiveDetectionView.jsx"
with open(live_view_file, "r", encoding="utf-8") as f:
    code = f.read()

# Add packetBoundary state
old_state = "const [csvFlowCount, setCsvFlowCount] = useState(50);"
new_state = """const [csvFlowCount, setCsvFlowCount] = useState(50);
  const [packetBoundary, setPacketBoundary] = useState(500);"""

if old_state in code:
    code = code.replace(old_state, new_state)
    print("Added packetBoundary state to LiveDetectionView.jsx")
else:
    print("Warning: old_state not matched")

# Update handleStartCapture payload
old_payload = """        mode: captureMode === 'simulated' ? 'simulated' : 'realtime'
      };"""

new_payload = """        mode: captureMode === 'simulated' ? 'simulated' : 'realtime',
        packet_boundary: packetBoundary ? Number(packetBoundary) : null
      };"""

if old_payload in code:
    code = code.replace(old_payload, new_payload)
    print("Updated handleStartCapture payload in LiveDetectionView.jsx")
else:
    print("Warning: old_payload not matched")

# Add Target Boundary dropdown right before Start Live Detection button
old_button_group = """          {isRunning ? (
            <button
              onClick={() => handleStopCapture()}
              disabled={loading}
              className="flex items-center space-x-1.5 px-4 py-2 rounded-xl text-xs font-bold text-white bg-rose-600 hover:bg-rose-700 shadow-sm transition-all cursor-pointer animate-pulse"
            >"""

new_button_group = """          {/* Target Capture Boundary Selector */}
          <div className="flex items-center space-x-1.5 text-xs bg-slate-100 border border-slate-300 rounded-xl px-2.5 py-1.5 shadow-2xs">
            <span className="text-[10px] font-bold text-slate-600 uppercase tracking-wider">Boundary:</span>
            <select
              value={packetBoundary || ''}
              disabled={isRunning}
              onChange={(e) => setPacketBoundary(e.target.value ? Number(e.target.value) : null)}
              className="bg-transparent text-xs font-mono font-bold text-purple-700 cursor-pointer focus:outline-hidden"
            >
              <option value={500}>500 Flows/Pkts</option>
              <option value={1000}>1,000 Flows/Pkts</option>
              <option value={2500}>2,500 Flows/Pkts</option>
              <option value={5000}>5,000 Flows/Pkts</option>
              <option value={10000}>10,000 Flows/Pkts</option>
              <option value={25000}>25,000 Flows/Pkts</option>
              <option value={50000}>50,000 Flows/Pkts</option>
              <option value="">Continuous</option>
            </select>
          </div>

          {isRunning ? (
            <button
              onClick={() => handleStopCapture()}
              disabled={loading}
              className="flex items-center space-x-1.5 px-4 py-2 rounded-xl text-xs font-bold text-white bg-rose-600 hover:bg-rose-700 shadow-sm transition-all cursor-pointer animate-pulse"
            >"""

if old_button_group in code:
    code = code.replace(old_button_group, new_button_group)
    print("Added Boundary selector before Start button in LiveDetectionView.jsx")
else:
    print("Warning: old_button_group not matched")

with open(live_view_file, "w", encoding="utf-8") as f:
    f.write(code)

# 2. Update ModelDetailsView.jsx
model_details_file = r"E:\ML\frontend\src\pages\dashboard\ModelDetailsView.jsx"
with open(model_details_file, "r", encoding="utf-8") as f:
    m_code = f.read()

old_flows_display = """              <div className="text-lg font-black text-slate-900 font-mono">
                {(liveReport.total_flows || evalFlowLimit).toLocaleString()}
              </div>
              <div className="text-[10px] text-slate-500 font-mono">
                {(liveReport.total_packets || (evalFlowLimit * 8)).toLocaleString()} pkts ({(((liveReport.total_bytes || (evalFlowLimit * 3780))) / 1024).toFixed(1)} KB)
              </div>"""

new_flows_display = """              <div className="text-lg font-black text-slate-900 font-mono flex items-baseline space-x-1.5">
                <span>{(liveReport.total_flows || 0).toLocaleString()}</span>
                {liveReport.requested_boundary && liveReport.total_flows < liveReport.requested_boundary && (
                  <span className="text-[10px] text-amber-600 font-sans font-bold">
                    (of {liveReport.requested_boundary.toLocaleString()} boundary)
                  </span>
                )}
              </div>
              <div className="text-[10px] text-slate-500 font-mono">
                {(liveReport.total_packets || 0).toLocaleString()} pkts ({(((liveReport.total_bytes || 0)) / 1024).toFixed(1)} KB)
              </div>"""

if old_flows_display in m_code:
    m_code = m_code.replace(old_flows_display, new_flows_display)
    print("Updated empirical live flows display in ModelDetailsView.jsx")
else:
    print("Warning: old_flows_display not matched")

with open(model_details_file, "w", encoding="utf-8") as f:
    f.write(m_code)

print("UI updates complete.")
