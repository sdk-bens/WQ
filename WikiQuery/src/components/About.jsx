
import React from "react";
import "./about.css"; 

const About = () => {
  return (
    <div id="about" className="page">
      <div className="header">
        <h1>WikiQuery: Information Retrieval with Precision and Ease</h1>
        <p><strong>Seddik Benaissa</strong>, Northeastern University</p>
        <p><em>Spring, 2024</em></p>
      </div>

      <div className="content">
        <section>
          <h2>What is WikiQuery</h2>
          <p>In the era of big data and new information emerging daily, the limitations of traditional search systems, especially when seeking specific answers on platforms like Wikipedia, are evident. WikiQuery is a solution to enhance the search experience, specifically addressing the challenge users face in obtaining accurate and direct answers to their questions. This platform designed to offer precise responses for any question related to digital currencies through a hybrid approach, integrating a vector database and a Large Language Model (LLM).</p>
        </section>

        <section>
          <h2>WikiQuery Objective</h2>
          <p>The primary goal of WikiQuery is to provide users interested in digital currencies with a streamlined and efficient method of obtaining accurate information to specific queries. Unlike traditional searches on platforms like Wikipedia, WikiQuery aims to offer direct answers to user questions, eliminating the need for users to navigate through articles that may or may not contain the desired information.</p>
        </section>
      </div>
    </div>
  );
};

export default About;
