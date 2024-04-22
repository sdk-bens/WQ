import React, { useState } from "react";
import "./data.css"; 

const DataPage = () => {
  const [profileHTML, setProfileHTML] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleExploreData = async () => {
    setLoading(true); 
    try {
      const response = await fetch("http://localhost:8000/profile-report");
      const report = await response.text();
      setProfileHTML(report);
    } catch (error) {
      console.error("Error fetching report:", error);
    } finally {
      setLoading(false); 
    }
  };

  return (
    <div className="data-page">
      <div className="header">
        <h1><strong>Knowledge Base</strong></h1>
        <p>
          <em><strong>Type:</strong> Cryptocurrency Article</em>
        </p>
        <p>
          <em><strong>Source:</strong> Wikipedia</em>
        </p>
        <p>
        <em><strong>Date:</strong> January 5ᵗʰ, 2024.</em>
        </p>

      </div>

      <div className="content">
        <section className="center-text">
          <p>
            Explore the cryptocurrency articles sourced from Wikipedia by clicking the button below.
          </p>
        </section>
      </div>

      <div className="buttons-container">
        {/* Button to fetch and display profiling report */}
        <button className="explore-button" onClick={handleExploreData}>Explore Data</button>
      </div>

      {/* Render loading indicator while fetching */}
      {loading && <div className="loading-indicator"></div>}

      {/* Render profile HTML */}
      {profileHTML && (
        <div className="profile-container" dangerouslySetInnerHTML={{ __html: profileHTML }}></div>
      )}
    </div>
  );
};

export default DataPage;

