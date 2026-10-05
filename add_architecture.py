import re

with open('/Users/anton/Documents/NIRS/rpz.tex', 'r', encoding='utf-8') as f:
    rpz = f.read()

# 1. Add tikz library to preamble
if '\\usepackage{tikz}' not in rpz:
    rpz = rpz.replace('\\usepackage{pgfplots}', '\\usepackage{tikz}\n\\usetikzlibrary{positioning, shapes.geometric, arrows.meta, decorations.pathreplacing}\n\\usepackage{pgfplots}')

# 2. Add Architecture Section right after \chapter{Трафик, архитектура, выбор активного оборудования}
arch_section = r'''
\section{Логическая архитектура и топология сети}

Согласно техническому заданию и современным корпоративным стандартам, сеть предприятия строится по классической трехуровневой иерархической модели (Cisco Three-Tier Model), что обеспечивает масштабируемость, отказоустойчивость и безопасность.

\subsection{Уровни иерархии и аплинки}

\begin{enumerate}
    \item \textbf{Уровень доступа (Access):} Располагается в кроссовой комнате (пом. №\,16). Задача уровня — терминация горизонтальных кабельных линий (148 портов) и обеспечение конечных устройств доступом в сеть с требуемыми параметрами электропитания (PoE+, PoE++). 
    \item \textbf{Уровень агрегации (Aggregation):} Также располагается в кроссовой комнате (пом. №\,16). Все 4 коммутатора уровня доступа подключаются оптическими патч-кордами (10G SFP+) к стеку коммутаторов агрегации. Это позволяет локализовать межкоммутаторный трафик и исключить прокладку горизонтального медного кабеля между кроссовой и серверной комнатами.
    \item \textbf{Уровень ядра (Core):} Размещается в серверной комнате этажа (пом. №\,19). Соединяется со стеком агрегации кроссовой посредством магистрального оптического канала — агрегированного линка (LACP / IEEE 802.3ad) емкостью $2 \times 10$\,Гбит/с. Ядро осуществляет высокоскоростную маршрутизацию между VLAN, связь с серверами, главным шлюзом сети (маршрутизатором) и стояками других этажей (№\,9 и №\,11).
\end{enumerate}

\subsection{Логическая адресация и VLAN}

Для изоляции широковещательных доменов, обеспечения безопасности и управления качеством обслуживания (QoS), логическая структура сети сегментируется на виртуальные локальные сети (VLAN). Применяется следующая схема адресации (блок $10.10.x.x$):

\begin{itemize}
    \item \textbf{VLAN 10 (Management):} $10.10.10.0/24$ — управление сетевым оборудованием (коммутаторы, маршрутизатор, ИБП).
    \item \textbf{VLAN 20 (Users):} $10.10.20.0/24$ — рабочие станции операторов и административного персонала.
    \item \textbf{VLAN 30 (IoT \& Labs):} $10.10.30.0/23$ — расширенная подсеть для тестируемых устройств IoT на стендах лабораторий (вмещает до 510 хостов).
    \item \textbf{VLAN 40 (Video \& Security):} $10.10.40.0/24$ — IP-камеры видеонаблюдения, медиасервер и контроллеры СКУД. Изоляция данного трафика критична для обеспечения работы режима MCU/SFU.
    \item \textbf{VLAN 50 (Servers):} $10.10.50.0/24$ — сервер CI/CD, NAS хранилище, интерфейсы управления серверами.
\end{itemize}

Схема логической топологии приведена в Приложении В.
'''

rpz = rpz.replace(
    '\\chapter{Трафик, архитектура, выбор активного оборудования}\n',
    '\\chapter{Трафик, архитектура, выбор активного оборудования}\n' + arch_section + '\n'
)

# 3. Add Aggregation switch to selection and BOM
# Let's insert the aggregation switch selection text right before core switch selection
agg_switch_text = r'''
\subsection{Выбор коммутатора агрегации}

Для консолидации трафика от коммутаторов доступа в кроссовой комнате (пом. №\,16) и организации резервированного высокоскоростного аплинка до серверной комнаты (пом. №\,19), проектом предусмотрен уровень агрегации. Выбран оптический коммутатор \textbf{Eltex MES3324F} (20 портов 1000Base-X (SFP), 4 порта 10/100/1000Base-T/1000Base-X Combo, 4 порта 10G SFP+). Он обеспечивает неблокируемую коммутацию и поддержку LACP, что необходимо для объединения двух линий 10G SFP+ в единый транк до ядра.
'''

rpz = rpz.replace(
    '% ---- Выбор коммутатора ядра ----',
    agg_switch_text + '\n% ---- Выбор коммутатора ядра ----'
)

