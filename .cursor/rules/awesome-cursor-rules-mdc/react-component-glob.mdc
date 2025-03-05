---
description: Rules and best practices for React components in the project
globs: "**/*.{jsx,tsx}"
---

# React Component Rules

## Purpose
This file defines rules and best practices for React components in the project. It ensures consistent component structure, proper state management, and adherence to React best practices across all React component files.

## Glob Patterns
- `**/*.tsx`
- `**/*.jsx`
- `src/components/**/*.tsx`
- `src/components/**/*.jsx`
- `src/pages/**/*.tsx`
- `src/pages/**/*.jsx`
- `!**/node_modules/**`
- `!**/dist/**`
- `!**/build/**`

## Rules

### Component Structure
- Use functional components with hooks instead of class components
- Define prop interfaces for TypeScript components
- Use React.FC type for functional components in TypeScript
- Use destructuring for props
- Keep components small and focused on a single responsibility
- Extract complex logic into custom hooks
- Use React.memo for performance optimization when appropriate
- Implement proper prop validation with PropTypes for JavaScript components

### Component Organization
- One component per file (except for small, tightly coupled components)
- Name component files the same as the component (PascalCase)
- Group related components in directories
- Use index.ts/index.js files for barrel exports
- Organize component files by feature or type
- Keep UI components separate from container components
- Place shared components in a common directory

### State Management
- Use useState for simple component state
- Use useReducer for complex state logic
- Use context API for shared state across components
- Avoid prop drilling more than 2-3 levels deep
- Keep state as close as possible to where it's used
- Use controlled components for form inputs
- Implement proper state initialization

### Side Effects
- Use useEffect for side effects
- Clean up side effects in the return function
- Use appropriate dependency arrays
- Avoid direct DOM manipulation
- Handle component unmounting properly
- Use useCallback for functions passed to child components
- Use useMemo for expensive calculations

### Performance Optimization
- Use React.memo for pure functional components
- Implement shouldComponentUpdate or React.PureComponent for class components
- Use useCallback for event handlers passed to child components
- Use useMemo for expensive calculations
- Avoid unnecessary re-renders
- Implement proper key props for lists
- Use virtualization for long lists

### Styling
- Use CSS modules or styled-components for component styling
- Follow BEM naming convention for CSS class names
- Use theme variables for colors, spacing, and typography
- Keep styles co-located with components
- Use responsive design principles
- Implement proper media queries
- Use CSS-in-JS libraries consistently

### Accessibility
- Use semantic HTML elements
- Implement proper ARIA attributes
- Ensure keyboard navigation works
- Provide alt text for images
- Use proper heading hierarchy
- Ensure sufficient color contrast
- Test with screen readers

## Examples

### Good Component Structure

```tsx
import React, { useState, useEffect, useCallback } from 'react';

import { User } from '../types/user';
import { fetchUserById } from '../api/users';
import { UserAvatar } from './UserAvatar';
import { ErrorMessage } from '../common/ErrorMessage';
import { LoadingSpinner } from '../common/LoadingSpinner';
import styles from './UserProfile.module.css';

interface UserProfileProps {
  userId: string;
  showDetails?: boolean;
  onUserLoad?: (user: User) => void;
}

/**
 * UserProfile component displays a user's profile information.
 */
export const UserProfile: React.FC<UserProfileProps> = ({
  userId,
  showDetails = false,
  onUserLoad,
}) => {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  const handleError = useCallback((err: unknown) => {
    setError(`Failed to load user: ${err instanceof Error ? err.message : 'Unknown error'}`);
  }, []);

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
          handleError(err);
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
  }, [userId, onUserLoad, handleError]);

  if (loading) {
    return <LoadingSpinner />;
  }

  if (error) {
    return <ErrorMessage message={error} />;
  }

  if (!user) {
    return <div className={styles.notFound}>User not found</div>;
  }

  return (
    <div className={styles.userProfile}>
      <div className={styles.header}>
        <UserAvatar user={user} size="large" />
        <h2 className={styles.userName}>{user.name}</h2>
      </div>
      
      <div className={styles.basicInfo}>
        <p className={styles.email}>Email: {user.email}</p>
        <p className={styles.status}>
          Status: <span className={styles[user.isActive ? 'active' : 'inactive']}>
            {user.isActive ? 'Active' : 'Inactive'}
          </span>
        </p>
      </div>
      
      {showDetails && (
        <div className={styles.details}>
          <h3>Additional Details</h3>
          <p>Member since: {new Date(user.createdAt).toLocaleDateString()}</p>
          <p>Last active: {new Date(user.lastActive).toLocaleDateString()}</p>
          <div className={styles.roles}>
            <h4>Roles:</h4>
            <ul>
              {user.roles.map(role => (
                <li key={role} className={styles.role}>{role}</li>
              ))}
            </ul>
          </div>
        </div>
      )}
    </div>
  );
};
```

### Good Custom Hook

