import React from 'react';

const ConversationLog = ({ logs }) => {
  return (
    <div className="conversation-log">
      <h2>Conversation Log</h2>
      {logs.map((log, index) => (
        <div key={index} className="log-entry">
          <strong>{log.role}:</strong> {log.content} <em>({log.timestamp})</em>
        </div>
      ))}
    </div>
  );
};

export default ConversationLog;