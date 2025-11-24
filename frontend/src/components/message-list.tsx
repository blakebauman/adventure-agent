import { Message } from '@/types/adventure';
import { Card, CardContent } from './ui/card';
import { AdventurePlanView } from './adventure-plan-view';
import { Loader2 } from 'lucide-react';

interface MessageListProps {
  messages: Message[];
}

export function MessageList({ messages }: MessageListProps) {
  if (messages.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center h-full text-center p-8">
        <h2 className="text-2xl font-semibold mb-2">Welcome to Adventure Agent</h2>
        <p className="text-muted-foreground mb-4">
          Ask me about mountain bike trails, bikepacking routes, or outdoor adventures in Arizona.
        </p>
        <div className="text-sm text-muted-foreground space-y-1">
          <p>Try asking:</p>
          <ul className="list-disc list-inside space-y-1">
            <li>"Plan a 3-day mountain bike trip in Sedona"</li>
            <li>"What are the best bikepacking routes near Flagstaff?"</li>
            <li>"Find intermediate trails in Payson"</li>
          </ul>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      {messages.map((message) => (
        <div
          key={message.id}
          className={`flex ${
            message.role === 'user' ? 'justify-end' : 'justify-start'
          }`}
        >
          <Card
            className={`max-w-[80%] ${
              message.role === 'user'
                ? 'bg-primary text-primary-foreground'
                : 'bg-card'
            }`}
          >
            <CardContent className="p-4">
              {message.role === 'system' ? (
                <p className="text-sm text-muted-foreground">{message.content}</p>
              ) : message.role === 'user' ? (
                <p className="text-sm">{message.content}</p>
              ) : (
                <div className="space-y-2">
                  {message.isStreaming && (
                    <div className="flex items-center gap-2 text-sm text-muted-foreground mb-2">
                      <Loader2 className="h-4 w-4 animate-spin" />
                      <span>Planning your adventure...</span>
                      <span className="text-xs">(This may take a minute)</span>
                    </div>
                  )}
                  {!message.isStreaming && message.adventurePlan && (
                    <div className="text-xs text-muted-foreground mb-2 pb-2 border-b">
                      ✓ Adventure plan complete
                    </div>
                  )}
                  {message.adventurePlan ? (
                    <AdventurePlanView plan={message.adventurePlan} />
                  ) : message.content.trim() ? (
                    <div className="prose prose-sm max-w-none">
                      {message.content.split('\n').map((line, i) => (
                        <p key={i} className="mb-2 last:mb-0">
                          {line.startsWith('**') && line.endsWith('**') ? (
                            <strong className="font-semibold">
                              {line.slice(2, -2)}
                            </strong>
                          ) : (
                            line
                          )}
                        </p>
                      ))}
                    </div>
                  ) : !message.isStreaming ? (
                    <div className="text-sm text-muted-foreground italic">
                      Adventure planning completed, but no plan details were generated. Please try again or rephrase your request.
                    </div>
                  ) : null}
                </div>
              )}
            </CardContent>
          </Card>
        </div>
      ))}
    </div>
  );
}

