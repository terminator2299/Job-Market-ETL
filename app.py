import streamlit as st
st.set_page_config(page_title="Job Market ETL & Analysis", layout="wide")

import requests
from bs4 import BeautifulSoup
import pandas as pd
import spacy
from collections import Counter
import io
import re

# Custom CSS for header and table
st.markdown("""
    <style>
    .main-header {
        background: linear-gradient(90deg, #4F8EF7 0%, #235390 100%);
        color: white;
        padding: 2rem 1rem 1rem 1rem;
        border-radius: 0 0 1rem 1rem;
        margin-bottom: 2rem;
        text-align: center;
    }
    .summary-card {
        background: #f0f4fa;
        border-radius: 1rem;
        padding: 1.5rem;
        margin-bottom: 2rem;
        display: flex;
        justify-content: space-around;
        font-size: 1.2rem;
        font-weight: 500;
    }
    .summary-item {
        margin: 0 2rem;
    }
    .stDataFrame th, .stDataFrame td {
        font-size: 1rem !important;
    }
    </style>
""", unsafe_allow_html=True)

# Load spaCy model for NER
@st.cache_resource
def load_spacy():
    return spacy.load('en_core_web_sm')
nlp = load_spacy()

# Header
st.markdown('<div class="main-header"><h1>Job Market ETL & Analysis</h1><h3>Scrape, Analyze, and Visualize Tech Jobs in Real Time</h3></div>', unsafe_allow_html=True)

# Sidebar: Job source, tech stack/keyword search, and location
st.sidebar.header('Search Jobs')
source = st.sidebar.selectbox('Job Source', ['Global (RemoteOK)', 'India (Indeed India)'])
search_term = st.sidebar.text_input('Enter tech stack or keyword (e.g., python, javascript, react, devops):', value='python')
if source == 'India (Indeed India)':
    location_filter = st.sidebar.text_input('Location (leave blank for all India):', value='')
else:
    st.sidebar.markdown('**Note:** RemoteOK only lists remote jobs.')
    location_filter = st.sidebar.text_input('Location (optional, for filtering results):', value='')

# Scrape jobs from RemoteOK for any tech stack
@st.cache_data(show_spinner=False)
def scrape_remoteok(keyword):
    url = f'https://remoteok.com/remote-{keyword}-jobs'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    jobs = []
    for tr in soup.find_all('tr', class_='job'):
        job = {}
        title_tag = tr.find('h2', itemprop='title')
        company_tag = tr.find('h3', itemprop='name')
        link_tag = tr.find('a', class_='preventLink', href=True)
        desc_tag = tr.find('td', class_='description')
        job['title'] = title_tag.text.strip() if title_tag else ''
        job['company'] = company_tag.text.strip() if company_tag else ''
        job['url'] = 'https://remoteok.com' + link_tag['href'] if link_tag else ''
        job['description'] = desc_tag.text.strip() if desc_tag else ''
        job['location'] = 'Remote'
        jobs.append(job)
    return jobs

# Scrape jobs from Indeed India for any tech stack and location
@st.cache_data(show_spinner=False)
def scrape_indeed_india(keyword, location):
    keyword_q = re.sub(r'\s+', '+', keyword.strip())
    location_q = re.sub(r'\s+', '+', location.strip()) if location.strip() else ''
    url = f'https://in.indeed.com/jobs?q={keyword_q}'
    if location_q:
        url += f'&l={location_q}'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    jobs = []
    for div in soup.find_all('div', class_='job_seen_beacon'):
        job = {}
        title_tag = div.find('h2', class_='jobTitle')
        company_tag = div.find('span', class_='companyName')
        location_tag = div.find('div', class_='companyLocation')
        link_tag = title_tag.find('a', href=True) if title_tag else None
        desc_tag = div.find('div', class_='job-snippet')
        job['title'] = title_tag.text.strip() if title_tag else ''
        job['company'] = company_tag.text.strip() if company_tag else ''
        job['url'] = 'https://in.indeed.com' + link_tag['href'] if link_tag else ''
        job['description'] = desc_tag.text.strip().replace('\n', ' ') if desc_tag else ''
        job['location'] = location_tag.text.strip() if location_tag else 'India'
        jobs.append(job)
    return jobs

