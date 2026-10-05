import re

with open('rpz.tex', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. We need to find where Chapter 3 starts breaking.
anchor = r"\\textbf\{4\. Схемы заполнения шкафов по юнитам \(Фронтальный вид\)\}"
match = re.search(anchor, content)
if not match:
    print("Anchor not found")
    exit(1)
start_idx = match.end()

# The incorrectly placed new BOM ends with \end{landscape} right before \cleardoublepage ... ПРИЛОЖЕНИЕ А
end_marker_app_a = r"\\cleardoublepage\s*\\stepcounter\{chapter\}\s*\\phantomsection\s*\\addcontentsline\{toc\}\{chapter\}\{ПРИЛОЖЕНИЕ А\}"
match2 = re.search(end_marker_app_a, content[start_idx:])
if not match2:
    print("Appendix A marker not found")
    exit(1)

# 2. We will replace everything from start_idx up to the start of Appendix A with:
correct_rack_tables_and_placeholders = r"""

\textbf{Таблица 1. Серверный шкаф 42U (Фронтальный вид)}

\begin{small}
\begin{longtable}{|c|l|l|}
\hline
\textbf{U} & \textbf{Оборудование} & \textbf{Примечание} \\ \hline
\endfirsthead
\hline
\textbf{U} & \textbf{Оборудование} & \textbf{Примечание} \\ \hline
\endhead
42 & Оптическая патч-панель & Ввод оптики от кроссовой \\ \hline
41 & Кабельный органайзер 1U & \\ \hline
40 & Маршрутизатор Eltex ESR-1200 & \\ \hline
39 & Кабельный органайзер 1U & \\ \hline
38 & Коммутатор ядра Eltex MES5324 & \\ \hline
37 & Кабельный органайзер 1U & \\ \hline
36--22 & Резерв (Фальш-панели) & 15U \\ \hline
21 & Консоль KVM 1U & На удобной высоте $\sim$1 м \\ \hline
20--19 & Резерв (Фальш-панели) & 2U \\ \hline
18--17 & Сервер CI/CD Гравитон С2122АА & Вычислительное оборудование \\ \hline
16--15 & Медиасервер Гравитон С2242И & Вычислительное оборудование \\ \hline
14--13 & NAS Qtech QSRV-260202 & Массивные диски \\ \hline
12--5 & Резерв (Фальш-панели) & 8U под будущее расширение \\ \hline
4--3 & ИБП 2000 ВА & Источник питания \\ \hline
2--1 & Батарейный модуль 2U & В самом низу (Тяжелое) \\ \hline
0 & Вертикальный PDU 16 А & На задней стойке \\ \hline
\end{longtable}
\end{small}

\textbf{Таблица 2. Шкаф кроссовой 42U (Фронтальный вид)}

\begin{small}
\begin{longtable}{|c|l|l|}
\hline
\textbf{U} & \textbf{Оборудование} & \textbf{Примечание} \\ \hline
\endfirsthead
\hline
\textbf{U} & \textbf{Оборудование} & \textbf{Примечание} \\ \hline
\endhead
42 & Оптическая патч-панель & Аплинк до серверной \\ \hline
41 & Кабельный органайзер 1U & \\ \hline
40 & Патч-панель 24xRJ45 & Для коммутатора Aquarius \\ \hline
39 & Коммутатор Aquarius PoE++ & \\ \hline
38 & Патч-панель 24xRJ45 & Для коммутатора Aquarius \\ \hline
37 & Кабельный органайзер 1U & \\ \hline
36 & Патч-панель 24xRJ45 & Для Eltex PoE+ \\ \hline
35 & Коммутатор Eltex MES2448P & \\ \hline
34 & Патч-панель 24xRJ45 & Для Eltex PoE+ \\ \hline
33 & Кабельный органайзер 1U & \\ \hline
32 & Патч-панель 24xRJ45 & Для Eltex MES2448B (1) \\ \hline
31 & Коммутатор Eltex MES2448B (1) & \\ \hline
30 & Патч-панель 24xRJ45 & Для Eltex MES2448B (1) \\ \hline
29 & Кабельный органайзер 1U & \\ \hline
28 & Патч-панель 24xRJ45 & Для Eltex MES2448B (2) \\ \hline
27 & Коммутатор Eltex MES2448B (2) & \\ \hline
26 & Патч-панель 24xRJ45 & Для Eltex MES2448B (2) \\ \hline
25 & Кабельный органайзер 1U & \\ \hline
24--5 & Резерв (Фальш-панели) & 20U \\ \hline
4--3 & ИБП 2000 ВА & \\ \hline
2--1 & Батарейный модуль 2U & \\ \hline
0 & Вертикальный PDU 16 А & На задней стойке \\ \hline
\end{longtable}
\end{small}

\chapter{Расчет длины кабелей горизонтальной подсистемы}
(В разработке)

\chapter{Емкость кабельных трасс и заполнение лотков}
(В разработке)

\chapter{Кабельный журнал}
(В разработке)

\chapter{Экономическая часть}
(В разработке)

\chapter{Безопасность жизнедеятельности}
(В разработке)

\cleardoublepage
\phantomsection
\addcontentsline{toc}{chapter}{ЗАКЛЮЧЕНИЕ}
\chapter*{ЗАКЛЮЧЕНИЕ}
(В разработке)

\cleardoublepage
\phantomsection
\addcontentsline{toc}{chapter}{СПИСОК ИСПОЛЬЗОВАННЫХ ИСТОЧНИКОВ}
\chapter*{СПИСОК ИСПОЛЬЗОВАННЫХ ИСТОЧНИКОВ}
(В разработке)

"""

app_a_idx = start_idx + match2.start()
content = content[:start_idx] + correct_rack_tables_and_placeholders + content[app_a_idx:]

# 3. Now let's fix the OLD BOM which is situated somewhere near ПРИЛОЖЕНИЕ В
# Actually, the original BOM was right after Appendix A! No, in my previous replacement,
# I replaced Appendix A but the new appendix B label was added at the end of new_tz.
# Wait, let's see how new_tz ended in my `update_tz_bom.py`:
# \cleardoublepage
# \stepcounter{chapter}
# \phantomsection
# \addcontentsline{toc}{chapter}{ПРИЛОЖЕНИЕ Б}
# ...

# Let's find "ПРИЛОЖЕНИЕ Б" in the content and everything after it up to "ПРИЛОЖЕНИЕ В"
old_bom_start_marker = r"\\cleardoublepage\s*\\stepcounter\{chapter\}\s*\\phantomsection\s*\\addcontentsline\{toc\}\{chapter\}\{ПРИЛОЖЕНИЕ Б\}"
old_bom_end_marker = r"\\cleardoublepage\s*\\stepcounter\{chapter\}\s*\\phantomsection\s*\\addcontentsline\{toc\}\{chapter\}\{ПРИЛОЖЕНИЕ В\}"

match3 = re.search(old_bom_start_marker, content)
match4 = re.search(old_bom_end_marker, content)

if not match3 or not match4:
    print("Appendix B or V markers not found")
    print("Match3:", bool(match3), "Match4:", bool(match4))
    exit(1)

new_bom_correct = r"""\cleardoublepage
\stepcounter{chapter}
\phantomsection
\addcontentsline{toc}{chapter}{ПРИЛОЖЕНИЕ Б}

\begin{flushright}
ПРИЛОЖЕНИЕ Б
\end{flushright}

\begin{center}
\textbf{\large ВЕДОМОСТЬ ПОКУПНЫХ ИЗДЕЛИЙ}
\end{center}

\begin{landscape}
\begin{small}
\begin{longtable}{|c|c|p{4cm}|p{2cm}|p{2.5cm}|p{2cm}|c|p{2.5cm}|}
\hline
\multirow{2}{*}{\textbf{Поз.}} &
\multirow{2}{*}{\textbf{Код продукции}} &
\multirow{2}{*}{\textbf{Наименование}} &
\multirow{2}{*}{\textbf{Обозначение документа}} &
\multirow{2}{*}{\textbf{Поставщик}} &
\multirow{2}{*}{\textbf{Куда входит}} &
\textbf{Кол.} &
\multirow{2}{*}{\textbf{Примечание}} \tabularnewline
\cline{7-7}
 & \centering\textbf{(ГИСП / Артикул)} & & & & & \textbf{всего} & \tabularnewline
\hline
\endfirsthead

\hline
\multirow{2}{*}{\textbf{Поз.}} &
\multirow{2}{*}{\textbf{Код продукции}} &
\multirow{2}{*}{\textbf{Наименование}} &
\multirow{2}{*}{\textbf{Обозначение документа}} &
\multirow{2}{*}{\textbf{Поставщик}} &
\multirow{2}{*}{\textbf{Куда входит}} &
\textbf{Кол.} &
\multirow{2}{*}{\textbf{Примечание}} \tabularnewline
\cline{7-7}
 & \centering\textbf{(ГИСП / Артикул)} & & & & & \textbf{всего} & \tabularnewline
\hline
\endhead
\hline \multicolumn{8}{r}{\textit{Продолжение на следующей странице}} \\
\endfoot
\hline
\endlastfoot

\multicolumn{8}{|c|}{\textbf{Активное сетевое оборудование}} \\ \hline
1 & 3501244 & Коммутатор агрегации MES3324F & & Eltex & Кроссовая & 1 & \\ \hline
2 & 4812300 & Коммутатор доступа AQ-N3000-48P4Y2Q & & Aquarius & Кроссовая & 1 & \\ \hline
3 & 3501245 & Коммутатор доступа MES2448B & & Eltex & Кроссовая & 2 & \\ \hline
4 & 3501246 & Коммутатор доступа MES2448P & & Eltex & Кроссовая & 1 & \\ \hline
5 & 5513820 & Коммутатор ядра MES5310-48 & & Eltex & Серверная & 1 & \\ \hline
6 & 5517235 & Сервисный маршрутизатор ESR-1200 & & Eltex & Серверная & 1 & \\ \hline
7 & Трансивер & Оптический трансивер SFP+ 10GBASE-SR & & Eltex & Коммутаторы & 4 & \\ \hline

\multicolumn{8}{|c|}{\textbf{Вычислительное оборудование и рабочие станции}} \\ \hline
8 & 4376653 & Медиасервер стоечный С2242И (2U) & & Гравитон & Серверная & 1 & \\ \hline
9 & 4533887 & Моноблок оператора М75И (PoE++) & & Гравитон & Операторская & 6 & \\ \hline
10 & 5404596 & Сервер CI/CD С2122АА (2U) & & Гравитон & Серверная & 1 & \\ \hline
11 & 2075661 & Сетевое хранилище (NAS) QSRV-260202 & & Qtech & Серверная & 1 & \\ \hline

\multicolumn{8}{|c|}{\textbf{Системы безопасности и контроля}} \\ \hline
12 & 4001025 & Обзорная 4 Мп IP-камера QVC-MiR803M & & QTECH & Лаборатории & 2 & \\ \hline
13 & 5531204 & Контроллер СКУД NC-8000-I (PoE) & & Parsec & Двери & 2 & \\ \hline
14 & 4001037 & Узконаправленная 4 Мп IP-камера QVC-MiR404Z532 & & QTECH & Стенды & 6 & \\ \hline

\multicolumn{8}{|c|}{\textbf{Системы бесперебойного электропитания и климат-контроля}} \\ \hline
15 & 5689102 & Батарейный модуль БМ-РСК-Эксперт-II-2000 & & Сайбер Электро & Шкафы & 2 & \\ \hline
16 & 5689101 & ИБП стоечный РСК-Эксперт-II-2000С & & Сайбер Электро & Шкафы & 2 & \\ \hline
17 & 3841120 & Блок распределения питания (PDU) 16А, 19'' & & C3 Solutions & Шкафы & 2 & \\ \hline
18 & Вне реестра & PoE-сплиттер Gigabit IEEE 802.3bt POE-173S & & Planet & Операторская & 6 & \\ \hline
19 & Вне реестра & Сплит-система настенная DHP-09 (2.5 кВт) & & Dahatsu & Серверная & 4 & \\ \hline
20 & 5776698 & Шкаф телекоммуникационный C3.RI (42U) & & C3 Solutions & Кроссовая & 1 & \\ \hline
21 & 3938495 & Шкаф телекоммуникационный C3.RK (42U) & & C3 Solutions & Серверная & 1 & \\ \hline
22 & Вентилятор & Модуль вентиляторный в крышу & & C3 Solutions & Шкафы & 2 & \\ \hline

\multicolumn{8}{|c|}{\textbf{Пассивное сетевое оборудование и кабельные системы}} \\ \hline
23 & NKL 4140C-BK & Кабель U/UTP, Cat.6A, 4x2x23AWG (бухта 500 м) & & NIKOMAX & Трассы & 8 & 4000 м \\ \hline
24 & NMC-RP24UD2 & Патч-панель 24 порта RJ-45, Cat.6A, 1U & & NIKOMAX & Шкафы & 7 & \\ \hline
25 & NMC-WP02UD2 & Розетка телекоммуникационная 2 порта RJ-45, Cat.6A & & NIKOMAX & Рабочие места & 75 & \\ \hline
26 & C3.ORG & Органайзер кабельный горизонтальный 19", 1U & & C3 Solutions & Шкафы & 10 & \\ \hline
27 & ОМ4-8 & Кабель волоконно-оптический многомодовый OM4 & & Еврокабель & Магистрали & 200 & В метрах \\ \hline
28 & Кросс 1U & Оптическая распределительная панель 19", 1U, 24 LC & & ЦМО & Шкафы & 2 & \\ \hline
29 & LC-LC & Шнур оптический соединительный LC-LC OM4, 2 м & & NIKOMAX & Шкафы & 4 & \\ \hline

\end{longtable}
\end{small}
\end{landscape}

"""

content = content[:match3.start()] + new_bom_correct + content[match4.start():]

with open('rpz.tex', 'w', encoding='utf-8') as f:
    f.write(content)

print("Structure fixed successfully.")
