import sys
with open('E:/ML/frontend/src/pages/dashboard/ModelDetailsView.jsx', 'r', encoding='utf-8') as f:
    lines = f.readlines()
for i in range(840, min(875, len(lines))):
    sys.stdout.buffer.write(f'{i+1}: {lines[i]}'.encode('utf-8'))
