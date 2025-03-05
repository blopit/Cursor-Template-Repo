---
description: Rules and best practices for TypeScript development in the project
globs: "**/*.{ts,tsx}"
---

# TypeScript Development Rules

## Purpose
This file defines rules and best practices for TypeScript development in the project. It ensures type safety, consistent code style, and proper documentation across all TypeScript files.

## Glob Patterns
- `**/*.ts`
- `**/*.tsx`
- `src/**/*.ts`
- `src/**/*.tsx`
- `!**/node_modules/**`
- `!**/dist/**`
- `!**/build/**`

## Rules

### Type Safety
- Always use explicit types for function parameters and return values
- Avoid using `any` type unless absolutely necessary
- Use interfaces for object shapes
- Use type aliases for complex types
- Enable strict mode in tsconfig.json
- Use union types instead of enums when possible
- Use readonly for immutable properties
- Use const assertions for literal values

### Code Style
- Follow ESLint and Prettier configurations
- Use 2 spaces for indentation
- Maximum line length of 100 characters
- Use semicolons at the end of statements
- Use single quotes for strings
- Use camelCase for variables and functions
- Use PascalCase for classes, interfaces, and type aliases
- Use UPPER_SNAKE_CASE for constants
- Add trailing commas in multi-line object and array literals

### Documentation
- Use JSDoc comments for functions, classes, and interfaces
- Document parameters, return values, and thrown exceptions
- Include examples for complex functions
- Add comments for complex or non-obvious code sections
- Document public APIs thoroughly

### Imports
- Group imports in the following order:
  1. External libraries
  2. Internal modules
  3. Relative imports
- Sort imports alphabetically within each group
- Use absolute imports for internal modules
- Avoid default exports
- Use named exports for better refactoring support
- Use barrel exports (index.ts) for related functionality

### Error Handling
- Use typed error classes
- Include meaningful error messages
- Handle errors at the appropriate level
- Use try/catch blocks for async code
- Avoid swallowing errors

### React-Specific Rules (for .tsx files)
- Use functional components with hooks
- Use React.FC type for components
- Define prop interfaces for components
- Use destructuring for props
- Extract complex logic into custom hooks
- Use React.memo for performance optimization when appropriate
- Keep components small and focused

## Examples

### Good Type Safety

```typescript
// Good type usage
interface User {
  id: string;
  name: string;
  email: string;
  age: number;
  isActive: boolean;
  roles: ReadonlyArray<string>;
  preferences?: UserPreferences;
}

type UserPreferences = {
  theme: 'light' | 'dark' | 'system';
  notifications: boolean;
  language: string;
};

function getUserById(id: string): Promise<User | null> {
  // Implementation
  return fetch(`/api/users/${id}`)
    .then(response => {
      if (!response.ok) {
        throw new Error(`Failed to fetch user: ${response.statusText}`);
      }
      return response.json();
    })
    .then(data => data as User)
    .catch(error => {
      console.error(`Error fetching user ${id}:`, error);
      return null;
    });
}

// Using const assertions
const ROLES = ['admin', 'user', 'guest'] as const;
type Role = typeof ROLES[number];

// Using readonly
interface ReadonlyUser {
  readonly id: string;
  readonly name: string;
  readonly email: string;
}
```

### Good React Component

```tsx
import React, { useState, useEffect } from 'react';

import { User } from '../types/user';
import { fetchUserById } from '../api/users';
import { UserCard } from './UserCard';
import { ErrorMessage } from './ErrorMessage';
import { LoadingSpinner } from './LoadingSpinner';

interface UserProfileProps {
  userId: string;
  showDetails?: boolean;
  onUserLoad?: (user: User) => void;
}

/**
 * UserProfile component displays a user's profile information.
 * 
 * @param userId - The ID of the user to display
 * @param showDetails - Whether to show detailed information
 * @param onUserLoad - Callback function called when user data is loaded
 */
export const UserProfile: React.FC<UserProfileProps> = ({
  userId,
  showDetails = false,
  onUserLoad,
}) => {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let isMounted = true;

    const loadUser = async (): Promise<void> => {
      try {
        setLoading(true);
        setError(null);
        
        const userData = await fetchUserById(userId);
        
        if (isMounted) {
          setUser(userData);
          if (userData && onUserLoad) {
            onUserLoad(userData);
          }
        }
      } catch (err) {
        if (isMounted) {
          setError(`Failed to load user: ${err instanceof Error ? err.message : 'Unknown error'}`);
        }
      } finally {
        if (isMounted) {
          setLoading(false);
        }
      }
    };

    loadUser();

    return () => {
      isMounted = false;
    };
  }, [userId, onUserLoad]);

  if (loading) {
    return <LoadingSpinner />;
  }

  if (error) {
    return <ErrorMessage message={error} />;
  }

  if (!user) {
    return <div>User not found</div>;
  }

  return (
    <div className="user-profile">
      <UserCard user={user} />
      
      {showDetails && (
        <div className="user-details">
          <h3>Additional Details</h3>
          <p>Email: {user.email}</p>
          <p>Member since: {new Date(user.createdAt).toLocaleDateString()}</p>
          <p>Last active: {new Date(user.lastActive).toLocaleDateString()}</p>
        </div>
      )}
    </div>
  );
};
```

### Good Custom Hook

```typescript
import { useState, useEffect, useCallback } from 'react';

interface UseFetchResult<T> {
  data: T | null;
  loading: boolean;
  error: string | null;
  refetch: () => Promise<void>;
}

/**
 * Custom hook for fetching data from an API.
 * 
 * @param url - The URL to fetch data from
 * @param options - Fetch options
 * @returns Object containing data, loading state, error, and refetch function
 */
export function useFetch<T>(
  url: string,
  options?: RequestInit
): UseFetchResult<T> {
  const [data, setData] = useState<T | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  const fetchData = useCallback(async (): Promise<void> => {
    try {
      setLoading(true);
      setError(null);

      const response = await fetch(url, options);
      
      if (!response.ok) {
        throw new Error(`API error: ${response.status} ${response.statusText}`);
      }
      
      const result = await response.json();
      setData(result as T);
    } catch (err) {
      setError(`Failed to fetch data: ${err instanceof Error ? err.message : 'Unknown error'}`);
      setData(null);
    } finally {
      setLoading(false);
    }
  }, [url, options]);

  useEffect(() => {
    fetchData();
  }, [fetchData]);

  const refetch = useCallback(async (): Promise<void> => {
    await fetchData();
  }, [fetchData]);

  return { data, loading, error, refetch };
}
```

## Related MDC Files
- [react-component-glob.mdc](mdc:../components/react-component-glob.mdc)
- [eslint-config.mdc](mdc:../linting/eslint-config.mdc)
- [testing-typescript-glob.mdc](mdc:../testing/testing-typescript-glob.mdc)

## Exceptions
- Generated TypeScript files (marked with a `// GENERATED FILE` comment) are exempt from style requirements
- Test files may have relaxed naming conventions for test functions
- Migration scripts may follow different import ordering due to their specific requirements
- Legacy code may be gradually updated to follow these standards

## Enforcement
- ESLint is used to enforce code style and best practices
- TypeScript compiler with strict mode enabled
- Prettier is used for consistent formatting
- Pre-commit hooks enforce these checks before commits
- CI/CD pipeline includes these checks for all pull requests
- Code reviews should verify adherence to these standards

## Version History
- 2023-09-15: Initial version
- 2023-10-30: Added React-specific rules
- 2024-01-10: Updated type safety guidelines
- 2024-02-22: Added custom hooks section and examples 