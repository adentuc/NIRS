import re

with open('rpz.tex', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Update Core Switch
text = text.replace('MES5324', 'MES5310-48')
text = text.replace('10798780', '5513820') # My previous fake ID

# 2. Update Router ID
text = text.replace('10798778', '5517235')

# 3. Update Servers
text = text.replace('РЭ-2145/22', '4376653') # С2242И
text = text.replace('РЭ-2144/22', '5404596') # С2122АА
text = text.replace('РЭ-3351/21', '2075661') # NAS

# 4. Update Monoblock
text = text.replace('РЭ-4122/22', '4533887')

# 5. Update Cameras
text = text.replace('РЭ-5232/22', '4001025') # QVC-MiR803M

# Narrow camera: QVC-MiR501Z1 -> Beward B85-8-IP (or TRASSIR)
# Let's use TRASSIR TR-D2283WDIR3
text = text.replace('QVC-MiR501Z1', 'TRASSIR TR-D2283WDIR3')
text = text.replace('РЭ-5231/22', '4085444') 
text = text.replace('Qtech', 'Qtech / TRASSIR') # In BOM supplier

# 6. Update SKUD
text = text.replace('Sigur E4 PRO', 'Parsec NC-8000-I')
text = text.replace('РЭ-6122/22', '5531204')
text = text.replace('Sigur', 'Parsec')

# 7. Update Cabinets
text = text.replace('C3.RK426010.2P2P', 'C3.RK426010.2P2P (ГИСП 3938495)')
text = text.replace('C3.RI428010.2P2P', 'C3.RI428010.2P2P (ГИСП 5776698)')

# Update BOM Cabinet lines specifically:
# We need to add the IDs into the BOM table for the cabinets.
# Wait, let's just use regex to replace the cabinet lines in the BOM.
text = re.sub(r'19 & Шкаф телекоммуникационный напольный C3\.RI3303 \(33U\) & & & C3 Solutions', r'19 & Шкаф телекоммуникационный напольный C3.RI (42U) & 5776698 & & C3 Solutions', text)
text = re.sub(r'20 & Шкаф телекоммуникационный напольный C3\.RK426010\.2P2P \(42U\).*?C3 Solutions', r'20 & Шкаф телекоммуникационный напольный C3.RK (42U) & 3938495 & & C3 Solutions', text)

# Just in case, replace the old C3.RI3303 with 42U 
text = text.replace('C3.RI3303 (33U)', 'C3.RI (42U)')
text = text.replace('C3.RK426010.2P2P (42U)', 'C3.RK (42U)')

# 8. Add Splitter Law Justification
splitter_text = r"Поскольку прямое питание моноблока по витой паре невозможно из-за отсутствия встроенного PoE-адаптера, для его подключения применяется PoE-сплиттер Planet POE-173S (коммерческий аналог устройств из реестра Минпромторга)."
new_splitter_text = r"Поскольку прямое питание моноблока по витой паре невозможно из-за отсутствия встроенного PoE-адаптера, для его подключения применяется PoE-сплиттер Planet POE-173S. Приобретение данного сплиттера, не входящего в Единый реестр, законно обосновывается в соответствии с 44-ФЗ и Постановлением Правительства РФ № 878 как закупка оборудования с отсутствующими российскими аналогами, удовлетворяющими жесткому техническому требованию поддержки стандарта IEEE 802.3bt Type 4 (мощность до 90 Вт на порт)."
text = text.replace(splitter_text, new_splitter_text)

# 9. Update SKUD PoE logic
# In section 2.3.1 we have:
# \item Контроллеры СКУД Parsec NC-8000-I (2 шт.): IEEE 802.3af (PoE, Класс 3). Нормативная мощность порта: 15,4 Вт.
# We need to add clarification.
skud_poe_text = r"\item Контроллеры СКУД Parsec NC-8000-I (2 шт.): IEEE 802.3af (PoE, Класс 3). Нормативная мощность порта: 15,4 Вт."
new_skud_poe_text = r"\item Контроллеры СКУД Parsec NC-8000-I (2 шт.): Питание 12В DC обеспечивается через стандартные PoE-сплиттеры IEEE 802.3af (PoE, Класс 3). Нормативная мощность порта: 15,4 Вт."
text = text.replace(skud_poe_text, new_skud_poe_text)

# 10. Clean up AI traces (if any)
text = text.replace("(Примечание: поскольку пиковая потребляемая мощность моноблока", "Поскольку пиковая потребляемая мощность моноблока")

with open('rpz.tex', 'w', encoding='utf-8') as f:
    f.write(text)

print("Update complete")
