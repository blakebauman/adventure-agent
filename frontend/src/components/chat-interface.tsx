import { useEffect, useRef } from 'react';
import { useChat } from '@/hooks/use-chat';
import { MessageList } from './message-list';
import { MessageInput } from './message-input';
import { HumanReviewModal } from './human-review-modal';
import { ThemeToggle } from './theme-toggle';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { ScrollArea } from './ui/scroll-area';
import { Toaster } from './ui/toaster';

export function ChatInterface() {
  const {
    messages,
    sendMessage,
    isLoading,
    needsReview,
    handleReview,
  } = useChat();
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  return (
    <div className="flex flex-col h-screen bg-background">
      <Card className="flex-1 flex flex-col m-4 mb-0">
        <CardHeader className="border-b">
          <div className="flex items-start justify-between">
            <div className="flex-1">
              <CardTitle className="text-2xl">Arizona Adventure Agent</CardTitle>
              <p className="text-sm text-muted-foreground">
                Plan your mountain bike adventures, bikepacking trips, and outdoor experiences
              </p>
              {import.meta.env.DEV && (
                <p className="text-xs text-muted-foreground mt-1">
                  API: {import.meta.env.VITE_API_URL || '/api (proxy)'}
                </p>
              )}
            </div>
            <ThemeToggle />
          </div>
        </CardHeader>
        <CardContent className="flex-1 flex flex-col p-0 overflow-hidden">
          <ScrollArea className="flex-1 p-4">
            <MessageList messages={messages} />
            <div ref={messagesEndRef} />
          </ScrollArea>
          <div className="border-t p-4">
            <MessageInput onSend={sendMessage} disabled={isLoading} />
          </div>
        </CardContent>
      </Card>
      {needsReview && (
        <HumanReviewModal
          onReview={handleReview}
          onClose={() => {}}
        />
      )}
      <Toaster />
    </div>
  );
}

