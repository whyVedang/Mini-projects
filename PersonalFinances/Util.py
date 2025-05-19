import streamlit as st 
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import date
import uuid
def dashboard():
    st.set_page_config(page_title="Dashboard", page_icon="💰", layout="wide")
    st.title("Dashboard")
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox("Select a page", ["Dashboard", "Budget", "Goals"])

    if 'df' not in st.session_state:
        st.session_state.df = None

    if page == "Dashboard":
        st.title("Personal Finances")
        st.write("This is a personal finance app that helps you track your income and expenses.")
        
        if st.session_state.df is None:
            uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])
            if uploaded_file:
                try:
                    df = pd.read_csv(uploaded_file)
                    df = cleanData(df) 
                    st.session_state.df = df
                    st.success("Data loaded successfully!")
                except Exception as e:
                    st.error(f"Error loading file: {str(e)}")
        
        if st.session_state.df is not None:
            display_data_tabs(st.session_state.df)

    elif page == "Budget":
        Budget(st.session_state.df)
    elif page == "Goals":
        goals()

def display_data_tabs(df):
    df1 = df.drop(columns=['Withdrawls'])
    df2 = df.drop(columns=['Deposits'])
    
    tab1, tab2 = st.tabs(['Credit', 'Debit'])
    with tab1:
        df1 = df1[df1['Deposits'] != '00.00']
        IncData(df1)
    with tab2:
        df2 = df2[df2['Withdrawls'] != '00.00']
        ExpData(df2)

def cleanData(df):
    df = df.copy()
    df.columns = [col.strip() for col in df.columns]
    df.dropna(how='all', inplace=True)
    df['Deposits'] = df['Deposits'].str.replace(',', '').astype(float)
    df['Withdrawls'] = df['Withdrawls'].str.replace(',', '').astype(float)
    df['Balance'] = df['Balance'].str.replace(',', '').astype(float)
    df['Date'] = pd.to_datetime(df['Date'], format='%d-%b-%Y', errors='coerce')
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

def Budget(df):
    st.header("Your Budget")
    if df is None:
        st.warning("No data available. Please upload your transactions file.")
        return

    df['Withdrawls'] = pd.to_numeric(df['Withdrawls'], errors='coerce')
    df['Deposits'] = pd.to_numeric(df['Deposits'], errors='coerce')

    df['CategoryType'] = df['Category'].apply(assign_category_type)

    df_exp = df[df['CategoryType'].notnull()]

    total_income = df['Deposits'].sum()
    if total_income == 0:
        st.error("Income is zero. Cannot compute budget recommendations.")
        return

    # 50/30/20 
    needs_budget = total_income * 0.5
    wants_budget = total_income * 0.3
    savings_budget = total_income * 0.2

    # Group by category and type
    summary = df_exp.groupby(['Category', 'CategoryType'])['Withdrawls'].sum().reset_index()

    # Calculate total spent per bucket
    bucket_totals = summary.groupby('CategoryType')['Withdrawls'].sum().to_dict()

    # Prepare recommendations
    recommendations = []
    for _, row in summary.iterrows():
        cat, cat_type, spent = row['Category'], row['CategoryType'], row['Withdrawls']
        # Proportional allocation within the bucket
        if cat_type == 'Need':
            bucket_total = bucket_totals.get('Need', 1)
            recommended = needs_budget * (spent / bucket_total) if bucket_total > 0 else 0
        elif cat_type == 'Want':
            bucket_total = bucket_totals.get('Want', 1)
            recommended = wants_budget * (spent / bucket_total) if bucket_total > 0 else 0
        elif cat_type == 'Saving':
            bucket_total = bucket_totals.get('Saving', 1)
            recommended = savings_budget * (spent / bucket_total) if bucket_total > 0 else 0
        else:
            recommended = 0

        recommendations.append({
            'Category': cat,
            'Type': cat_type,
            'Current Spending': spent,
            'Recommended Budget': recommended,
            'Difference': recommended - spent,
            'Percent Over/Under': ((spent - recommended) / recommended * 100) if recommended > 0 else 0
        })

    rec_df = pd.DataFrame(recommendations)
    st.subheader("Budget Recommendations (50/30/20 Rule)")
    st.dataframe(rec_df, use_container_width=True)


def goals():
    st.header("Goals")
    goals=['Emergency Fund','Retirement Fund','Travel Fund','Education Fund','Savings Fund']
    st.write("Set your goals for the year")
    col1,col2,col3=st.columns(3)
    with col1:
        goalName=st.text_input("Enter a goal name")
        goalType=st.selectbox("Select a goal",goals)
    with col2:
        goalAmount=st.number_input("Enter a goal amount",min_value=0)
        currentAmount=st.number_input("Enter current amount",min_value=0,max_value=goalAmount)
    with col3:
        deadline=st.date_input("DEADLINE!!!")
        priority=st.selectbox("Select a priority",['High','Medium','Low'])

    if st.button("Add Goal"):
        if goalName and goalAmount > 0:
            if 'goals' not in st.session_state:
                st.session_state.goals = {}
            goalID = str(uuid.uuid4())
            today = date.today()
            DayRemaining = (deadline - today).days
            st.session_state.goals[goalID]=({
                'goalName':goalName,
                'goalType':goalType,
                'goalAmount':goalAmount,
                'currentAmount':currentAmount,
                'deadline':deadline,
                'priority':priority,
                'DaysRemaining':DayRemaining,
                'progress':min((currentAmount/goalAmount)*100 if goalAmount > 0 else 0, 100),
                'Created At':today,
            })
            st.success("Goal added successfully!")
        else:
            st.error("Please enter a valid goal name and amount.")
    if 'goals' in st.session_state and st.session_state.goals:
        st.subheader("Your Goals")
        for goalID,goal in st.session_state.goals.items():
            st.write(f"Goal ID: {goalID}")
            st.write(f"Goal Name: {goal['goalName']}")
            st.write(f"Goal Type: {goal['goalType']}")
            st.write(f"Goal Amount: {goal['goalAmount']}")
            st.write(f"Current Amount: {goal['currentAmount']}")
            st.write(f"Deadline: {goal['deadline']}")
            st.write(f"Priority: {goal['priority']}")
            st.write(f"Days Remaining: {goal['DaysRemaining']}")
            st.write(f"Progress: {goal['progress']}%")
            st.write(f"Created At: {goal['Created At']}")
            st.write("---")
            updateAmount=st.number_input(f"Update Amount for ${goalName} ",min_value=0,value=goal['currentAmount'])
            if st.button(f'Update Goal {goalName}'):
                if updateAmount > goal['goalAmount']:
                    st.error("Amount cannot be greater than goal amount")
                else:
                    st.session_state.goals[goalID]['currentAmount'] = updateAmount
                    st.session_state.goals[goalID]['progress'] = min((updateAmount/goal['goalAmount'])*100, 100)
                    st.success("Goal updated successfully!")

category_mapping = {
    'ATM': 'Want',
    'Bill': 'Need',
    'Cash': 'Want',
    'Cheque': 'Want',
    'Commission': 'Want',
    'Debit Card': 'Want',
    'IMPS': 'Want',
    'Interest': 'Saving',
    'Miscellaneous': 'Want',
    'NEFT': 'Want',
    'Purchase': 'Want',
    'RTGS': 'Want',
    'Reversal': None,
    'Tax': 'Need',
    'Transfer': 'Saving',  # Or 'Want'/'Need' depending on your use
}

def assign_category_type(cat):
    return category_mapping.get(cat, 'Want')