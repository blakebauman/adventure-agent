import { ChatInterface } from './components/chat-interface';
import { ErrorBoundary } from './components/error-boundary';

function App() {
  return (
    <ErrorBoundary>
      <ChatInterface />
    </ErrorBoundary>
  );
}

export default App;

