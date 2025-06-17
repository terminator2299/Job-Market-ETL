# Job Market ETL Dashboard

A real-time job market insights dashboard that fetches data from the Adzuna API to provide up-to-date information about job opportunities, salaries, and market trends.

## Preview

Check out here - LiveLink(https://job-market-etl.streamlit.app/)

## Features

- Real-time job market data from Adzuna API
- Interactive filters for country, job category, location, and skills
- Salary distribution analysis
- Top companies hiring analysis
- Role comparison with salary ranges
- Skills correlation analysis
- Responsive and user-friendly interface

## Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd Job-Market-ETL
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure API credentials:
   - Sign up for an Adzuna API key at https://developer.adzuna.com/
   - Update the `config.py` file with your API credentials:
     ```python
     ADZUNA_APP_ID = "your_app_id_here"
     ADZUNA_API_KEY = "your_api_key_here"
     ```

5. Run the application:
```bash
streamlit run app.py
```

## Usage

1. Select a country from the dropdown menu
2. Choose a job category or enter a specific job title
3. Use the filters in the sidebar to narrow down results:
   - Location
   - Job roles
   - Required skills
   - Salary range
4. Explore the different tabs for various insights:
   - Salary Distribution
   - Top Companies
   - Role Comparison
   - Skills Correlation

## Technologies Used

- Python
- Streamlit
- Pandas
- Matplotlib
- Seaborn
- Scikit-learn
- Adzuna API

## Contributing

Feel free to submit issues and enhancement requests!

## License

This project is licensed under the MIT License - see the LICENSE file for details.

