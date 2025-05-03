import React from 'react';

const ChatHeader: React.FC = () => {
  return (
    <div className="flex items-center justify-between p-4 border-b border-border">
      <h1 className="text-xl font-semibold">Chat with Llama</h1>
      <div className="flex items-center space-x-2">
        <span className="text-sm text-muted-foreground">Powered by Llama3.2</span>
      </div>
    </div>
  );
};

export default ChatHeader; 