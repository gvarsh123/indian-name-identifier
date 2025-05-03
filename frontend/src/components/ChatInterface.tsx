import React, { useState, useRef, useEffect } from 'react';
import ChatMessage from './ChatMessage';
import ChatInput from './ChatInput';
import ChatSuggestion from './ChatSuggestion';
import LoadingDots from './LoadingDots';
import axios from 'axios';
import { Plus, MessageSquare, ChevronRight } from 'lucide-react';

interface Message {
  role: 'user' | 'assistant';
  content: string;
}

interface Chat {
  id: string;
  title: string;
  messages: Message[];
  createdAt: number;
}

const ChatInterface: React.FC = () => {
  const [chats, setChats] = useState<Chat[]>(() => {
    const saved = localStorage.getItem('chats');
    return saved ? JSON.parse(saved) : [];
  });
  const [currentChatId, setCurrentChatId] = useState<string>(() => {
    const saved = localStorage.getItem('currentChatId');
    return saved || '';
  });
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const currentChat = chats.find(chat => chat.id === currentChatId) || {
    id: '',
    title: '',
    messages: [],
    createdAt: Date.now()
  };

  useEffect(() => {
    localStorage.setItem('chats', JSON.stringify(chats));
  }, [chats]);

  useEffect(() => {
    localStorage.setItem('currentChatId', currentChatId);
  }, [currentChatId]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [currentChat.messages]);

  const startNewChat = () => {
    const newChat: Chat = {
      id: Date.now().toString(),
      title: 'New Chat',
      messages: [],
      createdAt: Date.now()
    };
    setChats(prev => [...prev, newChat]);
    setCurrentChatId(newChat.id);
    setInput('');
    setIsLoading(false);
  };

  const switchChat = (chatId: string) => {
    setCurrentChatId(chatId);
    setInput('');
    setIsLoading(false);
  };

  const updateChatTitle = (chatId: string, newTitle: string) => {
    setChats(prev => prev.map(chat => 
      chat.id === chatId ? { ...chat, title: newTitle } : chat
    ));
  };

  const handleSendMessage = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim()) return;

    const userMessage: Message = { role: 'user', content: input.trim() };
    const updatedMessages = [...currentChat.messages, userMessage];
    
    // Update chat with new message
    setChats(prev => prev.map(chat => 
      chat.id === currentChatId 
        ? { ...chat, messages: updatedMessages } 
        : chat
    ));

    // Update title if it's the first message
    if (currentChat.messages.length === 0) {
      updateChatTitle(currentChatId, input.trim().slice(0, 30) + '...');
    }

    setInput('');
    setIsLoading(true);

    try {
      const requestData = {
        message: userMessage.content,
        session_id: currentChatId
      };

      console.log('Sending request to backend:', requestData);

      const response = await axios.post('http://localhost:8000/api/chat', requestData, {
        headers: {
          'Content-Type': 'application/json'
        }
      });

      console.log('Received response from backend:', response.data);

      const assistantMessage: Message = {
        role: 'assistant',
        content: response.data.response
      };

      // Update chat with assistant's response
      setChats(prev => prev.map(chat => 
        chat.id === currentChatId 
          ? { ...chat, messages: [...updatedMessages, assistantMessage] } 
          : chat
      ));
    } catch (error) {
      console.error('Error sending message:', error);
      const errorMessage: Message = {
        role: 'assistant',
        content: 'Sorry, there was an error processing your message.'
      };
      setChats(prev => prev.map(chat => 
        chat.id === currentChatId 
          ? { ...chat, messages: [...updatedMessages, errorMessage] } 
          : chat
      ));
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex h-screen bg-background">
      {/* Sidebar */}
      <div className="w-64 border-r border-border bg-sidebar-background text-sidebar-foreground">
        <div className="p-4">
          <button
            onClick={startNewChat}
            className="w-full flex items-center space-x-2 p-2 rounded-lg bg-sidebar-primary text-sidebar-primary-foreground hover:bg-sidebar-primary/90"
          >
            <Plus className="w-4 h-4" />
            <span>New Chat</span>
          </button>
        </div>
        <div className="overflow-y-auto h-[calc(100vh-4rem)]">
          {chats.map(chat => (
            <button
              key={chat.id}
              onClick={() => switchChat(chat.id)}
              className={`w-full flex items-center space-x-2 p-3 hover:bg-sidebar-accent hover:text-sidebar-accent-foreground ${
                chat.id === currentChatId ? 'bg-sidebar-accent text-sidebar-accent-foreground' : ''
              }`}
            >
              <MessageSquare className="w-4 h-4" />
              <span className="truncate">{chat.title}</span>
              {chat.id === currentChatId && <ChevronRight className="w-4 h-4 ml-auto" />}
            </button>
          ))}
        </div>
      </div>

      {/* Main Chat Area */}
      <div className="flex-1 flex flex-col">
        <div className="flex-1 overflow-y-auto p-4 space-y-4">
          {currentChat.messages.map((message, index) => (
            <ChatMessage
              key={index}
              role={message.role}
              content={message.content}
            />
          ))}
          {isLoading && <LoadingDots />}
          <div ref={messagesEndRef} />
        </div>
        <div className="p-4 border-t border-border">
          <ChatInput
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onSubmit={handleSendMessage}
            disabled={isLoading}
          />
          <div className="mt-4 grid grid-cols-2 gap-2">
            <ChatSuggestion
              text="What can you do?"
              onClick={() => setInput("What can you do?")}
            />
            <ChatSuggestion
              text="Tell me a joke"
              onClick={() => setInput("Tell me a joke")}
            />
          </div>
        </div>
      </div>
    </div>
  );
};

export default ChatInterface; 