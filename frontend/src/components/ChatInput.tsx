import React from 'react';
import { Send } from 'lucide-react';

interface ChatInputProps {
  value: string;
  onChange: (e: React.ChangeEvent<HTMLInputElement>) => void;
  onSubmit: (e: React.FormEvent) => void;
  disabled?: boolean;
}

const ChatInput: React.FC<ChatInputProps> = ({ value, onChange, onSubmit, disabled }) => {
  return (
    <form onSubmit={onSubmit} className="flex items-center space-x-2">
      <input
        type="text"
        value={value}
        onChange={onChange}
        disabled={disabled}
        placeholder="Type your message..."
        className="flex-1 p-2 rounded-lg border border-border bg-background text-foreground focus:outline-none focus:ring-2 focus:ring-ring"
      />
      <button
        type="submit"
        disabled={disabled || !value.trim()}
        className="p-2 rounded-lg bg-primary text-primary-foreground hover:bg-primary/90 disabled:opacity-50 disabled:cursor-not-allowed"
      >
        <Send className="w-5 h-5" />
      </button>
    </form>
  );
};

export default ChatInput; 