# Save this as app.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set Streamlit page config
st.set_page_config(page_title="Netflix Dataset Dashboard", layout="centered")

# Title
st.title("Netflix Dataset Dashboard 📺")

# Load Netflix dataset
df = pd.read_csv('netflix_titles.csv')

# Clean and process 'date_added' column
df['date_added'] = pd.to_datetime(df['date_added'].astype(str).str.strip(), errors='coerce')
df = df.dropna(subset=['date_added'])
df['year_added'] = df['date_added'].dt.year

# ========================
# Sidebar
# ========================
st.sidebar.header("Dashboard Filters")

# Content type filter
selected_type = st.sidebar.selectbox("Select content type", ["All", "Movie", "TV Show"])

# Chart toggles
show_type_chart = st.sidebar.checkbox("Show Type Comparison (Movies vs TV Shows)", value=True)
show_country_chart = st.sidebar.checkbox("Show Top 10 Countries", value=True)
show_year_chart = st.sidebar.checkbox("Show Yearly Content Additions", value=True)

# Apply content type filter
filtered_df = df.copy()
if selected_type != "All":
    filtered_df = filtered_df[filtered_df['type'] == selected_type]

# ========================
# Main Content Area
# ========================

# Chart 1: Type Comparison
if show_type_chart:
    st.subheader("Number of Movies vs TV Shows")
    type_counts = df['type'].value_counts()
    fig1, ax1 = plt.subplots()
    sns.barplot(x=type_counts.index, y=type_counts.values, ax=ax1, palette="pastel")
    ax1.set_ylabel("Count")
    ax1.set_title("Total Content by Type")
    st.pyplot(fig1)

# Chart 2: Top 10 Countries
if show_country_chart:
    st.subheader("Top 10 Countries Producing Netflix Content")
    top_countries = filtered_df['country'].value_counts().head(10)
    fig2, ax2 = plt.subplots()
    sns.barplot(x=top_countries.values, y=top_countries.index, ax=ax2, palette="muted")
    ax2.set_xlabel("Number of Titles")
    ax2.set_title(f"Top 10 Countries ({selected_type})")
    st.pyplot(fig2)

# Chart 3: Yearly Additions
if show_year_chart:
    st.subheader("Content Released Over the Years")
    yearly_counts = filtered_df['year_added'].value_counts().sort_index()
    fig3, ax3 = plt.subplots()
    sns.lineplot(x=yearly_counts.index, y=yearly_counts.values, ax=ax3, marker='o')
    ax3.set_ylabel("Number of Titles")
    ax3.set_xlabel("Year")
    ax3.set_title(f"Netflix Additions Over Time ({selected_type})")
    st.pyplot(fig3)

# Footer
st.markdown("---")
st.caption("📊 Built with Streamlit | Data: Netflix Titles Dataset (Kaggle)")
