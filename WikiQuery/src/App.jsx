import React, { useState } from "react";
import "./App.css";
import { SearchBar } from "./components/SearchBar";
import { SearchResultsList } from "./components/SearchResultsList";
import About from "./components/About";
import DataPage from "./components/DataPage"; 

function App() {
  const [results, setResults] = useState([]);
  const [darkMode, setDarkMode] = useState(false);
  const [menuOpen, setMenuOpen] = useState(false);
  const [currentPage, setCurrentPage] = useState("");

  const toggleDarkMode = () => {
    setDarkMode((prevMode) => !prevMode);
  };

  const toggleMenu = () => {
    setMenuOpen(!menuOpen);
  };

  const handleMenuClick = (page) => {
    setCurrentPage(page);
    setMenuOpen(false);
  };

  return (
    <div className={`App ${darkMode ? 'dark-mode' : ''}`}>
      <div className="top-menu">
        <div className={`menu-icon ${menuOpen ? 'open' : ''}`} onClick={toggleMenu}>
          <div className="menu-line"></div>
          <div className="menu-line"></div>
          <div className="menu-line"></div>
        </div>
        <ul className={`menu-list ${menuOpen ? 'open' : ''}`}>
          <li><a href="#about" onClick={() => handleMenuClick("about")}>About</a></li>
          <li><a href="#data" onClick={() => handleMenuClick("data")}>Data</a></li>
          <li><a href="#search" onClick={() => handleMenuClick("search")}>Search</a></li>
        </ul>
      </div>
      {currentPage === "about" && <About />}
      {currentPage === "data" && <DataPage />} {/* Render DataPage component when currentPage is "data" */}
      {currentPage === "search" && (
        <div className="search-bar-container">
          <SearchBar setResults={setResults} />
          {results && results.length > 0 && <SearchResultsList results={results} />}
        </div>
      )}
      {currentPage !== "about" && currentPage !== "search" && currentPage !== "data" && (
        <div className="search-bar-container">
          <SearchBar setResults={setResults} />
          {results && results.length > 0 && <SearchResultsList results={results} />}
        </div>
      )}
    </div>
  );
}

export default App;