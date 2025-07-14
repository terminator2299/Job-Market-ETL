import React, { useEffect, useState } from 'react';
import './App.css';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend } from 'recharts';

function App() {
  const [jobs, setJobs] = useState([]);
  const [analysis, setAnalysis] = useState({ top_titles: {}, top_companies: {} });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchData() {
      setLoading(true);
      const jobsRes = await fetch('http://localhost:5000/api/jobs');
      const jobsData = await jobsRes.json();
      setJobs(jobsData);
      const analysisRes = await fetch('http://localhost:5000/api/analysis');
      const analysisData = await analysisRes.json();
      setAnalysis(analysisData);
      setLoading(false);
    }
    fetchData();
  }, []);

  // Prepare data for charts
  const titlesData = Object.entries(analysis.top_titles).map(([name, count]) => ({ name, count }));
  const companiesData = Object.entries(analysis.top_companies).map(([name, count]) => ({ name, count }));

  return (
    <div className="App">
      <header className="App-header">
        <h1>Job Market Scraper & Analyzer</h1>
      </header>
      <main>
        {loading ? (
          <p>Loading...</p>
        ) : (
          <>
            <section>
              <h2>Job Listings</h2>
              <table className="job-table">
                <thead>
                  <tr>
                    <th>Title</th>
                    <th>Company</th>
                    <th>Link</th>
                  </tr>
                </thead>
                <tbody>
                  {jobs.map((job, idx) => (
                    <tr key={idx}>
                      <td>{job.title}</td>
                      <td>{job.company}</td>
                      <td><a href={job.url} target="_blank" rel="noopener noreferrer">View</a></td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </section>
            <section>
              <h2>Analysis</h2>
              <div className="analysis-section">
                <div style={{ width: '100%', maxWidth: 500, margin: '0 auto' }}>
                  <h3>Top Job Titles</h3>
                  <ResponsiveContainer width="100%" height={250}>
                    <BarChart data={titlesData} layout="vertical" margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis type="number" allowDecimals={false} />
                      <YAxis dataKey="name" type="category" width={150} />
                      <Tooltip />
                      <Legend />
                      <Bar dataKey="count" fill="#8884d8" name="Count" />
                    </BarChart>
                  </ResponsiveContainer>
                </div>
                <div style={{ width: '100%', maxWidth: 500, margin: '0 auto', marginTop: 40 }}>
                  <h3>Top Companies</h3>
                  <ResponsiveContainer width="100%" height={250}>
                    <BarChart data={companiesData} layout="vertical" margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis type="number" allowDecimals={false} />
                      <YAxis dataKey="name" type="category" width={150} />
                      <Tooltip />
                      <Legend />
                      <Bar dataKey="count" fill="#82ca9d" name="Count" />
                    </BarChart>
                  </ResponsiveContainer>
                </div>
              </div>
            </section>
          </>
        )}
      </main>
    </div>
  );
}

export default App;
