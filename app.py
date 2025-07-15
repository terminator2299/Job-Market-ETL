import streamlit as st
import requests
import pandas as pd
import spacy
from collections import Counter
import io
import os
from dotenv import load_dotenv

# Load environment variables from .env file if present
load_dotenv()

# Load Adzuna API credentials from environment variables
ADZUNA_APP_ID = os.environ.get('ADZUNA_APP_ID')
ADZUNA_APP_KEY = os.environ.get('ADZUNA_APP_KEY')

if not ADZUNA_APP_ID or not ADZUNA_APP_KEY:
    st.error('Adzuna API credentials not found. Please set ADZUNA_APP_ID and ADZUNA_APP_KEY in your environment or .env file.')
    st.stop()

# Custom CSS for header, summary, and table
st.markdown("""
    <style>
    .main-header {
        background: linear-gradient(90deg, #4F8EF7 0%, #235390 100%);
        color: white;
        padding: 2rem 1rem 1rem 1rem;
        border-radius: 0 0 1rem 1rem;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 4px 16px rgba(79,142,247,0.15);
    }
    .summary-card {
        background: #f0f4fa;
        border-radius: 1rem;
        padding: 1.5rem 2rem;
        margin-bottom: 2rem;
        display: flex;
        justify-content: space-around;
        font-size: 1.2rem;
        font-weight: 500;
        box-shadow: 0 2px 8px rgba(79,142,247,0.08);
    }
    .summary-item {
        margin: 0 2rem;
        text-align: center;
    }
    .summary-icon {
        font-size: 2rem;
        margin-bottom: 0.2rem;
        display: block;
    }
    .stDataFrame th, .stDataFrame td {
        font-size: 1rem !important;
    }
    .job-table {
        border-radius: 1rem;
        overflow: hidden;
        box-shadow: 0 2px 8px rgba(79,142,247,0.08);
    }
    </style>
""", unsafe_allow_html=True)

# Load spaCy model for NER
@st.cache_resource
def load_spacy():
    return spacy.load('en_core_web_sm')
nlp = load_spacy()

# Header
st.title('Job Market ETL & Analysis')
st.markdown('Real-Time Indian Tech Jobs • Powered by Adzuna API')

# Sidebar: Only Adzuna API for Indian jobs
st.sidebar.header('🔎 Search Jobs')
st.sidebar.markdown('**Source:** India (Adzuna API, Real-Time)')
search_term = st.sidebar.text_input('Tech stack or keyword', value='', help='e.g., python, javascript, react, devops')
location_filter = st.sidebar.text_input('Location (leave blank for all India)', value='', help='e.g., Bangalore, Mumbai, Delhi')

# Adzuna API scraper for Indian jobs
@st.cache_data(show_spinner=False)
def scrape_adzuna_india(keyword, location):
    url = f'https://api.adzuna.com/v1/api/jobs/in/search/1'
    params = {
        'app_id': ADZUNA_APP_ID,
        'app_key': ADZUNA_APP_KEY,
        'results_per_page': 30,
        'what': keyword,
        'content-type': 'application/json',
    }
    if location.strip():
        params['where'] = location
    response = requests.get(url, params=params)
    jobs = []
    if response.status_code == 200:
        data = response.json()
        for res in data.get('results', []):
            job = {
                'title': res.get('title', ''),
                'company': res.get('company', {}).get('display_name', ''),
                'location': res.get('location', {}).get('display_name', ''),
                'description': res.get('description', ''),
                'url': res.get('redirect_url', '')
            }
            jobs.append(job)
    return jobs

# Scrape jobs using Adzuna only
with st.spinner(f'Fetching real-time jobs for "{search_term}" from Adzuna...'):
    jobs = scrape_adzuna_india(search_term, location_filter)
    for job in jobs:
        for key in ['title', 'company', 'url', 'description', 'location']:
            if key not in job:
                job[key] = ''
    df = pd.DataFrame(jobs)

