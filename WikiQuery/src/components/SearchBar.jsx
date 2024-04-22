import React, { useState } from "react";
import { FaBitcoin } from 'react-icons/fa'
import { BsArrowRightSquare } from 'react-icons/bs'
import { MdMic } from 'react-icons/md' 
import "./SearchBar.css";

export const SearchBar = ({ setResults }) => {
  const [input, setInput] = useState("");
  const [apiResponse, setApiResponse] = useState(null);
  const [listening, setListening] = useState(false); // State to track if microphone is listening
  const recognition = new window.webkitSpeechRecognition(); // Creating a new instance of speech recognition

  recognition.lang = "en-US"; // Set the language for speech recognition

  const fetchData = (value) => {
    if (value.trim() !== "") {
      fetch(`http://localhost:8000/generate_response?question=${encodeURIComponent(value)}`)
        .then((response) => response.json())
        .then((data) => {
          const results = data.response ? [capitalizeString(data.response)] : [];
          setResults(results);
          setApiResponse(capitalizeString(data.response));
        })
        .catch((error) => {
          console.error("Error fetching data:", error);
          setResults([]);
          setApiResponse(null);
        });
    } else {
      setResults([]);
      setApiResponse(null);
    }
  };

  const capitalizeString = (str) => {
    return str.charAt(0).toUpperCase() + str.slice(1);
  };

  const handleSearch = () => {
    fetchData(input);
  };

  const handleVoiceSearch = () => {
    if (!listening) {
      setListening(true); // Set listening state to true
      recognition.start(); // Start speech recognition
      recognition.onresult = (event) => {
        const transcript = event.results[0][0].transcript; // Get the transcript of the spoken words
        setInput(transcript); // Set the input value to the transcript
        fetchData(transcript); // Fetch data based on the transcript
        setListening(false); // Set listening state back to false
      };
    } else {
      recognition.stop(); // Stop speech recognition if already listening
      setListening(false); // Set listening state back to false
    }
  };

  const handleChange = (value) => {
    setInput(value);
    if (value.trim() === "") {
      setResults([]);
      setApiResponse(null);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === "Enter") {
      fetchData(input);
    }
  };

  const handleSearchIconClick = () => {
    fetchData(input);
  };

  return (
    <div>
      <div className="input-wrapper">
        <FaBitcoin size={50} id="search-icon" onClick={handleSearch} />
        <input
          placeholder=" Ask WikiQuery"
          value={input}
          onChange={(e) => handleChange(e.target.value)}
          onKeyDown={handleKeyPress}
        />
        <BsArrowRightSquare size={30} id="arrow-icon" onClick={handleSearchIconClick} />
        <MdMic
          size={30}
          id="mic-icon"
          onClick={handleVoiceSearch}
          style={{ color: listening ? "red" : "black" }} // Change mic icon color based on listening state
        />
      </div>
      {apiResponse && (
        <div className="response-wrapper">
          
        </div>
      )}
    </div>
  );
};

export default SearchBar;

