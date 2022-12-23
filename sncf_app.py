import streamlit as st
import pandas as pd
import sqlalchemy as db
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns


engine = db.create_engine("sqlite:///sncf_table.sqlite")
connection = engine.connect()


st.title("Objets Perdus de la SNCF")
st.image(image = "Logo_Sncf.jpg")


st.subheader("Partie n°2 : Visualisation")
tab1,tab2,tab3 = st.tabs(["Question n°1","Question n°2","Question n°3"])




with tab1 :
    request = """ 
    SELECT Lost_Item.date, Lost_Item.type_objets
    FROM Lost_Item 
"""

    df_itemlost = pd.read_sql(request, connection, parse_dates=True)
    df_itemlost['date'] = pd.to_datetime(df_itemlost['date'])
    df_count = df_itemlost.groupby(pd.Grouper(key='date', freq='W-MON'))['type_objets'].agg('count').reset_index().rename(columns={'type_objets':"Nombre d'objets perdus"})
    df_count

    plt.figure(figsize=(17,8))

    plt.title("Nombre d'objets perdus par semaine")
    sns.set(style="darkgrid")

    sns.histplot(data=df_count, x="Nombre d'objets perdus", bins=50)

    st.pyplot(plt)

    fig = px.line(df_count, x="date", y="Nombre d'objets perdus",title="Evolution du nombre d'objets perdus sur la période 2016-2021")

    fig.update_layout(
        xaxis_title="Année",
        yaxis_title="Nombre d'objets perdus",
        legend_title="Type d'objet",
        showlegend=True
    )

    st.pyplot(fig)