# Fallback: If no jobs, allow user to upload or use sample data
if df.empty or 'title' not in df.columns or 'company' not in df.columns:
    st.error(f"No job data found for '{search_term}' in India (Adzuna API, Real-Time). You can upload a CSV or use sample data.")
    uploaded_file = st.file_uploader("Upload a CSV file with columns: title, company, url, description, location", type=["csv"])
    use_sample = st.button("Use Sample Data")
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.success("Loaded uploaded data!")
    elif use_sample:
        sample_csv = '''title,company,url,description,location\nPython Developer,Acme Corp,https://example.com/job1,We are looking for a Python Developer in New York.,New York\nData Scientist,Globex,https://example.com/job2,Remote Data Scientist role in San Francisco.,San Francisco\nBackend Engineer,Initech,https://example.com/job3,Backend Engineer needed in London.,London\n'''
        df = pd.read_csv(io.StringIO(sample_csv))
        st.success("Loaded sample data!")
    else:
        st.stop()

if 'description' not in df.columns:
    st.warning("No job descriptions found. Skipping NER extraction.")
    df['description'] = ""
    df['roles'] = [[] for _ in range(len(df))]
    df['skills'] = [[] for _ in range(len(df))]
    df['locations'] = [[] for _ in range(len(df))]
else:
    def extract_entities(text):
        doc = nlp(str(text))
        roles = [ent.text for ent in doc.ents if ent.label_ in ['ORG', 'PERSON', 'TITLE']]
        locations = [ent.text for ent in doc.ents if ent.label_ == 'GPE']
        skills = []  # Placeholder: can use keyword matching or custom NER for skills
        return roles, skills, locations
    df['roles'], df['skills'], df['locations'] = zip(*df['description'].fillna('').map(extract_entities))

# Sidebar filters for job title, company, and location
st.sidebar.header('🧰 Filters')
all_titles = sorted(df['title'].unique())
selected_titles = st.sidebar.multiselect('Job Title', all_titles, default=all_titles)
all_companies = sorted(df['company'].unique())
selected_companies = st.sidebar.multiselect('Company', all_companies, default=all_companies)
location_filter2 = st.sidebar.text_input('Filter by Location (e.g., India, Bangalore, Mumbai):', value='')

def location_match(row):
    if not location_filter2.strip():
        return True
    desc = str(row.get('description', '')).lower()
    locs = str(row.get('location', '')).lower()
    extracted_locs = ' '.join(row.get('locations', [])) if 'locations' in row else ''
    return (location_filter2.lower() in desc or
            location_filter2.lower() in locs or
            location_filter2.lower() in extracted_locs.lower())

filtered_df = df[
    df['title'].isin(selected_titles) &
    df['company'].isin(selected_companies)
]
filtered_df = filtered_df[filtered_df.apply(location_match, axis=1)]

# --- Dynamic Subtitle ---
st.markdown(f"<h4 style='color:#235390;margin-top:-1.5rem;margin-bottom:1.5rem;'>🔎 Showing jobs for <b>{search_term.title() or 'All Tech Stacks'}</b> in <b>{location_filter or 'India'}</b></h4>", unsafe_allow_html=True)

# --- Total Jobs Small Text ---
total_jobs = len(filtered_df)
st.markdown(f"<p style='color:#235390;font-size:1.1rem;margin-top:-1rem;margin-bottom:1.5rem;'>Total jobs found: <b>{total_jobs}</b></p>", unsafe_allow_html=True)

# --- Remove Top Location logic and UI ---
# (No top_location variable, no summary card for location)

# --- Main Table ---
st.subheader('Job Listings')
def make_clickable(val):
    return f'<a href="{val}" target="_blank">View</a>' if val else ''

styled_table = filtered_df[['title', 'company', 'location', 'url', 'description']].copy()
styled_table['url'] = styled_table['url'].apply(make_clickable)
st.write(styled_table.to_html(escape=False, index=False, classes='job-table'), unsafe_allow_html=True)

# --- Analysis: Top job titles, companies, locations ---
st.subheader('Analysis & Visualization')
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown('**Top Job Titles**')
    st.bar_chart(filtered_df['title'].value_counts().head(10))
with col2:
    st.markdown('**Top Companies**')
    st.bar_chart(filtered_df['company'].value_counts().head(10))
with col3:
    st.markdown('**Top Locations (NER)**')
    locations_flat = [loc for sublist in filtered_df['locations'] for loc in sublist]
    loc_counts = pd.Series(Counter(locations_flat)).sort_values(ascending=False).head(10)
    st.bar_chart(loc_counts)

# Download option
st.subheader('Download Data')
st.download_button('Download CSV', filtered_df.to_csv(index=False), 'job_listings.csv')

st.caption('Built with Python, Pandas, spaCy, and Streamlit')
