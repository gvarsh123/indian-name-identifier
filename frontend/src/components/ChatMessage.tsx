import React from 'react';
import { Avatar } from '@radix-ui/react-avatar';

interface ChatMessageProps {
  role: 'user' | 'assistant';
  content: string;
}

const ChatMessage: React.FC<ChatMessageProps> = ({ role, content }) => {
  return (
    <div className={`flex items-start space-x-3 ${role === 'user' ? 'justify-end' : 'justify-start'}`}>
      {role === 'assistant' && (
        <Avatar className="w-8 h-8 rounded-full bg-primary text-primary-foreground flex items-center justify-center">
          L
        </Avatar>
      )}
      <div className={`max-w-[80%] p-3 rounded-lg ${
        role === 'user' 
          ? 'bg-primary text-primary-foreground' 
          : 'bg-muted text-muted-foreground'
      }`}>
        <p className="text-sm">{content}</p>
      </div>
      {role === 'user' && (
        <Avatar className="w-8 h-8 rounded-full bg-primary text-primary-foreground flex items-center justify-center">
          U
        </Avatar>
      )}
    </div>
  );
};

export default ChatMessage; 