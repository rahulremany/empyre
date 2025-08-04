# Empyre Frontend

A modern, sleek Next.js frontend for the Empyre AI Fitness Coach platform. Built with TypeScript, Tailwind CSS, and Framer Motion for smooth animations and interactions.

## Features

### 🎨 Modern Design
- **Glass Morphism**: Beautiful backdrop blur effects and transparency
- **Gradient Backgrounds**: Subtle color transitions for visual depth
- **Smooth Animations**: Framer Motion powered transitions and micro-interactions
- **Responsive Design**: Optimized for desktop, tablet, and mobile devices
- **Dark Mode Ready**: Built-in dark mode support (can be easily enabled)

### 💬 AI Chat Interface
- **Real-time Messaging**: Seamless conversation with the AI coach
- **Message History**: Persistent chat history with timestamps
- **Loading States**: Smooth loading animations and typing indicators
- **Auto-scroll**: Automatic scrolling to latest messages
- **Keyboard Shortcuts**: Enter to send, Shift+Enter for new lines

### 🏆 Gamification System
- **Laurels Dashboard**: View earned achievements and points
- **Progress Tracking**: Log workouts, measurements, and goals
- **Quick Actions**: Easy access to common tasks
- **Visual Feedback**: Animated achievement unlocks and progress indicators

### 📱 Responsive Navigation
- **Desktop Sidebar**: Fixed sidebar with smooth transitions
- **Mobile Menu**: Collapsible hamburger menu for mobile devices
- **Tab Navigation**: Easy switching between chat, achievements, and progress
- **User ID Display**: Clear user identification for debugging

## Tech Stack

- **Next.js 15**: React framework with App Router
- **TypeScript**: Type-safe development
- **Tailwind CSS**: Utility-first CSS framework
- **Framer Motion**: Animation library for smooth interactions
- **Lucide React**: Beautiful, customizable icons
- **Headless UI**: Accessible UI components
- **Class Variance Authority**: Type-safe component variants

## Getting Started

### Prerequisites
- Node.js 18+ 
- npm or yarn
- Backend server running on `http://localhost:8000`

### Installation

1. **Install dependencies**:
   ```bash
   npm install
   ```

2. **Set environment variables** (optional):
   Create a `.env.local` file:
   ```env
   NEXT_PUBLIC_API_URL=http://localhost:8000
   ```

3. **Start the development server**:
   ```bash
   npm run dev
   ```

4. **Open your browser**:
   Navigate to `http://localhost:3000`

### Building for Production

```bash
npm run build
npm start
```

## Project Structure

```
src/
├── app/                    # Next.js App Router
│   ├── globals.css        # Global styles and CSS variables
│   ├── layout.tsx         # Root layout component
│   └── page.tsx           # Main page with navigation
├── components/            # Reusable components
│   ├── ui/               # Base UI components
│   │   ├── button.tsx    # Button component with variants
│   │   ├── card.tsx      # Card component
│   │   └── input.tsx     # Input component
│   ├── chat/             # Chat-related components
│   │   └── chat-interface.tsx
│   └── dashboard/        # Dashboard components
│       ├── laurels-section.tsx
│       └── progress-section.tsx
└── lib/                  # Utility functions and types
    └── utils.ts          # API functions, types, and helpers
```

## Key Components

### ChatInterface
The main chat component that handles:
- Message sending and receiving
- Real-time API communication
- Message history management
- Loading states and error handling

### LaurelsSection
Gamification dashboard featuring:
- Achievement display and management
- Points tracking
- Quick action buttons
- Visual feedback for achievements

### ProgressSection
Progress tracking interface with:
- Workout logging forms
- Progress history display
- Multiple log types (workout, measurement, goal)
- Date formatting and organization

## API Integration

The frontend communicates with the backend through RESTful APIs:

- **Chat**: `POST /chat` - Send messages and receive AI responses
- **Laurels**: `GET /laurels/{userId}` - Fetch user achievements
- **Laurels**: `POST /laurels/{userId}/award` - Award new achievements
- **Progress**: `GET /progress/{userId}` - Fetch progress logs
- **Progress**: `POST /progress` - Log new progress entries

## Styling System

### CSS Variables
The app uses CSS custom properties for consistent theming:
- Color palette with light/dark mode support
- Border radius and spacing variables
- Animation timing and easing functions

### Tailwind Classes
- Utility-first approach for rapid development
- Custom animations and keyframes
- Responsive design utilities
- Glass morphism effects

### Component Variants
- Type-safe component variants using CVA
- Consistent button, card, and input styles
- Accessible focus states and interactions

## Performance Optimizations

- **Code Splitting**: Automatic route-based code splitting
- **Image Optimization**: Next.js built-in image optimization
- **Font Optimization**: Google Fonts with display swap
- **Bundle Analysis**: Built-in bundle analyzer support
- **Lazy Loading**: Components loaded on demand

## Accessibility Features

- **Keyboard Navigation**: Full keyboard support
- **Screen Reader Support**: Proper ARIA labels and roles
- **Focus Management**: Visible focus indicators
- **Color Contrast**: WCAG compliant color combinations
- **Semantic HTML**: Proper heading hierarchy and landmarks

## Browser Support

- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## Development

### Code Style
- ESLint configuration for code quality
- Prettier for consistent formatting
- TypeScript strict mode enabled

### Testing
```bash
npm run lint        # Run ESLint
npm run type-check  # TypeScript type checking
```

### Deployment
The app is ready for deployment on:
- Vercel (recommended)
- Netlify
- AWS Amplify
- Any static hosting service

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is part of the Empyre AI Fitness Coach platform.
