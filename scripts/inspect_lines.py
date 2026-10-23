with open('E:/ML/live_detection/detection_logger.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()
for i in range(1600, min(1680, len(lines))):
    print(f'{i+1}: {lines[i]}', end='')
