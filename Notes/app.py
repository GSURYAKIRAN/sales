
import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

# Page Configuration
st.set_page_config(
    page_title="Retail Sales Dashboard",
    page_icon="🛒",
    layout="wide"
)

# Load Dataset
df = pd.read_csv("Data/Retail Sales and Profit.csv")

df.columns = df.columns.str.strip()

st.write(df.columns.tolist())
# Convert Numeric Columns
for col in ['Quantity Ordered', 'Price Each', 'Cost price', 'turnover', 'profit']:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')

# Title
st.title("🛒 Retail Sales Dashboard")

# Sidebar
menu = st.sidebar.selectbox(
    "Select Analysis",
    [
        "Dashboard",
        "Product Analysis",
        "Category Analysis",
        "Correlation Analysis"
    ]
)

# Dashboard
if menu == "Dashboard":

    st.subheader("Dataset Preview")
    st.dataframe(df.head())

    st.subheader("Dataset Shape")
    st.write(df.shape)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Total Revenue",
            f"₹{df['turnover'].sum():,.0f}"
        )

    with col2:
        st.metric(
            "Total profit",
        f"₹{df['margin'].sum():,.0f}"
        )

    with col3:
        st.metric(
            "Quantity Sold",
            f"{df['Quantity Ordered'].sum():,.0f}"
        )

# Product Analysis
elif menu == "Product Analysis":

    st.subheader("Top 10 Products by Revenue")

    product_sales = (
        df.groupby("Product")["turnover"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
    )

    fig = px.bar(
        x=product_sales.index,
        y=product_sales.values,
        color=product_sales.values,
        title="Top 10 Products by Revenue"
    )

    st.plotly_chart(fig, use_container_width=True)

# Category Analysis
elif menu == "Category Analysis":

    st.subheader("Category Distribution")
    

    category = df["catégorie"].value_counts()

    fig = px.pie(
        values=category.values,
        names=category.index,
        hole=0.5,
        title="Category Distribution"
    )

    st.plotly_chart(fig, use_container_width=True)

# Correlation Analysis
elif menu == "Correlation Analysis":

    st.subheader("Correlation Heatmap")

    fig, ax = plt.subplots(figsize=(10, 6))

    sns.heatmap(
        df[
            [
                'Quantity Ordered',
                'Price Each',
                'Cost price',
                'turnover',
                'margin'
            ]
        ].corr(),
        annot=True,
        cmap="coolwarm",
        ax=ax
    )

    st.pyplot(fig)
    
    