# Scrape jobs based on user selection
with st.spinner(f'Scraping jobs for "{search_term}" from {source}...'):
    if source == 'Global (RemoteOK)':
        jobs = scrape_remoteok(search_term.lower())
    else:
        jobs = scrape_indeed_india(search_term, location_filter)
    for job in jobs:
        for key in ['title', 'company', 'url', 'description', 'location']:
            if key not in job:
                job[key] = ''
    df = pd.DataFrame(jobs)

# Fallback: If no jobs, allow user to upload or use sample data
if df.empty or 'title' not in df.columns or 'company' not in df.columns:
    st.error(f"No job data found for '{search_term}' in {source}. You can upload a CSV or use sample data.")
    uploaded_file = st.file_uploader("Upload a CSV file with columns: title, company, url, description, location", type=["csv"])
    use_sample = st.button("Use Sample Data")
    use_india_sample = st.button("Load Indian Sample Data (Demo Mode)")
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.success("Loaded uploaded data!")
    elif use_india_sample:
        india_sample_csv = '''title,company,url,description,location\nSoftware Engineer,TCS,https://tcs.com/job1,Work on backend systems for banking clients.,Bangalore\nFrontend Developer,Infosys,https://infosys.com/job2,React.js developer for enterprise web apps.,Pune\nData Scientist,Flipkart,https://flipkart.com/job3,Analyze e-commerce data and build ML models.,Bangalore\nDevOps Engineer,Wipro,https://wipro.com/job4,CI/CD pipelines and cloud infra automation.,Hyderabad\nBackend Developer,Zomato,https://zomato.com/job5,Python/Django backend for food delivery platform.,Gurgaon\nFull Stack Developer,Paytm,https://paytm.com/job6,Node.js and React full stack role.,Noida\nMobile App Developer,Swiggy,https://swiggy.com/job7,Flutter/React Native for food delivery app.,Bangalore\nQA Engineer,Freshworks,https://freshworks.com/job8,Manual and automation testing for SaaS products.,Chennai\nCloud Architect,Amazon India,https://amazon.in/job9,AWS cloud solutions for Indian enterprise clients.,Bangalore\nAI Engineer,InMobi,https://inmobi.com/job10,Build AI/ML features for ad tech.,Bangalore\n'''
        df = pd.read_csv(io.StringIO(india_sample_csv))
        st.success("Loaded Indian sample data!")
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
st.sidebar.header('Filters')
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

# --- Summary Card ---
total_jobs = len(filtered_df)
top_company = filtered_df['company'].value_counts().idxmax() if not filtered_df.empty else 'N/A'
top_location = 'N/A'
if 'locations' in filtered_df.columns and filtered_df['locations'].apply(lambda x: len(x) > 0).any():
    locations_flat = [loc for sublist in filtered_df['locations'] for loc in sublist]
    if locations_flat:
        top_location = pd.Series(locations_flat).value_counts().idxmax()

st.markdown(f'''
<div class="summary-card">
    <div class="summary-item">Total Jobs: <b>{total_jobs}</b></div>
    <div class="summary-item">Top Company: <b>{top_company}</b></div>
    <div class="summary-item">Top Location: <b>{top_location}</b></div>
</div>
''', unsafe_allow_html=True)

# --- Main Table ---
st.subheader('Job Listings')
def make_clickable(val):
    return f'<a href="{val}" target="_blank">View</a>' if val else ''

styled_table = filtered_df[['title', 'company', 'location', 'url', 'description']].copy()
styled_table['url'] = styled_table['url'].apply(make_clickable)
st.write(styled_table.to_html(escape=False, index=False), unsafe_allow_html=True)

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
