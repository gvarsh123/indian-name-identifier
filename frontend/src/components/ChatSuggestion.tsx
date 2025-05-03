import React from 'react';

interface ChatSuggestionProps {
  text: string;
  onClick: () => void;
}

const ChatSuggestion: React.FC<ChatSuggestionProps> = ({ text, onClick }) => {
  return (
    <button
      onClick={onClick}
      className="p-2 rounded-lg bg-muted text-muted-foreground hover:bg-muted/80 transition-colors text-sm"
    >
      {text}
    </button>
  );
};

export default ChatSuggestion; 