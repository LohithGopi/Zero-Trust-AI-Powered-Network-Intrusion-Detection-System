with open('E:/ML/frontend/src/pages/dashboard/ModelDetailsView.jsx', 'r', encoding='utf-8') as f:
    lines = f.readlines()
for i in range(8, 35):
    print(f'{i+1}: {repr(lines[i])}')
