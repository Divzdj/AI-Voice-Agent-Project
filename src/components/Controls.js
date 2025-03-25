import React from 'react';

const Controls = ({ onStart, onStop, onRefresh }) => {
  return (
    <div className="controls">
      <button onClick={onStart}>Start</button>
      <button onClick={onStop}>Stop</button>
      <button onClick={onRefresh}>Refresh</button>
    </div>
  );
};

export default Controls;