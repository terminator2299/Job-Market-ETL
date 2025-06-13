import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import MultiLabelBinarizer
from api_client import JobMarketAPI

st.set_page_config(
    page_title="🌍 Job Market Insights",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize API client
api_client = JobMarketAPI()

# Load data with caching
@st.cache_data(ttl=3600)  # Cache for 1 hour
def load_data(country='gb', category=''):
    return api_client.fetch_jobs(country=country, what=category)

# === Sidebar Filters ===
with st.sidebar:
    st.header("🔍 Filter Job Listings")

    # Country filter
    countries = api_client.get_available_countries()
    selected_country = st.selectbox(
        "Select Country:",
        options=countries,
        index=countries.index('gb')
    )
    
    # Category filter
    categories = api_client.get_available_categories()
    selected_category = st.selectbox(
        "Select Job Category:",
        options=[''] + categories
    )

    # Add a search box for specific job titles
    job_title = st.text_input("Search for specific job title (optional):")

    # Fetch data based on filters
    with st.spinner('Fetching job data...'):
        df = load_data(
            country=selected_country,
            category=selected_category if selected_category else job_title
        )

    if df.empty:
        st.error("""
        No data available for the selected filters. Try:
        1. Selecting a different country
        2. Using a different job category
        3. Entering a specific job title
        4. Checking if the API is accessible
        """)
        st.stop()

    st.success(f"Found {len(df)} jobs!")

    # Location filter
    locations = df['location'].dropna().unique()
    selected_locations = st.multiselect(
        "Select Location(s):",
        options=sorted(locations),
        default=sorted(locations)[:5] if len(locations) > 5 else sorted(locations)
    )
    
    # Role filter
    roles = df['title'].dropna().unique()
    selected_roles = st.multiselect(
        "Select Role(s):",
        options=sorted(roles),
        default=sorted(roles)[:5] if len(roles) > 5 else sorted(roles)
    )
    
    # Skills filter
    skills = set()
    df['skills'] = df['skills'].fillna('')
    for skill_list in df['skills']:
        for skill in skill_list.split(','):
            skills.add(skill.strip().lower())
    skills = sorted(list(skills))
    
    selected_skills = st.multiselect(
        "Filter by Skills:",
        options=skills
    )
    
    # Salary range filter
    min_salary = int(df['salary_min'].min())
    max_salary = int(df['salary_max'].max())
    salary_range = st.slider(
        "Select Salary Range ($):",
        min_value=min_salary,
        max_value=max_salary,
        value=(min_salary, max_salary),
        step=1000
    )

st.title("🌍 Job Market Insights Dashboard")

# Show data summary
st.info(f"""
📊 Data Summary:
- Total Jobs: {len(df)}
- Country: {df['country'].iloc[0] if not df.empty else 'N/A'}
- Date Range: {df['posted'].min()[:10] if not df.empty else 'N/A'} to {df['posted'].max()[:10] if not df.empty else 'N/A'}
""")

# Filter dataframe based on sidebar inputs
filtered_df = df[
    (df['location'].isin(selected_locations)) &
    (df['title'].isin(selected_roles)) &
    (df['salary_min'] >= salary_range[0]) &
    (df['salary_max'] <= salary_range[1])
]

if selected_skills:
    filtered_df = filtered_df[
        filtered_df['skills'].apply(
            lambda x: any(skill in x.lower() for skill in selected_skills)
        )
    ]

# === Tabs ===
tab1, tab2, tab3, tab4 = st.tabs([
    "💰 Salary Distribution",
    "🏢 Top Companies",
    "👔 Role Comparison",
    "🧩 Skills Correlation"
])

# --- Tab 1: Salary Distribution ---
with tab1:
    st.subheader("Salary Distribution for Filtered Jobs")
    if not filtered_df.empty:
        fig, ax = plt.subplots(figsize=(12, 5))
        sns.histplot(
            filtered_df['salary_min'], bins=30, kde=True,
            color='#1f77b4', ax=ax
        )
        ax.set_xlabel("Minimum Salary ($)")
        ax.set_ylabel("Number of Jobs")
        ax.grid(True, linestyle='--', alpha=0.5)
        st.pyplot(fig)
    else:
        st.warning("No data available for the selected filters.")

# --- Tab 2: Top Companies ---
with tab2:
    st.subheader("Top Companies Hiring (Filtered Data)")
    if not filtered_df.empty:
        top_companies = filtered_df['company'].value_counts().nlargest(10)
        fig, ax = plt.subplots(figsize=(12, 5))
        sns.barplot(
            x=top_companies.values, y=top_companies.index,
            palette="viridis", ax=ax
        )
        ax.set_xlabel("Number of Openings")
        ax.set_ylabel("Company")
        ax.grid(axis='x', linestyle='--', alpha=0.5)
        st.pyplot(fig)
    else:
        st.warning("No data available for the selected filters.")

# --- Tab 3: Role Comparison ---
with tab3:
    st.subheader("Role Comparison: Average Salaries")
    if not filtered_df.empty:
        avg_salary_by_role = filtered_df.groupby('title')[['salary_min', 'salary_max']].mean().sort_values('salary_min', ascending=False).head(10)

        fig, ax = plt.subplots(figsize=(12, 6))
        width = 0.4
        x = range(len(avg_salary_by_role))

        ax.bar(x, avg_salary_by_role['salary_min'], width=width, label='Min Salary', color='#ff7f0e')
        ax.bar([i + width for i in x], avg_salary_by_role['salary_max'], width=width, label='Max Salary', color='#2ca02c', alpha=0.7)
        
        ax.set_xticks([i + width / 2 for i in x])
        ax.set_xticklabels(avg_salary_by_role.index, rotation=45, ha='right')
        ax.set_ylabel("Average Salary ($)")
        ax.legend()
        ax.grid(axis='y', linestyle='--', alpha=0.5)
        st.pyplot(fig)
    else:
        st.warning("No data available for the selected filters.")

# --- Tab 4: Skills Correlation ---
with tab4:
    st.subheader("Skills Correlation Heatmap")
    if not filtered_df.empty:
        skills_lists = filtered_df['skills'].str.lower().str.split(',').apply(lambda x: [s.strip() for s in x if s.strip() != ''])
        mlb = MultiLabelBinarizer()
        skills_matrix = pd.DataFrame(mlb.fit_transform(skills_lists), columns=mlb.classes_, index=filtered_df.index)

        corr = skills_matrix.corr()

        fig, ax = plt.subplots(figsize=(12, 10))
        sns.heatmap(
            corr, cmap='coolwarm', ax=ax,
            center=0, square=True, cbar_kws={"shrink": .5},
            linewidths=0.5, linecolor='gray'
        )
        ax.set_title("Skill Correlation Matrix")
        st.pyplot(fig)
    else:
        st.warning("No data available for the selected filters.")
