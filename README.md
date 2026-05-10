# Live Customer Support Chat

A real-time customer support chat application where customers can talk instantly with support agents through a web chat widget. Agents manage incoming conversations from a dashboard, claim waiting chats, reply in real time, and close sessions after support is complete.

## Core Project Idea

The project solves a common customer support problem: customers need fast help, and support teams need one place to manage conversations.

The system has two main interfaces:

- Customer chat widget: used by website visitors to start and continue a support conversation.
- Agent dashboard: used by support agents to see waiting chats, claim conversations, reply to customers, and manage active sessions.

Messages are delivered instantly using WebSockets. Every chat session and message is also saved in the database so conversations can be reloaded later.

## Main Users

### Customer

The customer starts a chat by entering basic information such as their name. After the session starts, they can send and receive messages in real time. The customer can also see typing indicators, reconnect to the same conversation, and submit feedback after the chat ends.

### Agent

The agent uses a dashboard to view waiting chats and active chats. An agent can claim a waiting chat, reply to the customer, mark messages as read, transfer the conversation to another agent, and close the chat when the issue is solved.

### Admin

The admin manages users, agents, chat sessions, messages, and ratings from the backend.

## Main Features

### Real-Time Messaging

Customers and agents communicate through WebSockets. When one user sends a message, the backend saves it to the database and broadcasts it to everyone connected to that chat session.

### Chat Sessions

Each conversation is stored as a chat session. A session can be:

- `waiting`: customer has started a chat but no agent has claimed it yet.
- `active`: an agent is handling the conversation.
- `closed`: the conversation is finished.

### Agent Queue

New customer chats appear in a waiting queue for online agents. When an agent claims a chat, that session is assigned to the agent and removed from the waiting queue.

### Agent Availability

Agents can have availability states such as:

- `online`
- `busy`
- `offline`

Only available agents should receive or claim new conversations.

### Message History

Messages are stored in the database, so both customers and agents can reload previous messages when they open or reconnect to a chat.

### Typing Indicators

Typing events are sent through WebSockets to show when the other person is typing. These events are temporary and are not saved in the database.

### Read Receipts

When a user views messages, the system can mark them as read and notify the other side.

### Chat Transfer

An agent can transfer an active chat to another agent. The customer remains in the same conversation, but the assigned agent changes.

### Post-Chat Rating

After a chat is closed, the customer can submit a rating and optional feedback. This helps track support quality and agent performance.

### Canned Responses

Agents can save common replies and reuse them during conversations to respond faster.

## Core Models

### ChatSession

Represents one customer conversation.

Important fields:

- customer name
- assigned agent
- status
- created date
- updated date

### Message

Represents one message inside a chat session.

Important fields:

- chat session
- sender type: customer or agent
- message content
- timestamp
- read status

### Agent

Represents a support agent.

Important fields:

- linked user account
- availability status
- department
- active chat count
- average rating

### Rating

Stores customer feedback after a chat ends.

Important fields:

- chat session
- rating score
- feedback text

## WebSocket Flow

Each chat session has its own WebSocket group.

Example:

```text
chat_12
```

Basic message flow:

1. Customer opens a chat session.
2. Browser connects to the chat WebSocket.
3. Customer sends a message.
4. Backend validates the message.
5. Backend saves the message to the database.
6. Backend broadcasts the message to the chat group.
7. Agent receives the message instantly.
8. Agent sends a reply through the same flow.

## REST API Ideas

The project can use REST APIs for actions that do not need a permanent WebSocket connection.

| Method | Endpoint | Purpose |
| --- | --- | --- |
| `POST` | `/api/sessions/` | Start a new chat session. |
| `GET` | `/api/sessions/{id}/messages/` | Load chat message history. |
| `POST` | `/api/sessions/{id}/close/` | Close a chat session. |
| `POST` | `/api/sessions/{id}/rate/` | Submit customer rating. |
| `GET` | `/api/agents/` | List available agents. |

## Technology Used

- Django for the backend.
- Django Channels for WebSocket support.
- Redis as the WebSocket channel layer.
- Django REST Framework for API endpoints.
- PostgreSQL or SQLite for storing sessions and messages.
- HTML, CSS, and JavaScript for the customer chat widget and agent dashboard.

## Final Project Scope

The completed project should allow a customer to start a support chat, exchange real-time messages with an agent, reload previous messages, see typing and read status, and rate the chat after completion.

The agent side should allow agents to view the waiting queue, claim chats, reply to customers, manage active conversations, transfer chats, use canned responses, and close sessions.
