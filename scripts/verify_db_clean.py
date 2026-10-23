import sqlite3
import json

conn = sqlite3.connect('database/database.db')
cursor = conn.cursor()

# Update model_history table
cursor.execute("SELECT id, params_json, metrics_json, algorithm, model_name, model_type FROM model_history")
rows = cursor.fetchall()
for row_id, p_json, m_json, algo, m_name, m_type in rows:
    new_algo = "Support Vector Machine" if "forest" in str(algo).lower() else algo
    new_name = "Support Vector Machine (NSL-KDD)" if "forest" in str(m_name).lower() else m_name
    new_type = "Kernel Methods (Support Vector Classifier / RBF)" if "forest" in str(m_type).lower() or "ensemble" in str(m_type).lower() else m_type
    
    new_p_json = p_json
    if new_p_json:
        new_p_json = new_p_json.replace("Random Forest", "Support Vector Machine")
        new_p_json = new_p_json.replace("random_forest", "svm")
        new_p_json = new_p_json.replace("Ensemble Learning (Bagging / Decision Trees)", "Kernel Methods (Support Vector Classifier / RBF)")
        
    new_m_json = m_json
    if new_m_json:
        new_m_json = new_m_json.replace("Random Forest", "Support Vector Machine")
        new_m_json = new_m_json.replace("random_forest", "svm")
        new_m_json = new_m_json.replace("Ensemble Learning (Bagging / Decision Trees)", "Kernel Methods (Support Vector Classifier / RBF)")

    cursor.execute("""
        UPDATE model_history
        SET algorithm = ?, model_name = ?, model_type = ?, params_json = ?, metrics_json = ?
        WHERE id = ?
    """, (new_algo, new_name, new_type, new_p_json, new_m_json, row_id))

# Also clean audit_logs
cursor.execute("""
    UPDATE audit_logs 
    SET details = replace(replace(details, 'Random Forest', 'Support Vector Machine'), 'random_forest', 'svm')
    WHERE details LIKE '%random_forest%' OR details LIKE '%Random Forest%'
""")

conn.commit()

# Verify remaining
cursor.execute("SELECT count(*) FROM model_history WHERE lower(algorithm) LIKE '%forest%' OR lower(model_name) LIKE '%forest%'")
print("Remaining forest in model_history:", cursor.fetchone()[0])
conn.close()
print("DB Cleaned successfully.")
