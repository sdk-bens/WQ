import "./SearchResult.css";

export const SearchResult = ({ result }) => {
  const handleCopyText = (text) => {
    navigator.clipboard.writeText(text)
      .then(() => {
        alert(`"${text}" copied to clipboard!`);
      })
      .catch((error) => {
        console.error('Unable to copy text:', error);
        alert(`Failed to copy "${text}" to clipboard`);
      });
  };

  return (
    <div
      className="search-result"
      onClick={(e) => handleCopyText(result)}
    >
      {result}
    </div>
  );
};




