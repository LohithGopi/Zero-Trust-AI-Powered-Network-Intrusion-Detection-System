with open('E:/ML/training/comparison_service.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()
for i in range(390, min(450, len(lines))):
    print(f'{i+1}: {lines[i]}', end='')
