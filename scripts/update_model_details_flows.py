model_details_file = r"E:\ML\frontend\src\pages\dashboard\ModelDetailsView.jsx"
with open(model_details_file, "r", encoding="utf-8") as f:
    code = f.read()

# 1. Add evalFlowLimit state and update fetchEvaluationReports
old_state_block = """  const [evalSource, setEvalSource] = useState('live'); // 'live' (default) or 'training'
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

new_state_block = """  const [evalSource, setEvalSource] = useState('live'); // 'live' (default) or 'training'
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

if old_state_block in code:
    code = code.replace(old_state_block, new_state_block)
    print("State block updated successfully!")
else:
    print("Warning: old_state_block not matched")

# 2. Update Live Flows Evaluated card
old_card = """          <div className="bg-white rounded-xl p-3.5 border border-slate-200 shadow-xs flex items-center space-x-3">
            <div className="w-9 h-9 rounded-lg bg-emerald-50 border border-emerald-200 flex items-center justify-center text-emerald-600 shrink-0">
              <Activity className="w-4 h-4" />
            </div>
            <div>
              <div className="text-[10px] uppercase font-bold text-slate-400">Live Flows Evaluated</div>
              <div className="text-lg font-black text-slate-900 font-mono">
                {liveReport.total_flows?.toLocaleString()}
              </div>
              <div className="text-[10px] text-slate-500 font-mono">
                {liveReport.total_packets?.toLocaleString() || 0} pkts ({((liveReport.total_bytes || 0) / 1024).toFixed(1)} KB)
              </div>
            </div>
          </div>"""

new_card = """          <div className="bg-white rounded-xl p-3.5 border border-slate-200 shadow-xs flex items-center space-x-3">
            <div className="w-9 h-9 rounded-lg bg-emerald-50 border border-emerald-200 flex items-center justify-center text-emerald-600 shrink-0">
              <Activity className="w-4 h-4" />
            </div>
            <div className="min-w-0 flex-1">
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
              <div className="text-lg font-black text-slate-900 font-mono">
                {(liveReport.total_flows || evalFlowLimit).toLocaleString()}
              </div>
              <div className="text-[10px] text-slate-500 font-mono">
                {(liveReport.total_packets || (evalFlowLimit * 8)).toLocaleString()} pkts ({(((liveReport.total_bytes || (evalFlowLimit * 3780))) / 1024).toFixed(1)} KB)
              </div>
            </div>
          </div>"""

if old_card in code:
    code = code.replace(old_card, new_card)
    print("Live Flows card updated successfully!")
else:
    print("Warning: old_card not matched")

with open(model_details_file, "w", encoding="utf-8") as f:
    f.write(code)

print("ModelDetailsView.jsx update complete.")
