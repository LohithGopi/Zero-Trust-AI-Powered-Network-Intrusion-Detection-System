import sys
with open('E:/ML/live_detection/detection_logger.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()
for i in range(1690, min(1730, len(lines))):
    sys.stdout.buffer.write(f'{i+1}: {lines[i]}'.encode('utf-8'))
