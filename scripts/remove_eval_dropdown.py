import re

# 1. Update ModelDetailsView.jsx
model_details_path = r"E:\ML\frontend\src\pages\dashboard\ModelDetailsView.jsx"
with open(model_details_path, "r", encoding="utf-8") as f:
    content = f.read()

# Replace state and fetch function
old_state_block = """  const [evalSource, setEvalSource] = useState('live'); // 'live' (default) or 'training'
  const [showSummaryModal, setShowSummaryModal] = useState(false);
  const [evalFlowLimit, setEvalFlowLimit] = useState(500);
  const [liveReport, setLiveReport] = useState(null);
  const [trainingReport, setTrainingReport] = useState(null);
  const [loadingReport, setLoadingReport] = useState(false);

  const { user, role, modelStatus, modelMetrics, trainingProgress, activeDataset } = useAuth();
  const isTrained = modelStatus === 'Trained' || (trainingReport && typeof trainingReport.accuracy === 'number');
  const isTraining = modelStatus === 'Training' || modelStatus === 'Preprocessing' || (trainingProgress && trainingProgress.isTraining);

  const fetchEvaluationReports = async (limitOverride = null) => {
    setLoadingReport(true);
    const currentLimit = limitOverride || evalFlowLimit;
    try {
      const [liveRes, trainRes] = await Promise.allSettled([
        apiGetLiveEvaluation(currentLimit),
        apiGetModelReport()
      ]);

      if (liveRes.status === 'fulfilled' && liveRes.value) {
        setLiveReport(liveRes.value);
      }
      if (trainRes.status === 'fulfilled' && trainRes.value && typeof trainRes.value.accuracy === 'number') {
        setTrainingReport(trainRes.value);
      } else {
        setTrainingReport(null);
      }
    } catch (err) {
      console.error('Failed to load performance evaluations:', err);
      setTrainingReport(null);
    } finally {
      setLoadingReport(false);
    }
  };

  const handleFlowLimitChange = (newLimit) => {
    setEvalFlowLimit(newLimit);
    fetchEvaluationReports(newLimit);
  };"""

new_state_block = """  const [evalSource, setEvalSource] = useState('live'); // 'live' (default) or 'training'
  const [showSummaryModal, setShowSummaryModal] = useState(false);
  const [liveReport, setLiveReport] = useState(null);
  const [trainingReport, setTrainingReport] = useState(null);
  const [loadingReport, setLoadingReport] = useState(false);

  const { user, role, modelStatus, modelMetrics, trainingProgress, activeDataset } = useAuth();
  const isTrained = modelStatus === 'Trained' || (trainingReport && typeof trainingReport.accuracy === 'number');
  const isTraining = modelStatus === 'Training' || modelStatus === 'Preprocessing' || (trainingProgress && trainingProgress.isTraining);

  const fetchEvaluationReports = async () => {
    setLoadingReport(true);
    try {
      const [liveRes, trainRes] = await Promise.allSettled([
        apiGetLiveEvaluation(),
        apiGetModelReport()
      ]);

      if (liveRes.status === 'fulfilled' && liveRes.value) {
        setLiveReport(liveRes.value);
      }
      if (trainRes.status === 'fulfilled' && trainRes.value && typeof trainRes.value.accuracy === 'number') {
        setTrainingReport(trainRes.value);
      } else {
        setTrainingReport(null);
      }
    } catch (err) {
      console.error('Failed to load performance evaluations:', err);
      setTrainingReport(null);
    } finally {
      setLoadingReport(false);
    }
  };"""

# Replace Live Flows Evaluated card
old_card_block = """            <div className="min-w-0 flex-1">
              <div className="flex items-center justify-between gap-1 mb-0.5">
                <span className="text-[10px] uppercase font-bold text-slate-400">Live Flows Evaluated</span>
                <select
                  value={evalFlowLimit}
                  onChange={(e) => handleFlowLimitChange(Number(e.target.value))}
                  className="text-[10px] font-mono font-bold text-emerald-700 bg-emerald-50 border border-emerald-200 rounded px-1.5 py-0.5 cursor-pointer focus:outline-hidden"
                >
                  <option value={500}>500 Flows</option>
                  <option value={1000}>1,000 Flows</option>
                  <option value={2500}>2,500 Flows</option>
                  <option value={5000}>5,000 Flows</option>
                  <option value={10000}>10,000 Flows</option>
                  <option value={25000}>25,000 Flows</option>
                  <option value={50000}>50,000 Flows</option>
                </select>
              </div>
              <div className="text-lg font-black text-slate-900 font-mono flex items-baseline space-x-1.5">
                <span>{(liveReport.total_flows || 0).toLocaleString()}</span>
                {liveReport.requested_boundary && liveReport.total_flows < liveReport.requested_boundary && (
                  <span className="text-[10px] text-amber-600 font-sans font-bold">
                    (of {liveReport.requested_boundary.toLocaleString()} boundary)
                  </span>
                )}
              </div>
              <div className="text-[10px] text-slate-500 font-mono">
                {(liveReport.total_packets || 0).toLocaleString()} pkts ({(((liveReport.total_bytes || 0)) / 1024).toFixed(1)} KB)
              </div>
            </div>"""

new_card_block = """            <div className="min-w-0 flex-1">
              <div className="text-[10px] uppercase font-bold text-slate-400 mb-0.5">Live Flows Evaluated</div>
              <div className="text-lg font-black text-slate-900 font-mono">
                {(liveReport.total_flows || 0).toLocaleString()}
              </div>
              <div className="text-[10px] text-slate-500 font-mono">
                {(liveReport.total_packets || 0).toLocaleString()} pkts ({(((liveReport.total_bytes || 0)) / 1024).toFixed(1)} KB)
              </div>
            </div>"""

# Normalize line endings for replacement
content_norm = content.replace("\r\n", "\n")
old_state_norm = old_state_block.replace("\r\n", "\n")
new_state_norm = new_state_block.replace("\r\n", "\n")
old_card_norm = old_card_block.replace("\r\n", "\n")
new_card_norm = new_card_block.replace("\r\n", "\n")

if old_state_norm in content_norm and old_card_norm in content_norm:
    content_norm = content_norm.replace(old_state_norm, new_state_norm)
    content_norm = content_norm.replace(old_card_norm, new_card_norm)
    with open(model_details_path, "w", encoding="utf-8") as f:
        f.write(content_norm)
    print("SUCCESS: ModelDetailsView.jsx updated cleanly without dropdown.")
else:
    print("ERROR: Could not locate targets in ModelDetailsView.jsx")
