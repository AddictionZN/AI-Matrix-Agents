# React Coding Standards

This document outlines our React coding standards and best practices using React 19 ([react.dev](https://react.dev/)). Following these guidelines ensures consistency, readability, and maintainability across all React applications in the project.

## Table of Contents

1. [Component Architecture](#1-component-architecture)
2. [JSX Formatting](#2-jsx-formatting)
3. [Hooks Usage](#3-hooks-usage)
4. [Props](#4-props)
5. [State Management](#5-state-management)
6. [Performance Optimization](#6-performance-optimization)
7. [File Structure](#7-file-structure)
8. [Styling](#8-styling)
9. [Error Handling](#9-error-handling)
10. [Testing](#10-testing)
11. [Accessibility](#11-accessibility)

## 1. Component Architecture

### 1.1 Component Types

- Use **function components** as the default approach
- Organize components by feature rather than type
- Extract reusable UI elements into separate components

```jsx
// Correct
function UserProfile({ user }) {
  return (
    <div className="user-profile">
      <Avatar src={user.avatarUrl} size="large" />
      <UserDetails user={user} />
      <UserActions userId={user.id} />
    </div>
  );
}

// Incorrect - Too many responsibilities in one component
function UserPage({ userId }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  
  // Data fetching, error handling, rendering all mixed together
  // ...
}
```

### 1.2 Component Naming

- Use **PascalCase** for component names
- Use descriptive names that explain the component's purpose
- Suffix higher-order components with `With` (e.g., `WithAuth`)
- Suffix custom hooks with `use` (e.g., `useFormValidation`)

```jsx
// Correct
function ProductCard() { /* ... */ }
function EnhancedComponent() { /* ... */ }
function useWindowSize() { /* ... */ }

// Incorrect
function product_card() { /* ... */ }
function products() { /* ... */ }
function getWindowSize() { /* ... */ }
```

## 2. JSX Formatting

### 2.1 General Rules

- Use self-closing tags for elements with no children
- Use multiline format for components with 3+ props
- Place each prop on a new line when using multiline format
- Always use double quotes (`"`) for JSX attributes
- Use curly braces (`{}`) for dynamic values

```jsx
// Correct - Self-closing tag
<UserAvatar src={avatarUrl} size="large" />

// Correct - Multiline format for many props
<UserProfileCard
  username={user.name}
  email={user.email}
  avatarUrl={user.avatarUrl}
  isVerified={user.isVerified}
  joinDate={user.joinDate}
/>

// Incorrect
<UserProfileCard username={user.name} email={user.email} avatarUrl={user.avatarUrl} isVerified={user.isVerified} joinDate={user.joinDate}/>
```

### 2.2 Conditional Rendering

- Use conditional (ternary) operator for simple conditions
- Extract complex conditions into variables or functions
- Use logical AND (`&&`) operator with caution (avoid boolean conversion issues)

```jsx
// Correct - Simple ternary
{isLoggedIn ? <UserDashboard /> : <LoginPrompt />}

// Correct - Extracted condition
const userContent = isAdmin 
  ? <AdminDashboard permissions={permissions} /> 
  : <UserDashboard />;

return <div className="dashboard-container">{userContent}</div>;

// Correct - Safe use of logical AND
{items.length > 0 && <ItemList items={items} />}

// Incorrect - Potential issue with falsy values
{itemCount && <span>{itemCount} items</span>} // Renders "0" when itemCount is 0
```

## 3. Hooks Usage

### 3.1 Basic Rules

- Only call hooks at the top level of components or custom hooks
- Follow the naming convention `useXxx` for custom hooks
- Keep hooks focused on a single concern

```jsx
// Correct
function useUserStatus(userId) {
  const [isOnline, setIsOnline] = useState(false);
  
  useEffect(() => {
    const unsubscribe = subscribeToUserStatus(userId, status => {
      setIsOnline(status.isOnline);
    });
    
    return () => unsubscribe();
  }, [userId]);
  
  return isOnline;
}

// Incorrect - Hook inside conditional
function UserStatus({ userId }) {
  if (userId) {
    // This breaks the Rules of Hooks
    const [isOnline, setIsOnline] = useState(false);
  }
  // ...
}
```

### 3.2 Common Hooks

- `useState`: Use for simple component state
- `useReducer`: Use for complex state logic
- `useContext`: Use for deeply shared state
- `useEffect`: Separate effects by concern
- `useMemo`/`useCallback`: Use for performance optimization only when needed

```jsx
// Correct - Separate effects by concern
function UserProfile({ userId }) {
  const [user, setUser] = useState(null);
  
  // Effect for data fetching
  useEffect(() => {
    let isMounted = true;
    fetchUserData(userId).then(data => {
      if (isMounted) setUser(data);
    });
    return () => { isMounted = false; };
  }, [userId]);
  
  // Separate effect for analytics
  useEffect(() => {
    logProfileView(userId);
  }, [userId]);
  
  // ...
}
```

### 3.3 Dependencies Array

- Include all values from component scope used inside the Effect
- Use dependency linting rules (ESLint plugin react-hooks)
- Extract functions inside effects when they don't need to be dependencies

```jsx
// Correct
function SearchResults({ query, pageSize }) {
  const [results, setResults] = useState([]);
  
  useEffect(() => {
    // Function extracted inside to avoid adding it to dependencies
    async function fetchResults() {
      const data = await searchApi(query, pageSize);
      setResults(data);
    }
    
    fetchResults();
  }, [query, pageSize]); // All dependencies listed
  
  // ...
}
```

## 4. Props

### 4.1 Prop Types and Default Values

- Use TypeScript or PropTypes for type checking
- Provide default values for optional props
- Destructure props in function parameters

```jsx
// Using TypeScript
interface UserCardProps {
  name: string;
  email: string;
  avatar?: string;
  isVerified?: boolean;
}

function UserCard({ 
  name, 
  email, 
  avatar = '/default-avatar.png',
  isVerified = false 
}: UserCardProps) {
  // Component implementation
}

// Using PropTypes
function UserCard({ name, email, avatar = '/default-avatar.png', isVerified = false }) {
  // Component implementation
}

UserCard.propTypes = {
  name: PropTypes.string.isRequired,
  email: PropTypes.string.isRequired,
  avatar: PropTypes.string,
  isVerified: PropTypes.bool
};
```

### 4.2 Prop Naming

- Use camelCase for prop names
- Use boolean props with "is", "has", or "should" prefixes
- Be consistent with event handler props (e.g., `onClick`, `onSubmit`)

```jsx
// Correct
<UserProfile 
  userName="johndoe"
  isAdmin={true}
  hasAccess={true}
  onProfileUpdate={handleUpdate}
/>

// Incorrect
<UserProfile 
  UserName="johndoe"
  admin={true}
  access={true}
  profileUpdate={handleUpdate}
/>
```

## 5. State Management

### 5.1 Component State

- Keep state as local as possible
- Split state into multiple `useState` calls by concern
- Use `useReducer` for complex state logic

```jsx
// Correct - Separate state by concern
function UserForm() {
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [errors, setErrors] = useState({});
  
  // Form handling logic
}

// Correct - Using useReducer for complex state
function formReducer(state, action) {
  switch (action.type) {
    case 'field_change':
      return { ...state, [action.field]: action.value };
    case 'submit_start':
      return { ...state, isSubmitting: true, errors: {} };
    case 'submit_success':
      return { ...state, isSubmitting: false, isSuccess: true };
    case 'submit_error':
      return { ...state, isSubmitting: false, errors: action.errors };
    default:
      return state;
  }
}

function ComplexForm() {
  const [state, dispatch] = useReducer(formReducer, {
    username: '',
    email: '',
    isSubmitting: false,
    isSuccess: false,
    errors: {}
  });
  
  // Form handling logic
}
```

### 5.2 Global State Management

- Use React Context for sharing state between components
- Consider external libraries (Redux, Zustand, Jotai) for complex applications
- Split global state by domain concern

```jsx
// Context example
const UserContext = createContext();

function UserProvider({ children }) {
  const [user, setUser] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  
  // Authentication logic
  const login = async (credentials) => {/* ... */};
  const logout = async () => {/* ... */};
  
  const value = {
    user,
    isLoading,
    login,
    logout
  };
  
  return <UserContext.Provider value={value}>{children}</UserContext.Provider>;
}

// Custom hook for consuming the context
function useUser() {
  const context = useContext(UserContext);
  if (!context) {
    throw new Error('useUser must be used within a UserProvider');
  }
  return context;
}
```

## 6. Performance Optimization

### 6.1 Component Memoization

- Use `React.memo` for components that render often with the same props
- Use `useMemo` for expensive calculations
- Use `useCallback` for functions passed as props to memoized components

```jsx
// Memoizing a component
const MemoizedUserCard = memo(UserCard);

// Using useMemo for expensive calculations
function ProductList({ products, filter }) {
  const filteredProducts = useMemo(() => {
    return products.filter(product => 
      product.category === filter.category &&
      product.price <= filter.maxPrice
    );
  }, [products, filter.category, filter.maxPrice]);
  
  // Rest of component
}

// Using useCallback for event handlers
function Parent() {
  const [count, setCount] = useState(0);
  
  const handleIncrement = useCallback(() => {
    setCount(c => c + 1);
  }, []);
  
  return <MemoizedButton onClick={handleIncrement} label="Increment" />;
}
```

### 6.2 Render Optimization

- Use virtualization for long lists (react-window or react-virtualized)
- Avoid inline object creation in render
- Prioritize lazy loading for code splitting

```jsx
// Correct - Avoiding inline object creation
function UserProfile({ user }) {
  const cardStyle = useMemo(() => ({ 
    backgroundColor: user.isPremium ? 'gold' : 'silver' 
  }), [user.isPremium]);
  
  return <div style={cardStyle}>{/* ... */}</div>;
}

// Incorrect
function UserProfile({ user }) {
  return (
    <div style={{ backgroundColor: user.isPremium ? 'gold' : 'silver' }}>
      {/* This creates a new style object on every render */}
    </div>
  );
}

// Correct - Using lazy loading for routes
const UserDashboard = lazy(() => import('./UserDashboard'));

function App() {
  return (
    <Routes>
      <Route 
        path="/dashboard" 
        element={
          <Suspense fallback={<LoadingSpinner />}>
            <UserDashboard />
          </Suspense>
        } 
      />
    </Routes>
  );
}
```

## 7. File Structure

### 7.1 Project Organization

- Organize by feature or domain instead of type
- Keep related files together
- Use index files for cleaner imports

```
src/
├── features/
│   ├── users/
│   │   ├── components/
│   │   │   ├── UserCard.tsx
│   │   │   ├── UserList.tsx
│   │   │   └── index.ts
│   │   ├── hooks/
│   │   │   ├── useUsers.ts
│   │   │   └── index.ts
│   │   ├── api.ts
│   │   ├── types.ts
│   │   └── index.ts
│   └── products/
│       └── ...
├── components/ (shared components)
│   ├── Button/
│   │   ├── Button.tsx
│   │   ├── Button.test.tsx
│   │   ├── Button.module.css
│   │   └── index.ts
│   └── ...
├── hooks/ (shared hooks)
├── utils/ (utility functions)
└── App.tsx
```

### 7.2 Component File Structure

- One component per file (with related subcomponents allowed)
- Export components as named or default exports consistently
- Co-locate test files with component files

```jsx
// Button.tsx
import styles from './Button.module.css';

// Types
interface ButtonProps {
  label: string;
  onClick: () => void;
  variant?: 'primary' | 'secondary';
  disabled?: boolean;
}

// Component
export function Button({ 
  label, 
  onClick, 
  variant = 'primary', 
  disabled = false 
}: ButtonProps) {
  return (
    <button
      className={styles[variant]}
      onClick={onClick}
      disabled={disabled}
    >
      {label}
    </button>
  );
}

// index.ts
export * from './Button';
```

## 8. Styling

### 8.1 CSS Approaches

- Use CSS Modules or styled-components for component-scoped styles
- Follow a consistent naming convention (BEM, SMACSS, etc.)
- Use CSS variables for theming

```jsx
// Using CSS Modules
import styles from './Button.module.css';

function Button({ variant = 'primary', children }) {
  return (
    <button className={`${styles.button} ${styles[variant]}`}>
      {children}
    </button>
  );
}

// Using styled-components
import styled, { css } from 'styled-components';

const Button = styled.button`
  padding: 10px 16px;
  border-radius: 4px;
  font-size: 16px;
  
  ${props => props.variant === 'primary' && css`
    background-color: var(--primary-color);
    color: white;
  `}
  
  ${props => props.variant === 'secondary' && css`
    background-color: transparent;
    border: 1px solid var(--primary-color);
    color: var(--primary-color);
  `}
`;

function StyledButton({ variant, children }) {
  return <Button variant={variant}>{children}</Button>;
}
```

### 8.2 Responsive Design

- Use relative units (rem, em) over pixels
- Implement responsive design with CSS media queries
- Consider mobile-first approach

```jsx
// CSS Module with responsive design
.container {
  padding: 1rem;
  display: grid;
  grid-template-columns: 1fr;
  gap: 1rem;
}

@media (min-width: 768px) {
  .container {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (min-width: 1024px) {
  .container {
    grid-template-columns: repeat(3, 1fr);
  }
}
```

## 9. Error Handling

### 9.1 Component Error Boundaries

- Use Error Boundary components to catch and handle runtime errors
- Provide meaningful fallback UIs
- Log errors appropriately

```jsx
// Error boundary component
class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, error: null };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true, error };
  }

  componentDidCatch(error, errorInfo) {
    // Log error to monitoring service
    logErrorToService(error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return this.props.fallback || <DefaultErrorUI error={this.state.error} />;
    }
    return this.props.children;
  }
}

// Usage
function App() {
  return (
    <ErrorBoundary fallback={<AppErrorFallback />}>
      <AppContent />
    </ErrorBoundary>
  );
}
```

### 9.2 Async Error Handling

- Handle API errors gracefully
- Show appropriate loading and error states
- Use try/catch with async/await

```jsx
function UserProfile({ userId }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    async function fetchUser() {
      try {
        setLoading(true);
        setError(null);
        const data = await api.getUser(userId);
        setUser(data);
      } catch (err) {
        setError(err.message || "Failed to fetch user");
      } finally {
        setLoading(false);
      }
    }

    fetchUser();
  }, [userId]);

  if (loading) return <LoadingSpinner />;
  if (error) return <ErrorMessage message={error} />;
  if (!user) return <EmptyState message="User not found" />;

  return <UserDetails user={user} />;
}
```

## 10. Testing

### 10.1 Component Testing

- Use React Testing Library for component tests
- Focus on testing behavior, not implementation
- Use mock services for API calls

```jsx
// Button.test.tsx
import { render, screen, fireEvent } from '@testing-library/react';
import { Button } from './Button';

describe('Button', () => {
  test('renders with correct label', () => {
    render(<Button label="Click me" onClick={() => {}} />);
    expect(screen.getByText('Click me')).toBeInTheDocument();
  });

  test('calls onClick handler when clicked', () => {
    const handleClick = jest.fn();
    render(<Button label="Click me" onClick={handleClick} />);
    fireEvent.click(screen.getByText('Click me'));
    expect(handleClick).toHaveBeenCalledTimes(1);
  });

  test('is disabled when disabled prop is true', () => {
    render(<Button label="Click me" onClick={() => {}} disabled={true} />);
    expect(screen.getByText('Click me')).toBeDisabled();
  });
});
```

### 10.2 Hook Testing

- Test custom hooks with `@testing-library/react-hooks`
- Test different scenarios and edge cases

```jsx
// useCounter.test.js
import { renderHook, act } from '@testing-library/react-hooks';
import { useCounter } from './useCounter';

describe('useCounter', () => {
  test('should initialize with default value', () => {
    const { result } = renderHook(() => useCounter());
    expect(result.current.count).toBe(0);
  });

  test('should initialize with provided value', () => {
    const { result } = renderHook(() => useCounter(10));
    expect(result.current.count).toBe(10);
  });

  test('should increment counter', () => {
    const { result } = renderHook(() => useCounter());
    act(() => {
      result.current.increment();
    });
    expect(result.current.count).toBe(1);
  });

  test('should decrement counter', () => {
    const { result } = renderHook(() => useCounter(5));
    act(() => {
      result.current.decrement();
    });
    expect(result.current.count).toBe(4);
  });
});
```

## 11. Accessibility

### 11.1 Semantic HTML

- Use appropriate semantic HTML elements
- Use ARIA attributes when necessary
- Ensure keyboard navigation works correctly

```jsx
// Correct - Using semantic HTML
function Article({ title, content, publishDate, author }) {
  return (
    <article>
      <h2>{title}</h2>
      <p>{content}</p>
      <footer>
        <p>Published on <time dateTime={publishDate.toISOString()}>
          {formatDate(publishDate)}
        </time> by {author}</p>
      </footer>
    </article>
  );
}

// Incorrect - Div soup
function Article({ title, content, publishDate, author }) {
  return (
    <div className="article">
      <div className="title">{title}</div>
      <div className="content">{content}</div>
      <div className="footer">
        Published on {formatDate(publishDate)} by {author}
      </div>
    </div>
  );
}
```

### 11.2 Focus Management

- Manage focus for dynamic content changes
- Use `useRef` and `focus()` for programmatic focus
- Implement focus traps for modals and dialogs

```jsx
function SearchInput() {
  const inputRef = useRef(null);
  
  useEffect(() => {
    // Auto-focus the input on mount
    inputRef.current?.focus();
  }, []);
  
  return (
    <input
      ref={inputRef}
      type="search"
      aria-label="Search"
      placeholder="Search..."
    />
  );
}

function Modal({ isOpen, onClose, children }) {
  const modalRef = useRef(null);
  
  useEffect(() => {
    if (isOpen) {
      // Store the current active element to restore focus later
      const previousFocus = document.activeElement;
      
      // Focus the modal when it opens
      modalRef.current?.focus();
      
      return () => {
        // Restore focus when modal closes
        previousFocus?.focus();
      };
    }
  }, [isOpen]);
  
  if (!isOpen) return null;
  
  return (
    <div 
      role="dialog"
      aria-modal="true"
      ref={modalRef}
      tabIndex={-1}
      className="modal"
    >
      <div className="modal-content">
        {children}
        <button onClick={onClose}>Close</button>
      </div>
    </div>
  );
}
```