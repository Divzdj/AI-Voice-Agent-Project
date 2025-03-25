import React, { useEffect, useState } from "react";
import axios from "axios";
import "./App.css";

const App = () => {
  const [conversationLog, setConversationLog] = useState([]);

  useEffect(() => {
    const fetchConversationLog = async () => {
      try {
        const response = await axios.get("/conversation-log");
        setConversationLog(response.data);
      } catch (error) {
        console.error("Error fetching conversation log:", error);
      }
    };

    fetchConversationLog();
  }, []);

  return (
    <div className="App">
      <header className="App-header">
        <h1>Live Conversation Log</h1>
      </header>
      <main>
        {conversationLog.length > 0 ? (
          <ul>
            {conversationLog.map((entry, index) => (
              <li key={index}>
                <strong>{entry.role}:</strong> {entry.content}
              </li>
            ))}
          </ul>
        ) : (
          <p>No conversation data available.</p>
        )}
      </main>
    </div>
  );
};

export default App;