import streamlit as st
import json
import requests
from app.config.settings import api_settings
from dbfread import DBF
import pandas as pd
import matplotlib.pyplot as plt
import altair as alt


@st.cache_data
def get_data_frame():
    COSTOS = 'Bases 2021/31-12-2021/Spm2003/2021/costos22.DBF'
    dbf_costos = DBF(COSTOS)
    df_costos = pd.DataFrame(iter(dbf_costos))
    df = df_costos
    df['CCACTUAL'] = df['CCACTUAL'].astype(int)
    df = df[['PEDIDO', 'ORDEN', 'CCACTUAL', 'MODELO', 'NMODELO', 'CODIGO']]
    informe_ccactual = df.pivot_table(index=["MODELO", "NMODELO", "PEDIDO", 'ORDEN'],
                                      columns=["CCACTUAL"], values="CODIGO", aggfunc="count", fill_value=0)
    # Calcular la columna "OTRAS" como la suma de ccactual diferentes de 100, 110 y 600
    informe_ccactual['TEJIDO'] = informe_ccactual[100] + \
        informe_ccactual[110] + informe_ccactual[112]
    informe_ccactual['FINALIZADO'] = informe_ccactual[600]
    informe_ccactual['EN_PROGRESO'] = informe_ccactual.sum(
        axis=1) - informe_ccactual['FINALIZADO'] - informe_ccactual['TEJIDO']

    # SELECIONA LAS COLUMNAS 100, 110, 600, OTRAS_CCOSTO, MODELO, NMODELO, COLOR
    # print(informe_ccactual.columns)
    informe_ccactual = informe_ccactual[[
        'TEJIDO', 'FINALIZADO', 'EN_PROGRESO']]
    informe_ccactual = informe_ccactual.reset_index()

    informe_ccactual = informe_ccactual[[
        'PEDIDO', 'ORDEN', 'MODELO', 'NMODELO', 'TEJIDO', 'FINALIZADO', 'EN_PROGRESO']]
    # count rows
    # print(informe_ccactual.shape[0])
    return informe_ccactual


def run():
    st.set_page_config(
        page_title=api_settings.TITLE,
        page_icon="✅",
        layout="wide",
        # initial_sidebar_state="expanded",
    )
    # st.title(api_settings.TITLE)
    informe_ccactual = get_data_frame()
   
    # st.title(api_settings.TITLE)
 
    # Get unique combinations of PEDIDO and ORDEN
    unique_combinations = informe_ccactual[[
        'PEDIDO', 'ORDEN']].drop_duplicates()
    # Allow the user to select PEDIDO and ORDEN interactively
    fit_col1,fit_col2 = st.columns(2)

    with fit_col1:
        selected_pedido = st.selectbox(
            "Select PEDIDO", unique_combinations['PEDIDO'].unique())
    # with fit_col2:
    #     selected_orden = st.selectbox("Select ORDEN", unique_combinations[unique_combinations['PEDIDO'] == selected_pedido]['ORDEN'].unique())

    # st.subheader(f'Pie Chart for PEDIDO: {selected_pedido} and ORDEN: {selected_orden}')

    # Filter data for the selected PEDIDO and ORDEN
    data = informe_ccactual[(informe_ccactual['PEDIDO'] == selected_pedido)]
    # print(data)

    kpi1, kpi2, kpi3,kpi4 = st.columns(4)
    tejido = data['TEJIDO'].sum()
    en_progreso = data['EN_PROGRESO'].sum()
    finalizado = data['FINALIZADO'].sum()
    total = tejido + en_progreso + finalizado

    kpi1.metric(
        label="TOTAL",
        value=total,
    )

    kpi2.metric(
        label="TEJIDO",
        value=tejido,
    )

    kpi3.metric(
        label="EN_PROGRESO",
        value=en_progreso,
    )
    kpi4.metric(
        label="FINALIZADO",
        value=finalizado,
    )

    # fig_col2 = st.columns(1)
    labels = ['TEJIDO', 'EN_PROGRESO', 'FINALIZADO']
    colors = ['#e74c3c', '#f1c40f', '#2ecc71']

    # # Create a pie chart
    # with fig_col1:
    #     # plt.figure(figsize=(2, 2))
    #     labels = ['TEJIDO', 'EN_PROGRESO', 'FINALIZADO']
    #     sizes = [tejido, en_progreso, finalizado]
    #     colors = ['#e74c3c', '#f1c40f', '#2ecc71']
    #     explode = (0.1, 0.1, 0.1)  # Separation of the sections
    #     plt.pie(sizes, explode=explode, labels=labels,
    #             colors=colors, autopct='%1.1f%%', startangle=140)
    #     # Equal aspect ratio ensures that the pie chart is drawn as a circle
    #     plt.axis('equal')
    #     st.pyplot(plt)
    
    # with fig_col2:
        # Create horizontal bar charts for each model within the selected PEDIDO and ORDEN
        # st.subheader(f'Horizontal Bar Charts for PEDIDO: {selected_pedido} and ORDEN: {selected_orden}')
        # value_vars = ['TEJIDO', 'EN_PROGRESO', 'FINALIZADO']
    alt_data = data.melt(
        id_vars=['NMODELO'], value_vars=labels, var_name='Category', value_name='Count')

    chart = alt.Chart(alt_data).mark_bar().encode(
        x=alt.X('Count:Q', title='Count', ),
        y=alt.Y('NMODELO:N', title='Model', sort='-x'),
        color=alt.Color('Category:N',
                        scale=alt.Scale(
                            domain=labels,
                            range=colors,
                        ),
                        sort=labels
                        ),
        order=alt.Order('color_Category_sort_index:Q'),
    )

    st.altair_chart(chart, use_container_width=True)


    st.dataframe(data)


if __name__ == '__main__':
    run()
