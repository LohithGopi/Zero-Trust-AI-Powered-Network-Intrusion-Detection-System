import os

file_path = os.path.join("c:\\", "Users", "HP", "OneDrive", "Desktop", "ML", "frontend", "src", "pages", "dashboard", "TrainingView.jsx")

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

target1 = """      {/* 3. TRAINED MODEL VERSIONS & HISTORY TABLE */}
      <div className="bg-white rounded-2xl p-6 border border-slate-200/90 shadow-sm space-y-4">"""

replacement1 = """      {/* 3. TRAINED MODEL VERSIONS & HISTORY TABLE (Only included after model training) */}
      {(modelStatus === 'Trained' || !!trainedModel) && modelHistoryList.length > 0 && (
        <div className="bg-white rounded-2xl p-6 border border-slate-200/90 shadow-sm space-y-4">"""

if target1 not in content:
    raise ValueError("Target 1 not found in TrainingView.jsx")

content = content.replace(target1, replacement1, 1)

target2 = """            </table>
          </div>
        )}
      </div>

      {/* 4. STRATIFIED SAMPLING CONFIRMATION MODAL */}"""

replacement2 = """            </table>
          </div>
        )}
        </div>
      )}

      {/* 4. STRATIFIED SAMPLING CONFIRMATION MODAL */}"""

if target2 not in content:
    raise ValueError("Target 2 not found in TrainingView.jsx")

content = content.replace(target2, replacement2, 1)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)

print("SUCCESS: Successfully wrapped Section 3 in TrainingView.jsx!")