```typescript
import { useState, useEffect, useCallback } from 'react';

/**
 * Custom hook for managing form state.
 * 
 * @param initialValues - Initial form values
 * @param validate - Validation function
 * @returns Form state, handlers, and submission utilities
 */
export function useForm<T extends Record<string, any>>(
  initialValues: T,
  validate?: (values: T) => Record<string, string>
) {
  const [values, setValues] = useState<T>(initialValues);
  const [errors, setErrors] = useState<Record<string, string>>({});
  const [touched, setTouched] = useState<Record<string, boolean>>({});
  const [isSubmitting, setIsSubmitting] = useState<boolean>(false);

  // Reset form to initial values
  const resetForm = useCallback(() => {
    setValues(initialValues);
    setErrors({});
    setTouched({});
    setIsSubmitting(false);
  }, [initialValues]);

  // Handle input change
  const handleChange = useCallback((
    e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement>
  ) => {
    const { name, value, type } = e.target;
    
    setValues(prevValues => ({
      ...prevValues,
      [name]: type === 'checkbox' 
        ? (e.target as HTMLInputElement).checked 
        : value
    }));
  }, []);

  // Handle input blur
  const handleBlur = useCallback((
    e: React.FocusEvent<HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement>
  ) => {
    const { name } = e.target;
    
    setTouched(prevTouched => ({
      ...prevTouched,
      [name]: true
    }));
  }, []);

  // Validate form values
  const validateForm = useCallback(() => {
    if (!validate) return {};
    
    const validationErrors = validate(values);
    setErrors(validationErrors);
    return validationErrors;
  }, [validate, values]);

  // Handle form submission
  const handleSubmit = useCallback((
    onSubmit: (values: T) => void | Promise<void>
  ) => async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    
    // Mark all fields as touched
    const allTouched = Object.keys(values).reduce(
      (acc, key) => ({ ...acc, [key]: true }),
      {}
    );
    setTouched(allTouched);
    
    // Validate form
    const validationErrors = validateForm();
    
    // If no errors, submit the form
    if (Object.keys(validationErrors).length === 0) {
      setIsSubmitting(true);
      
      try {
        await onSubmit(values);
      } catch (error) {
        console.error('Form submission error:', error);
      } finally {
        setIsSubmitting(false);
      }
    }
  }, [values, validateForm]);

  // Validate on touched fields change
  useEffect(() => {
    if (Object.keys(touched).length > 0) {
      validateForm();
    }
  }, [touched, validateForm]);

  return {
    values,
    errors,
    touched,
    isSubmitting,
    handleChange,
    handleBlur,
    handleSubmit,
    resetForm,
    setValues
  };
}
```

### Good Component Composition

```tsx
import React from 'react';

import { Card } from '../common/Card';
import { Button } from '../common/Button';
import { UserAvatar } from './UserAvatar';
import { UserBadge } from './UserBadge';
import styles from './UserCard.module.css';

interface UserCardProps {
  user: {
    id: string;
    name: string;
    email: string;
    role: string;
    avatarUrl?: string;
  };
  onEdit?: () => void;
  onDelete?: () => void;
}

export const UserCard: React.FC<UserCardProps> = ({
  user,
  onEdit,
  onDelete,
}) => {
  return (
    <Card className={styles.userCard}>
      <div className={styles.header}>
        <UserAvatar 
          user={user} 
          size="medium" 
          className={styles.avatar} 
        />
        <div className={styles.info}>
          <h3 className={styles.name}>{user.name}</h3>
          <p className={styles.email}>{user.email}</p>
          <UserBadge role={user.role} />
        </div>
      </div>
      
      <div className={styles.actions}>
        {onEdit && (
          <Button 
            variant="secondary" 
            onClick={onEdit}
            aria-label={`Edit ${user.name}`}
          >
            Edit
          </Button>
        )}
        
        {onDelete && (
          <Button 
            variant="danger" 
            onClick={onDelete}
            aria-label={`Delete ${user.name}`}
          >
            Delete
          </Button>
        )}
      </div>
    </Card>
  );
};
```

## Related MDC Files
- [typescript-glob.mdc](mdc:../typescript-glob.mdc)
- [css-modules-glob.mdc](mdc:../styling/css-modules-glob.mdc)
- [accessibility-glob.mdc](mdc:../accessibility/accessibility-glob.mdc)
- [testing-react-glob.mdc](mdc:../testing/testing-react-glob.mdc)

## Exceptions
- Generated React components (marked with a `// GENERATED COMPONENT` comment) are exempt from some style requirements
- Higher-order components may follow different patterns
- Legacy class components may be gradually migrated to functional components
- Third-party component libraries may have their own patterns

## Enforcement
- ESLint with React plugin is used to enforce React best practices
- React-specific linting rules are enabled
- Pre-commit hooks enforce these checks before commits
- CI/CD pipeline includes these checks for all pull requests
- Code reviews should verify adherence to these standards
- Component library documentation should follow these standards

## Version History
- 2023-09-01: Initial version
- 2023-10-15: Added accessibility guidelines
- 2023-12-05: Updated component organization rules
- 2024-02-10: Added custom hooks section and examples
- 2024-03-20: Updated styling guidelines 