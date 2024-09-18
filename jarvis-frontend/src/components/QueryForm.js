import React, { useState } from 'react';
import { queryAPI } from '../api';

const QueryForm = () => {
  const [query, setQuery] = useState('');
  const [response, setResponse] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const result = await queryAPI(query);
      setResponse(result.response);
    } catch (error) {
      setResponse('Error querying API');
    }
  };

  return (
    <div>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Enter your query"
        />
        <button type="submit">Submit</button>
      </form>
      {response && <div>{response}</div>}
    </div>
  );
};

export default QueryForm;