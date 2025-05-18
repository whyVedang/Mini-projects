import streamlit as st 
import pandas as pd
import numpy as np
import plotly.express as px

def streamlit_config():
    st.set_page_config(page_title="Personal Finances",page_icon="💰" ,layout="wide")
    st.title("Personal Finances")
    st.write("This is a personal finance app that helps you track your income and expenses.")
    uploadFile()


def uploadFile():
    upload=st.file_uploader("Upload a CSV file", type=["csv"])
    if upload is not None:
        df=load(upload)


def load(upload):
    try:
        df=pd.read_csv(upload)
        st.write("Data loaded successfully!")
        cleanData(df)
        st.write(df)
        if df is not None:
            df1=df.drop(columns=['Withdrawls'])
            df2=df.drop(columns=['Deposits'])
            tab1,tab2=st.tabs(['Credit','Debit'])
            with tab1:
                df1 = df1[df1['Deposits'] != '00.00']
                IncData(df1)
                st.write(df1)
            with tab2:
                df2 = df2[df2['Withdrawls'] != '00.00']
                ExpData(df2)
                st.write(df2)
        return df
    except Exception as e:
        st.error(f"Error loading file: {str(e)}")
        return None
    

def cleanData(df):
     # Remove empty rows
    df.columns=[col.strip() for col in df.columns]
    df.dropna(how='all', inplace=True)
    df['Deposits']=df['Deposits'].str.replace(',', '')
    df['Withdrawls']=df['Withdrawls'].str.replace(',', '')
    df['Balance']=df['Balance'].str.replace(',', '')
    return df

def ExpData(df):
    st.subheader('Expense Summary')
    category=df
    category['Withdrawls'] = category['Withdrawls'].astype(float)
    category=df.groupby('Category')['Withdrawls'].sum().reset_index()
    category=category.sort_values(by='Withdrawls', ascending=False)
    st.metric("Total", category['Withdrawls'].sum())
    st.dataframe(category,
                    hide_index=True,
                    use_container_width=True
                )
    Expensefigure(category)


def IncData(df):
    st.subheader('Income Summary')
    category=df
    category['Deposits'] = category['Deposits'].astype(float)
    category=df.groupby('Category')['Deposits'].sum().reset_index()
    category=category.sort_values(by='Deposits', ascending=False)
    st.metric("Total", category['Deposits'].sum())
    st.dataframe(category,
                    hide_index=True,
                    use_container_width=True
                )
    IncomeFig(category)
    
def Expensefigure(df):
    fig=px.pie(df,values='Withdrawls',names='Category',title='Expenses')
    st.plotly_chart(fig, use_container_width=True)


def IncomeFig(df): 
    fig=px.pie(df,values='Deposits',names='Category',title='Income')
    st.plotly_chart(fig, use_container_width=True)
