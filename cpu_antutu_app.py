"""
Streamlit-приложение: сравнение процессоров смартфонов по AnTuTu-баллам.

Запуск:
    pip install streamlit pandas plotly
    streamlit run cpu_antutu_app.py
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ---------------------------------------------------------------------------
# 1. Данные о процессорах
# ---------------------------------------------------------------------------
# Значения AnTuTu являются усреднёнными ориентировочными оценками (v10/v9,
# порядок величины) и могут отличаться от актуальных замеров на конкретных
# устройствах. Перед принятием решений сверяйтесь со свежими бенчмарками.

DATA = [
    # name, vendor, year, process_nm, cores, max_ghz, antutu, category
    ("Snapdragon 8 Elite Gen 5", "Qualcomm", 2025, 3, 8, 4.6, 4_200_000, "Флагман"),
    ("Snapdragon 8 Elite", "Qualcomm", 2024, 3, 8, 4.32, 3_450_000, "Флагман"),
    ("Snapdragon 8 Gen 3", "Qualcomm", 2023, 4, 8, 3.3, 2_150_000, "Флагман"),
    ("Snapdragon 8 Gen 2", "Qualcomm", 2022, 4, 8, 3.2, 1_550_000, "Флагман"),
    ("Snapdragon 7+ Gen 3", "Qualcomm", 2024, 4, 8, 2.8, 1_450_000, "Средний+"),
    ("Snapdragon 7 Gen 3", "Qualcomm", 2024, 4, 8, 2.5, 1_050_000, "Средний"),
    ("Snapdragon 6 Gen 3", "Qualcomm", 2024, 4, 8, 2.3, 650_000, "Средний"),
    ("Snapdragon 4 Gen 2", "Qualcomm", 2023, 4, 8, 2.2, 420_000, "Бюджет"),

    ("Dimensity 9400+", "MediaTek", 2025, 3, 8, 3.73, 3_500_000, "Флагман"),
    ("Dimensity 9400", "MediaTek", 2024, 3, 8, 3.62, 2_350_000, "Флагман"),
    ("Dimensity 9300+", "MediaTek", 2024, 4, 8, 3.4, 2_200_000, "Флагман"),
    ("Dimensity 8300", "MediaTek", 2023, 4, 8, 3.35, 1_400_000, "Средний+"),
    ("Dimensity 7300", "MediaTek", 2024, 6, 8, 2.5, 850_000, "Средний"),
    ("Dimensity 6300", "MediaTek", 2024, 6, 8, 2.4, 480_000, "Бюджет"),

    ("Apple A19 Pro", "Apple", 2025, 3, 6, 4.0, 4_600_000, "Флагман"),
    ("Apple A18 Pro", "Apple", 2024, 3, 6, 4.04, 3_650_000, "Флагман"),
    ("Apple A17 Pro", "Apple", 2023, 3, 6, 3.78, 2_950_000, "Флагман"),
    ("Apple A16 Bionic", "Apple", 2022, 4, 6, 3.46, 1_700_000, "Флагман"),

    ("Exynos 2500", "Samsung", 2025, 3, 10, 3.3, 2_450_000, "Флагман"),
    ("Exynos 2400", "Samsung", 2024, 4, 10, 3.2, 1_950_000, "Флагман"),
    ("Exynos 1580", "Samsung", 2024, 4, 8, 2.9, 900_000, "Средний"),

    ("Google Tensor G4", "Google", 2024, 4, 9, 3.1, 1_350_000, "Флагман"),
    ("Google Tensor G3", "Google", 2023, 4, 9, 2.91, 1_100_000, "Флагман"),

    ("Kirin 9020", "HiSilicon", 2024, 7, 8, 2.3, 1_150_000, "Флагман"),
    ("Kirin 9010", "HiSilicon", 2023, 7, 8, 2.3, 900_000, "Флагман"),
]

COLUMNS = [
    "Модель", "Вендор", "Год", "Техпроцесс, нм", "Ядра",
    "Макс. частота, ГГц", "AnTuTu", "Класс",
]

df = pd.DataFrame(DATA, columns=COLUMNS)

# ---------------------------------------------------------------------------
# 2. Настройка страницы
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="Сравнение процессоров смартфонов",
    page_icon="📱",
    layout="wide",
)

st.title("📱 Сравнение процессоров смартфонов по AnTuTu")
st.caption(
    "Оценки AnTuTu являются усреднёнными ориентировочными значениями "
    "(порядок величины). Для точных цифр сверяйтесь с актуальными "
    "тестами на официальном сайте AnTuTu."
)

# ---------------------------------------------------------------------------
# 3. Боковая панель — фильтры
# ---------------------------------------------------------------------------
st.sidebar.header("Фильтры")

vendors = sorted(df["Вендор"].unique())
selected_vendors = st.sidebar.multiselect(
    "Вендор", vendors, default=vendors
)

categories = sorted(df["Класс"].unique())
selected_categories = st.sidebar.multiselect(
    "Класс устройства", categories, default=categories
)

year_min, year_max = int(df["Год"].min()), int(df["Год"].max())
selected_years = st.sidebar.slider(
    "Год выхода", year_min, year_max, (year_min, year_max)
)

antutu_min, antutu_max = int(df["AnTuTu"].min()), int(df["AnTuTu"].max())
selected_antutu = st.sidebar.slider(
    "Диапазон AnTuTu",
    antutu_min, antutu_max, (antutu_min, antutu_max),
    step=50_000,
    format="%d",
)

filtered_df = df[
    df["Вендор"].isin(selected_vendors)
    & df["Класс"].isin(selected_categories)
    & df["Год"].between(*selected_years)
    & df["AnTuTu"].between(*selected_antutu)
].sort_values("AnTuTu", ascending=False)

st.sidebar.markdown("---")
st.sidebar.metric("Найдено процессоров", len(filtered_df))

# ---------------------------------------------------------------------------
# 4. Основной выбор — сравнение конкретных чипов
# ---------------------------------------------------------------------------
st.subheader("Выберите процессоры для сравнения")

default_selection = filtered_df["Модель"].head(4).tolist()
compare_list = st.multiselect(
    "Модели процессоров",
    options=filtered_df["Модель"].tolist(),
    default=default_selection,
)

compare_df = filtered_df[filtered_df["Модель"].isin(compare_list)]

if compare_df.empty:
    st.info("Выберите хотя бы один процессор выше, чтобы увидеть сравнение.")
else:
    # -- Таблица сравнения ---------------------------------------------
    st.markdown("### Таблица сравнения")
    st.dataframe(
        compare_df.set_index("Модель").style.format({"AnTuTu": "{:,}"}),
        use_container_width=True,
    )

    # -- Столбчатая диаграмма AnTuTu -------------------------------------
    st.markdown("### AnTuTu — баллы")
    fig_bar = px.bar(
        compare_df.sort_values("AnTuTu"),
        x="AnTuTu",
        y="Модель",
        color="Вендор",
        orientation="h",
        text="AnTuTu",
        title="Сравнение баллов AnTuTu",
    )
    fig_bar.update_traces(texttemplate="%{text:,}", textposition="outside")
    fig_bar.update_layout(
        xaxis_title="AnTuTu, баллы",
        yaxis_title="",
        height=120 + 60 * len(compare_df),
    )
    st.plotly_chart(fig_bar, use_container_width=True)

    # -- Радар-диаграмма характеристик -----------------------------------
    st.markdown("### Радар-диаграмма характеристик")
    st.caption(
        "Значения нормированы (0–100%) относительно максимума среди "
        "выбранных процессоров, чтобы разные метрики можно было сравнить "
        "на одном графике."
    )

    radar_metrics = ["AnTuTu", "Ядра", "Макс. частота, ГГц", "Техпроцесс, нм"]
    radar_df = compare_df.set_index("Модель")[radar_metrics].copy()

    # Для техпроцесса меньше = лучше, поэтому инвертируем перед нормировкой
    radar_df["Техпроцесс, нм"] = radar_df["Техпроцесс, нм"].max() - radar_df["Техпроцесс, нм"] + 1

    normalized = radar_df / radar_df.max() * 100

    fig_radar = go.Figure()
    for model in normalized.index:
        fig_radar.add_trace(
            go.Scatterpolar(
                r=normalized.loc[model].tolist() + [normalized.loc[model].tolist()[0]],
                theta=radar_metrics + [radar_metrics[0]],
                fill="toself",
                name=model,
            )
        )
    fig_radar.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
        showlegend=True,
        height=500,
    )
    st.plotly_chart(fig_radar, use_container_width=True)

    # -- Динамика по годам ------------------------------------------------
    if compare_df["Год"].nunique() > 1:
        st.markdown("### AnTuTu по годам выпуска")
        fig_year = px.scatter(
            compare_df,
            x="Год",
            y="AnTuTu",
            color="Вендор",
            text="Модель",
            size="Ядра",
            title="Рост производительности по годам",
        )
        fig_year.update_traces(textposition="top center")
        st.plotly_chart(fig_year, use_container_width=True)

# ---------------------------------------------------------------------------
# 5. Полная таблица со всеми процессорами (с учётом фильтров)
# ---------------------------------------------------------------------------
st.markdown("---")
st.subheader("Полный список процессоров (с учётом фильтров)")
st.dataframe(
    filtered_df.set_index("Модель").style.format({"AnTuTu": "{:,}"}),
    use_container_width=True,
)

csv = filtered_df.to_csv(index=False).encode("utf-8-sig")
st.download_button(
    "⬇️ Скачать таблицу в CSV",
    data=csv,
    file_name="cpu_antutu_comparison.csv",
    mime="text/csv",
)

# ---------------------------------------------------------------------------
# 6. Возможность добавить свой процессор вручную
# ---------------------------------------------------------------------------
st.markdown("---")
with st.expander("➕ Добавить свой процессор для сравнения (временно, в рамках сессии)"):
    with st.form("add_cpu_form"):
        c1, c2, c3 = st.columns(3)
        with c1:
            new_name = st.text_input("Название модели")
            new_vendor = st.text_input("Вендор")
        with c2:
            new_year = st.number_input("Год", min_value=2015, max_value=2030, value=2025)
            new_nm = st.number_input("Техпроцесс, нм", min_value=2, max_value=28, value=4)
        with c3:
            new_cores = st.number_input("Кол-во ядер", min_value=1, max_value=16, value=8)
            new_ghz = st.number_input("Макс. частота, ГГц", min_value=0.5, max_value=6.0, value=3.0, step=0.1)
        new_antutu = st.number_input("AnTuTu баллы", min_value=1000, max_value=10_000_000, value=1_000_000, step=10_000)
        new_category = st.selectbox("Класс", ["Флагман", "Средний+", "Средний", "Бюджет"])

        submitted = st.form_submit_button("Добавить")
        if submitted and new_name and new_vendor:
            if "custom_cpus" not in st.session_state:
                st.session_state.custom_cpus = []
            st.session_state.custom_cpus.append(
                [new_name, new_vendor, new_year, new_nm, new_cores, new_ghz, new_antutu, new_category]
            )
            st.success(f"Процессор «{new_name}» добавлен! Обновите страницу выбора выше, чтобы сравнить его.")

    if st.session_state.get("custom_cpus"):
        st.markdown("**Добавленные вами процессоры:**")
        custom_df = pd.DataFrame(st.session_state.custom_cpus, columns=COLUMNS)
        st.dataframe(custom_df, use_container_width=True)
        # Объединяем с основным датасетом для использования в фильтрах при перезапуске
        df = pd.concat([df, custom_df], ignore_index=True)

st.markdown("---")
st.caption(
    "Данные приведены для ориентировочного сравнения. Реальные результаты "
    "AnTuTu зависят от конкретного устройства, версии ПО, охлаждения и "
    "версии бенчмарка."
)
