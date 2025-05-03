import React from 'react';

const LoadingDots: React.FC = () => {
  return (
    <div className="flex items-center space-x-2">
      <div className="dot-flashing" />
    </div>
  );
};

export default LoadingDots; 