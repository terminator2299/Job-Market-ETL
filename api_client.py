import requests
import pandas as pd
from config import ADZUNA_APP_ID, ADZUNA_API_KEY, ADZUNA_BASE_URL

class JobMarketAPI:
    def __init__(self):
        self.app_id = ADZUNA_APP_ID
        self.api_key = ADZUNA_API_KEY
        self.base_url = ADZUNA_BASE_URL

    def fetch_jobs(self, country='gb', results_per_page=100, what='', where=''):
        """
        Fetch jobs from Adzuna API
        """
        # Map country codes to their full names for better search
        country_mapping = {
            'gb': 'United Kingdom',
            'us': 'United States',
            'au': 'Australia',
            'br': 'Brazil',
            'ca': 'Canada',
            'de': 'Germany',
            'fr': 'France',
            'in': 'India',
            'it': 'Italy',
            'nl': 'Netherlands',
            'nz': 'New Zealand',
            'pl': 'Poland',
            'ru': 'Russia',
            'sg': 'Singapore',
            'es': 'Spain',
            'za': 'South Africa'
        }

        # Construct the correct URL for the country
        url = f"https://api.adzuna.com/v1/api/jobs/{country}/search/1"
        
        # Add country name to the search query for better results
        search_query = what
        if where:
            search_query = f"{what} in {where}"
        
        params = {
            'app_id': self.app_id,
            'app_key': self.api_key,
            'results_per_page': results_per_page,
            'what': search_query,
            'where': where,
            'sort_by': 'date',
            'sort_direction': 'down',
            'content-type': 'application/json'
        }

        try:
            print(f"Fetching data from: {url}")  # Debug print
            response = requests.get(url, params=params)
            print(f"Response status: {response.status_code}")  # Debug print
            
            if response.status_code == 404:
                print(f"No data available for country: {country}")
                return pd.DataFrame()
                
            response.raise_for_status()
            data = response.json()
            
            if not data.get('results'):
                print(f"No results found for the query: {search_query}")
                return pd.DataFrame()

            # Transform the data into a DataFrame
            jobs = []
            for job in data.get('results', []):
                # Extract salary information
                salary_min = job.get('salary_min', 0)
                salary_max = job.get('salary_max', 0)
                
                # Handle currency conversion if needed
                if country != 'gb' and salary_min > 0:
                    # You might want to add actual currency conversion here
                    # For now, we'll just use the values as is
                    pass

                jobs.append({
                    'title': job.get('title', ''),
                    'company': job.get('company_name', ''),
                    'location': job.get('location', {}).get('display_name', ''),
                    'salary_min': salary_min,
                    'salary_max': salary_max,
                    'description': job.get('description', ''),
                    'skills': ', '.join(job.get('category', {}).get('tag', [])),
                    'posted': job.get('created', ''),
                    'url': job.get('redirect_url', ''),
                    'country': country_mapping.get(country, country)
                })

            df = pd.DataFrame(jobs)
            print(f"Retrieved {len(df)} jobs")  # Debug print
            return df

        except requests.exceptions.RequestException as e:
            print(f"Error fetching data: {e}")
            return pd.DataFrame()
        except Exception as e:
            print(f"Unexpected error: {e}")
            return pd.DataFrame()

    def get_available_countries(self):
        """
        Get list of available countries
        """
        return ['gb', 'us', 'au', 'br', 'ca', 'de', 'fr', 'in', 'it', 'nl', 'nz', 'pl', 'ru', 'sg', 'es', 'za']

    def get_available_categories(self):
        """
        Get list of available job categories
        """
        return [
            'IT Jobs', 'Engineering Jobs', 'Science Jobs', 'Healthcare Jobs',
            'Finance Jobs', 'Marketing Jobs', 'Sales Jobs', 'Design Jobs',
            'Education Jobs', 'Legal Jobs', 'Management Jobs'
        ] 