# Insert into BOM
bom_agg_entry = r'1.6 & Коммутатор агрегации MES3324F (20xSFP, 4xCombo, 4x10G SFP+) & Eltex & шт. & 1 & Кроссовая (пом. №\,16), агрегация аплинков \\ \hline'
rpz = rpz.replace(
    '1.5 & Коммутатор доступа MES2448B (48x1G, 4x10G SFP+) & Eltex & шт. & 2 & Кроссовая (пом. №\,16), стенды лабораторий \\\\\n\\hline',
    '1.5 & Коммутатор доступа MES2448B (48x1G, 4x10G SFP+) & Eltex & шт. & 2 & Кроссовая (пом. №\,16), стенды лабораторий \\\\\n\\hline\n' + bom_agg_entry + '\n'
)

# 4. Add Appendix V (Logical Diagram)
appendix_v = r'''
\cleardoublepage
\stepcounter{chapter}
\phantomsection
\addcontentsline{toc}{chapter}{ПРИЛОЖЕНИЕ В}

\begin{flushright}
ПРИЛОЖЕНИЕ В
\end{flushright}

\begin{center}
\textbf{\large Схема логической топологии сети}
\end{center}

Ниже представлена структурная логическая схема разрабатываемой сети с разделением на уровни иерархии (Ядро, Агрегация, Доступ) и физическим расположением оборудования по помещениям.

\vspace{1cm}
\begin{center}
\begin{tikzpicture}[
    box/.style={draw, rectangle, rounded corners, minimum width=3.5cm, minimum height=1cm, text centered, font=\sffamily\footnotesize},
    core/.style={box, fill=red!10, draw=red!60, thick},
    agg/.style={box, fill=blue!10, draw=blue!60, thick},
    acc/.style={box, fill=green!10, draw=green!60, thick},
    server/.style={box, fill=gray!10, draw=gray!60},
    link/.style={draw, thick, -},
    uplink/.style={draw, thick, blue, -},
    lacp/.style={draw, ultra thick, red, -},
    node distance=1.5cm and 1cm
]

% Уровень ядра (Серверная)
\node[core] (core_sw) {Ядро: MES5324};
\node[server, above=of core_sw] (router) {Шлюз: ESR-1200};
\node[server, left=of core_sw, xshift=-1cm] (servers) {Серверы (VLAN 50, 40)};

\draw[link] (router) -- (core_sw);
\draw[link] (servers) -- (core_sw);

% Рамка для серверной
\draw[dashed, draw=gray, rounded corners] 
    ([xshift=-1.5cm,yshift=1cm]servers.north west) rectangle 
    ([xshift=1.5cm,yshift=-1cm]core_sw.south east) 
    node[below right] at ([xshift=-1.5cm,yshift=1cm]servers.north west) {\textbf{Серверная (пом. 19)}};

% Уровень агрегации (Кроссовая)
\node[agg, below=of core_sw, yshift=-1.5cm] (agg_sw) {Агрегация: MES3324F};

% Связь Ядро - Агрегация (LACP)
\draw[lacp] (core_sw) -- node[right, font=\scriptsize, text=red] {LACP $2\times10$G SFP+} (agg_sw);

% Уровень доступа (Кроссовая)
\node[acc, below left=of agg_sw, xshift=1cm] (acc_poe2) {Доступ: AQ-N3000 (PoE++)};
\node[acc, right=of acc_poe2] (acc_poe) {Доступ: MES2448P (PoE+)};
\node[acc, right=of acc_poe] (acc_base) {Доступ: MES2448B $\times 2$};

\draw[uplink] (acc_poe2) -- node[left, font=\scriptsize] {10G} (agg_sw);
\draw[uplink] (acc_poe) -- node[left, font=\scriptsize] {10G} (agg_sw);
\draw[uplink] (acc_base) -- node[right, font=\scriptsize] {10G} (agg_sw);

% Рамка для кроссовой
\draw[dashed, draw=gray, rounded corners] 
    ([xshift=-0.5cm,yshift=1cm]agg_sw.north west -| acc_poe2.west) rectangle 
    ([xshift=0.5cm,yshift=-1cm]acc_base.south east)
    node[below right] at ([xshift=-0.5cm,yshift=1cm]agg_sw.north west -| acc_poe2.west) {\textbf{Кроссовая (пом. 16)}};

\end{tikzpicture}
\end{center}

\vspace{1cm}
\noindent Оптические аплинки 10G от коммутаторов доступа подключаются к портам SFP+ коммутатора агрегации. Связь между коммутатором агрегации и коммутатором ядра осуществляется по двум оптическим волокнам, объединенным в группу LACP, что обеспечивает общую пропускную способность магистрали 20 Гбит/с и отказоустойчивость соединения.
'''

rpz = rpz.replace(
    '\\end{appendices}',
    appendix_v + '\n\\end{appendices}'
)

with open('/Users/anton/Documents/NIRS/rpz.tex', 'w', encoding='utf-8') as f:
    f.write(rpz)

print("Architecture section and Appendix V added.")
