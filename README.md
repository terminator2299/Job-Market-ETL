# 🇮🇳 Job Market ETL & Analysis (India, Real-Time)

A modern Streamlit dashboard to search, analyze, and visualize real-time Indian tech jobs using the Adzuna API. Showcases ETL, NLP, and data visualization skills with a beautiful, interactive UI.

---

## 🚀 Features
- **Real-time Indian job search** (powered by Adzuna API)
- Filter by tech stack, location, job title, and company
- NLP-based extraction of roles and locations from job descriptions (spaCy)
- Interactive analytics: top job titles, companies, and locations
- Download filtered job data as CSV
- Clean, modern, and mobile-friendly UI
- Secure: API credentials loaded from `.env` (never hardcoded)

---

## 🛠️ Setup Instructions

1. **Clone the repo:**
   ```sh
   git clone <your-repo-url>
   cd Job-Market-ETL
   ```

2. **Create and activate a virtual environment (optional but recommended):**
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

4. **Set up Adzuna API credentials:**
   - Register for a free API key at [Adzuna Developer Portal](https://developer.adzuna.com/)
   - Create a `.env` file in your project root:
     ```
     ADZUNA_APP_ID=your_app_id
     ADZUNA_APP_KEY=your_app_key
     ```

5. **Run the Streamlit app:**
   ```sh
   streamlit run app.py
   ```

6. **Open the app in your browser:**
   - Usually at [http://localhost:8501](http://localhost:8501)

---

## 📝 Usage
- Enter a tech stack or keyword (e.g., `python`, `react`, `data science`)
- (Optional) Enter a location (e.g., `Bangalore`, `Mumbai`, or leave blank for all India)
- Use sidebar filters to further refine by job title or company
- Download the filtered job data as CSV
- All API credentials are loaded securely from `.env`

---

## 🔒 Security
- **Never commit your `.env` file or API keys to git!**
- `.gitignore` is set up to protect secrets and virtual environments

---

## 📦 Dependencies
- streamlit
- pandas
- requests
- python-dotenv
- spacy

---

## 🙏 Credits
- [Adzuna API](https://developer.adzuna.com/) for real-time job data
- [spaCy](https://spacy.io/) for NLP
- [Streamlit](https://streamlit.io/) for the dashboard

---

## 📄 License
MIT License (see LICENSE file)

