import streamlit as st
from app.styling import template0_page_style
from app.styling import template1_page_style

import urllib.request
import os
from sqlalchemy import URL,create_engine, text
import plotly.express as px
import pandas as pd
from datetime import date,timedelta
import pmdarima as pm
from sympy import Point
import plotly.graph_objects as go


st.set_page_config(layout="wide")
template0_page_style()
template1_page_style()



file_name='datos/vista_insumos.csv'

def main_data():
    Url = open (file_name,'r',encoding="utf8")
    content = Url.read()
    Url.close()
    filas = content.split('\n')
    datos = []
    for fila in filas:
        datos.append(fila.split(','))
    df = pd.DataFrame(datos[1:])
    encabezados = ['id','departamento_nombre','departamento_id','municipio_nombre','municipio_id','producto_id','producto_nombre','valor','fechapublicacion','presentacion']
    df.columns = encabezados
    df['fechapublicacion'] = pd.to_datetime(df['fechapublicacion'])
    df['valor'] = df['valor'].astype(float) 
    with st.sidebar:
        dep = st.selectbox('Seleccionar departamento',df['departamento_nombre'].unique())
        filtro_departamento = 'departamento_nombre=="%s"'% dep
        muni = st.selectbox('Seleccionar municipio',df.query(filtro_departamento)['municipio_nombre'].unique())
        filtro_municipio = 'municipio_nombre=="%s"'% muni
        filtro_de_mu = filtro_departamento+' and '+filtro_municipio
        prod = st.selectbox('Seleccionar producto',df.query(filtro_de_mu)['producto_nombre'].unique())
        filtro_producto = 'producto_nombre=="%s"'% prod
        filtro_de_mu_pr = filtro_de_mu +' and '+filtro_producto
        pres = st.selectbox('Seleccionar Presentacion',df.query(filtro_de_mu_pr)['presentacion'].unique())
        filtro_pres = 'presentacion=="%s"'% pres
        filtro_de_mu_pr = filtro_de_mu +' and '+filtro_producto+' and '+filtro_pres
        #st.write('ok')
    unano = date.today()
    hoy = date.today()
    unano -= timedelta(days=365)
    col1, col2, col3, col4 = st.columns(4)
    with col1:  
     fi = st.date_input("Fecha Inicial", unano)
    with col2:  
     ff = st.date_input("Fecha Final", hoy)
    with col3:  
     option = st.selectbox('Frecuencia',('Semanal','Quincenal','Mensual'))
    with col4:  
     number = st.number_input('Predeccion %s '%option, 1, 10, 1)
    if option == 'Mensual':
        frecuencia = 'M'
    elif option == 'Quincenal':
        frecuencia = '15D'
    else:
        frecuencia = 'W' 
    df = df.query(filtro_de_mu_pr)    
    df = df.loc[df["fechapublicacion"].between(str(fi),str(ff))]
    if len(df)==0:
        st.subheader('👋 No hay datos para mostrar 👋 ',divider="green")
    else:
        df.set_index('fechapublicacion', inplace=True)
        df = df['valor']
        dff = df.copy()
        df = df.resample(frecuencia).mean().fillna(0)
        model = pm.auto_arima(df)
        pred = model.predict(n_periods=number)
        tpre = pd.DataFrame(pred)
        tpre.rename(columns={0:'Predicción'}, inplace=True)
        minimos_mensuales = dff.resample(frecuencia).min()
        max_mensuales = dff.resample(frecuencia).max()
        tpre['Minimo'] = df.min()#minimos_mensuales.tail(1).values[0]
        tpre['Maximo'] = df.max()#max_mensuales.tail(1).values[0]

        tpre = tpre.transpose()
        lista = []
        for i in range(len(pred)+1):
            if i == 0:
                lista.append([df.tail(1).index.values[0],df.tail(1).values[0]])
            else:
                lista.append([pred.index.values[i-1],pred[i-1]])
        pred = pd.DataFrame(lista)
        pred.set_index(0, inplace=True)
        df = pd.DataFrame(df)
        df['grupo']='Historico'
        pred['grupo']='Prediccion'
        pred.rename(columns={1:'valor'}, inplace=True)
        total = pd.concat([df,pred], axis=0)
        total2 = total.copy()
        total2.rename(columns={'valor':'Precio'}, inplace=True)
        total2 = total2.rename_axis('Fecha', axis='index')
        #st.dataframe(total2, use_container_width=True)
        import plotly.graph_objects as go
        fig = go.Figure()
        st.header(prod+' en '+pres)
        fig = px.line(total2,
                    x=total2.index,
                    y='Precio',
                    color='grupo',
                    symbol='grupo',
                    title='Gráfica con la prediccion %s de precios de insumos' % option,
                    color_discrete_map={'Historico': 'green', 'Prediccion': 'blue'}).update_traces(mode='markers+lines', line={'width':4})



        fig.add_trace(go.Scatter(x=max_mensuales.index, y=max_mensuales,mode='lines',name='Maximo')).update_traces(mode='markers+lines', line={'width':2})
        fig.add_trace(go.Scatter(x=minimos_mensuales.index, y=minimos_mensuales,mode='lines',name='Minimo')).update_traces(mode='markers+lines', line={'width':2})


        if len(df)!=0:
            st.plotly_chart(fig, use_container_width=True)
            st.subheader('Información general')
            tpre = tpre.T
            #st.dataframe(tpre, use_container_width=True)
            col1, col2, col3 = st.columns(3)
            col1.metric("Precio Predición", '$'+str('{:,}'.format(round(tpre['Predicción'].values[0],1))), "")
            col2.metric("Precio Maximo", '$'+str('{:,}'.format(round(tpre['Maximo'].values[0]))), "")
            col3.metric("Precio Minimo", '$'+str('{:,}'.format(round(tpre['Minimo'].values[0]))), "")


    
if(os.path.isfile(file_name)):
    main_data()
else:
    st.subheader('No fue posible acceder al conjunto de datos')



