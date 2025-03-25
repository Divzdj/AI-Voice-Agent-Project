import React from 'react';

const RealTimeStatus = ({ status, currentCaller }) => {
  return (
    <div className="real-time-status">
      <h2>Real-Time Status</h2>
      <p>Status: {status}</p>
      <p>Current Caller: {currentCaller}</p>
    </div>
  );
};

export default RealTimeStatus;