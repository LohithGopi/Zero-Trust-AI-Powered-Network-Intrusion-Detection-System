import sys
sys.path.append(r"E:\ML")
from app import create_app
from training.comparison_service import ModelComparisonService
from database.init_db import ModelHistory

app = create_app()
with app.app_context():
    models = ModelHistory.query.all()
    m_ids = [m.id for m in models]
    print(f"Comparing model IDs: {m_ids}")
    try:
        report = ModelComparisonService.compare_offline_benchmark(model_ids=m_ids, test_samples_limit=500)
        print("Summary:")
        for k, v in report.get("summary", {}).items():
            print(f"  {k}: {v}")
        print("\nModels:")
        for m in report.get("models", []):
            print(f"  {m['model_name']} ({m['algorithm']}): Acc={m['accuracy']}, FPR={m['false_positive_rate']}, F1={m['f1_score']}")
    except Exception as e:
        import traceback
        traceback.print_exc()
