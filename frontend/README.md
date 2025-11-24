# Adventure Agent Frontend

A modern React + TypeScript chat interface for the Arizona Adventure Agent, built with Vite, Tailwind CSS, and shadcn/ui components.

## Features

- 🎨 Beautiful UI with shadcn/ui components
- 💬 Real-time streaming chat interface
- 📱 Responsive design
- 🔄 Human-in-the-loop review support
- 🎯 TypeScript for type safety
- ⚡ Fast development with Vite

## Getting Started

### Prerequisites

- Node.js 18+ and npm/yarn/pnpm
- LangGraph API server running on `http://localhost:2024` (or configure via environment variable)

### Installation

```bash
# Install dependencies
npm install

# Start development server
npm run dev
```

The app will be available at `http://localhost:3000`.

### Environment Variables

Create a `.env` file in the frontend directory:

```env
VITE_API_URL=http://localhost:2024
```

### Building for Production

```bash
npm run build
```

The built files will be in the `dist` directory.

## Project Structure

```
frontend/
├── src/
│   ├── components/
│   │   ├── ui/              # shadcn/ui components
│   │   ├── chat-interface.tsx
│   │   ├── message-list.tsx
│   │   ├── message-input.tsx
│   │   ├── adventure-plan-view.tsx
│   │   └── human-review-modal.tsx
│   ├── hooks/
│   │   └── use-chat.ts      # Chat state management
│   ├── services/
│   │   └── api-client.ts    # LangGraph API client
│   ├── types/
│   │   └── adventure.ts     # TypeScript types
│   ├── lib/
│   │   └── utils.ts         # Utility functions
│   ├── App.tsx
│   └── main.tsx
├── package.json
├── vite.config.ts
└── tailwind.config.js
```

## Usage

1. Start the LangGraph API server:
   ```bash
   langgraph dev
   ```

2. Start the frontend:
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

3. Open `http://localhost:3000` in your browser

4. Start chatting! Try:
   - "Plan a 3-day mountain bike trip in Sedona"
   - "What are the best bikepacking routes near Flagstaff?"
   - "Find intermediate trails in Payson"

## Components

### ChatInterface
Main chat container component that manages the conversation flow.

### MessageList
Displays messages in the chat, including user messages, assistant responses, and adventure plans.

### MessageInput
Input field for sending messages to the agent.

### AdventurePlanView
Renders structured adventure plans with itineraries, trails, gear recommendations, etc.

### HumanReviewModal
Modal dialog for reviewing and approving/rejecting adventure plans when human-in-the-loop is triggered.

## API Integration

The frontend communicates with the LangGraph API server using the `AdventureAgentClient` class. It supports:

- Creating conversation threads
- Streaming real-time updates
- Handling human-in-the-loop interrupts
- Resuming interrupted runs

## Styling

The project uses Tailwind CSS with shadcn/ui components. The theme can be customized in `src/index.css` and `tailwind.config.js`.

## License

Same as the main adventure-agent project.

