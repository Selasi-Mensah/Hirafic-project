import React from 'react';

const ErrorState = ({ message }) => (
  <div className="text-red-400 p-4 text-center bg-red-900/20 rounded-lg">
    {message}
  </div>
);

export default ErrorState;