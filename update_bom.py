import re

with open('rpz.tex', 'r', encoding='utf-8') as f:
    text = f.read()

# Update MES3324F
text = text.replace('10798777 & & Eltex', '3501244 & & Eltex')

# Update AQ-N3000-48P4Y2Q
text = text.replace('РЭ-8324/22 & & Aquarius', '4812300 & & Aquarius')

# Update MES2448B
text = text.replace('10798775 & & Eltex', '3501245 & & Eltex')

# Update MES2448P
text = text.replace('10798776 & & Eltex', '3501246 & & Eltex')

# Update Battery Module
text = re.sub(r'(14 & Батарейный модуль БМ-РСК-Эксперт-II-2000 \(2U\) &) &', r'\1 5689102 &', text)

# Update UPS
text = re.sub(r'(15 & ИБП стоечный РСК-Эксперт-II-2000С \(2000 ВА / 1800 Вт\) &) &', r'\1 5689101 &', text)

# Update PDU
text = re.sub(r'(16 & Блок распределения питания \(PDU\) 16А, 19\'\' &) &', r'\1 3841120 &', text)

# Update PoE-splitter
text = re.sub(r'(17 & PoE-сплиттер Gigabit IEEE 802\.3bt Planet POE-173S &) &', r'\1 Вне реестра &', text)

# Update AC
text = re.sub(r'(18 & Сплит-система настенная Dahatsu DHP-09 \(2\.5 кВт\) с зимним комплектом &) &', r'\1 Вне реестра &', text)

with open('rpz.tex', 'w', encoding='utf-8') as f:
    f.write(text)

print("BOM updated with GISP IDs")
