# Job Market ETL & Dashboard Project

## Overview
This project extracts, transforms, and loads job market data from multiple sources to provide actionable insights on job openings, salaries, companies hiring, and skills correlations. It includes an interactive Streamlit dashboard for exploring and visualizing job market trends dynamically.

## Features
- **Data Processing Pipeline:** ETL scripts to clean and unify job data from multiple countries and sources.
- **Interactive Dashboard:**  
  - Salary distribution histograms  
  - Top hiring companies bar charts  
  - Role-wise salary comparison  
  - Skill correlation heatmap  
- **Custom Filters:** Filter by location, role, salary range, and skills to refine data views.
- **Real-time Visualization:** Dynamic update of charts and data based on user selections.

## Technologies Used
- Python (pandas, numpy, scikit-learn)
- Streamlit for interactive dashboard
- Seaborn and Matplotlib for visualization
- Pydeck (planned for geo visualizations)
- Git for version control

## Getting Started

### Prerequisites
- Python 3.8+
- pip

### Installation
1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/Job-Market-ETL.git
   cd Job-Market-ETL
   ```

2. **Create and activate a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # macOS/Linux
   .\venv\Scripts\activate   # Windows
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the dashboard**
   ```bash
   streamlit run notebooks/dashboard.py
   ```

## Project Structure
```
Job-Market-ETL/
│
├── data/                   # Raw and processed datasets
├── notebooks/              # Streamlit app and analysis scripts
│   └── dashboard.py        # Main dashboard app
├── scripts/                # ETL and data processing scripts
├── requirements.txt        # Python dependencies
└── README.md               # Project documentation
```

## How to Use
1. Use sidebar filters to select locations, job roles, salary ranges, and skills.
2. Explore different tabs for salary distributions, top companies hiring, role-based salary comparisons, and skills correlation heatmaps.
3. Insights dynamically update based on filters.

## Future Improvements
- Add geo-location based heatmaps for job distribution.
- Implement automated data refresh from live job portals.
- Expand skill correlation analysis with interactive network graphs.
- Expand skill correlation analysis with interactive network graphs.
