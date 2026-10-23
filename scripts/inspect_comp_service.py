with open('E:/ML/training/comparison_service.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()
for i in range(190, min(250, len(lines))):
    print(f'{i+1}: {lines[i]}', end='')
