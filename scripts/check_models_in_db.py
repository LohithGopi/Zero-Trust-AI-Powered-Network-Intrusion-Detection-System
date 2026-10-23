import sys
sys.path.append(r"E:\ML")
from app import create_app
from database.init_db import ModelHistory

app = create_app()
with app.app_context():
    models = ModelHistory.query.all()
    print(f"Total models in DB: {len(models)}")
    for m in models:
        print(m.to_dict())
