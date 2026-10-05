import re

with open('rpz.tex', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace TRASSIR with QTECH QVC-MiR404Z532
content = content.replace('TRASSIR TR-D2283WDIR3', 'QTECH QVC-MiR404Z532')
content = content.replace('4085444 & & TRASSIR', '4001037 & & QTECH')
content = content.replace('4085444', '4001037')

# Replace '4K' references to '4 Мп'
content = content.replace('разрешения 4K (30~Гц)', 'разрешения 4 Мп (30~Гц)')
content = content.replace('4K 30~Гц', '4 Мп 30~Гц')
content = content.replace('4K-видеопотоков', 'видеопотоков высокого разрешения (4 Мп)')
content = content.replace('4K IP-камеры', '4 Мп IP-камеры')

with open('rpz.tex', 'w', encoding='utf-8') as f:
    f.write(content)
