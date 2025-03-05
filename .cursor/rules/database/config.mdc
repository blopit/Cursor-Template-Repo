---
description: Guidelines for database configuration, management, and optimization
globs: **/*.{sql,prisma,js,ts,py,java,rb,php,go}
version: 1.0.0
author: Cursor AI
tags: database, configuration, optimization, security, migrations
---

# Database Configuration Guidelines

This document defines guidelines for database configuration, management, and optimization across different environments and database systems.

## Database Selection Criteria

When selecting a database system, consider the following criteria:

1. **Data Model**: Relational, document, key-value, graph, or time-series
2. **Scalability Requirements**: Vertical vs. horizontal scaling needs
3. **Consistency Requirements**: ACID compliance vs. eventual consistency
4. **Performance Requirements**: Read vs. write optimization
5. **Operational Complexity**: Managed service vs. self-hosted
6. **Cost Considerations**: Licensing, hosting, and operational costs
7. **Ecosystem Integration**: Tools, libraries, and community support
8. **Security Features**: Authentication, encryption, and compliance capabilities

## Primary Database: PostgreSQL

### Configuration Guidelines

#### Basic Configuration

```ini
# postgresql.conf basic settings
listen_addresses = '*'
max_connections = 100
shared_buffers = 256MB
effective_cache_size = 768MB
maintenance_work_mem = 64MB
checkpoint_completion_target = 0.9
wal_buffers = 16MB
default_statistics_target = 100
random_page_cost = 1.1
effective_io_concurrency = 200
work_mem = 4MB
min_wal_size = 1GB
max_wal_size = 4GB
```

#### Performance Tuning

Adjust these parameters based on available system resources:

| Parameter | Small (2GB RAM) | Medium (8GB RAM) | Large (32GB RAM) |
|-----------|----------------|-----------------|------------------|
| `shared_buffers` | 512MB | 2GB | 8GB |
| `effective_cache_size` | 1.5GB | 6GB | 24GB |
| `work_mem` | 4MB | 16MB | 64MB |
| `maintenance_work_mem` | 64MB | 256MB | 1GB |
| `max_connections` | 100 | 200 | 400 |

#### Security Configuration

```ini
# Security settings
ssl = on
ssl_cert_file = 'server.crt'
ssl_key_file = 'server.key'
ssl_ciphers = 'HIGH:!aNULL:!MD5'
password_encryption = scram-sha-256
```

### Connection Management

#### Connection Pooling with PgBouncer

```ini
# pgbouncer.ini
[databases]
* = host=localhost port=5432 dbname=app

[pgbouncer]
listen_addr = *
listen_port = 6432
auth_type = md5
auth_file = /etc/pgbouncer/userlist.txt
pool_mode = transaction
max_client_conn = 1000
default_pool_size = 20
```

#### Application Connection Configuration

```javascript
// Node.js with Prisma example
// .env
DATABASE_URL="postgresql://username:password@localhost:6432/app?schema=public&connection_limit=5"

// prisma/schema.prisma
datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
}
```

```python
# Python with SQLAlchemy example
from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool

engine = create_engine(
    "postgresql://username:password@localhost:6432/app",
    poolclass=QueuePool,
    pool_size=5,
    max_overflow=10,
    pool_timeout=30,
    pool_recycle=1800,
)
```

## Environment-Specific Configuration

### Development Environment

```ini
# Development PostgreSQL settings
log_statement = 'all'
log_duration = on
debug_print_parse = on
debug_print_rewritten = on
debug_print_plan = on
```

```javascript
// Development connection string
DATABASE_URL="postgresql://dev_user:dev_password@localhost:5432/app_dev?schema=public"
```

### Testing Environment

```ini
# Testing PostgreSQL settings
fsync = off
synchronous_commit = off
full_page_writes = off
```

```javascript
// Testing connection string
DATABASE_URL="postgresql://test_user:test_password@localhost:5432/app_test?schema=public"
```

### Production Environment

```ini
# Production PostgreSQL settings
log_statement = 'none'
log_duration = off
log_min_duration_statement = 1000
```

```javascript
// Production connection string with connection pooling
DATABASE_URL="postgresql://app_user:strong_password@db.example.com:6432/app_prod?schema=public&connection_limit=10&ssl=true&sslmode=require"
```

## Schema Management

### Migration Strategy

1. **Version-controlled migrations**: Use tools like Prisma Migrate, Flyway, or Alembic
2. **Forward and backward compatibility**: Ensure migrations can be rolled back
3. **Non-destructive changes**: Prefer additive changes over destructive ones
4. **Staged migrations**: Split complex migrations into smaller, safer steps

### Example Prisma Migration

```prisma
// prisma/schema.prisma
model User {
  id        String   @id @default(cuid())
  email     String   @unique
  name      String?
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt
  
  @@index([email])
}
```

```bash
# Generate and apply migration
npx prisma migrate dev --name add_user_model
```

### Database Versioning Best Practices

1. **One change per migration**: Each migration should make a single logical change
2. **Descriptive names**: Use clear, descriptive names for migration files
3. **Test migrations**: Test migrations in development before applying to production
4. **Document breaking changes**: Clearly document any breaking changes
5. **Include seed data**: Provide seed data for development and testing

## Indexing Strategy

### Index Types

1. **B-tree indexes**: Default index type, good for equality and range queries
2. **Hash indexes**: Optimized for equality comparisons
3. **GIN indexes**: Good for composite values like arrays and JSON
4. **BRIN indexes**: Block Range INdexes for large tables with ordered data
5. **Partial indexes**: Index only a subset of rows that match a condition

### Indexing Guidelines

```sql
-- Primary key (automatically indexed)
CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  email VARCHAR(255) NOT NULL,
  name VARCHAR(255)
);

-- Index for frequent lookups
CREATE INDEX idx_users_email ON users(email);

-- Composite index for queries that filter on multiple columns
CREATE INDEX idx_users_name_email ON users(name, email);

-- Partial index for specific queries
CREATE INDEX idx_active_users ON users(last_login) WHERE status = 'active';

-- Expression index
CREATE INDEX idx_users_lower_email ON users(LOWER(email));
```

### Index Maintenance

```sql
-- Analyze table to update statistics
ANALYZE users;

-- Rebuild index to remove bloat
REINDEX INDEX idx_users_email;

-- Monitor index usage
SELECT indexrelname, idx_scan, idx_tup_read, idx_tup_fetch
FROM pg_stat_user_indexes
JOIN pg_stat_user_tables ON idx_rel_id = relid
WHERE schemaname = 'public';
```

## Query Optimization

### Query Performance Guidelines

1. **Use prepared statements**: Avoid SQL injection and improve performance
2. **Limit result sets**: Use LIMIT and pagination
3. **Select only needed columns**: Avoid SELECT *
4. **Use appropriate joins**: Choose the right join type (INNER, LEFT, etc.)
5. **Optimize subqueries**: Consider using JOINs instead of subqueries
6. **Use EXISTS instead of IN**: For better performance with large datasets
7. **Batch operations**: Use bulk inserts and updates

### Example Optimized Queries

```sql
-- Bad: Selecting all columns, no limit
SELECT * FROM users WHERE status = 'active';

-- Good: Selecting only needed columns with limit
SELECT id, email, name FROM users WHERE status = 'active' LIMIT 100;

-- Bad: Using a subquery
SELECT * FROM orders WHERE user_id IN (SELECT id FROM users WHERE status = 'active');

-- Good: Using a join
SELECT o.* FROM orders o
JOIN users u ON o.user_id = u.id
WHERE u.status = 'active';

-- Using EXISTS for better performance
SELECT * FROM orders o
WHERE EXISTS (SELECT 1 FROM users u WHERE u.id = o.user_id AND u.status = 'active');
```

## Caching Strategy

### Application-Level Caching

```javascript
// Redis caching example with Node.js
const redis = require('redis');
const client = redis.createClient({
  url: 'redis://localhost:6379'
});

async function getUserById(id) {
  // Try to get from cache first
  const cachedUser = await client.get(`user:${id}`);
  if (cachedUser) {
    return JSON.parse(cachedUser);
  }
  
  // If not in cache, get from database
  const user = await db.user.findUnique({ where: { id } });
  
  // Store in cache with expiration
  if (user) {
    await client.set(`user:${id}`, JSON.stringify(user), {
      EX: 3600 // Expire after 1 hour
    });
  }
  
  return user;
}
```

### Database Query Caching

```sql
-- Create a materialized view for expensive queries
CREATE MATERIALIZED VIEW user_stats AS
SELECT 
  u.id,
  u.name,
  COUNT(o.id) AS order_count,
  SUM(o.total) AS total_spent
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
GROUP BY u.id, u.name;

-- Create an index on the materialized view
CREATE INDEX idx_user_stats_id ON user_stats(id);

-- Refresh the materialized view
REFRESH MATERIALIZED VIEW user_stats;
```

## Backup and Recovery

### Backup Strategy

1. **Regular full backups**: Daily or weekly full database dumps
2. **Continuous WAL archiving**: For point-in-time recovery
3. **Offsite storage**: Store backups in a separate location
4. **Backup verification**: Regularly test restores from backups

### Backup Commands

```bash
# PostgreSQL full backup
pg_dump -U username -d dbname -F custom -f backup.dump

# Incremental backup with WAL archiving
# In postgresql.conf:
# wal_level = replica
# archive_mode = on
# archive_command = 'cp %p /path/to/archive/%f'

# Restore from backup
pg_restore -U username -d dbname -F custom backup.dump
```

## Security Best Practices

### Authentication and Authorization

```sql
-- Create a role with limited privileges
CREATE ROLE app_user WITH LOGIN PASSWORD 'strong_password';

-- Grant specific privileges
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO app_user;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO app_user;

-- Revoke public privileges
REVOKE CREATE ON SCHEMA public FROM PUBLIC;
```

### Data Encryption

1. **Connection encryption**: Use SSL/TLS for all connections
2. **Data-at-rest encryption**: Use filesystem or volume encryption
3. **Sensitive data encryption**: Encrypt sensitive columns

```sql
-- Enable pgcrypto extension
CREATE EXTENSION pgcrypto;

-- Encrypt sensitive data
UPDATE users SET 
  credit_card = pgp_sym_encrypt(credit_card, 'encryption_key');

-- Decrypt data when needed
SELECT pgp_sym_decrypt(credit_card::bytea, 'encryption_key') 
FROM users WHERE id = 123;
```

## Monitoring and Maintenance

### Key Metrics to Monitor

1. **Connection count**: Number of active connections
2. **Query performance**: Slow query log and execution times
3. **Index usage**: Unused and inefficient indexes
4. **Cache hit ratio**: Buffer cache effectiveness
5. **Disk usage**: Database and table sizes
6. **Replication lag**: For replicated setups
7. **Lock contention**: Blocked queries and deadlocks

### Maintenance Tasks

```sql
-- Update statistics
ANALYZE;

-- Reclaim space and optimize tables
VACUUM FULL;

-- Rebuild indexes
REINDEX DATABASE dbname;

-- Find slow queries
SELECT query, calls, total_time, rows, mean_time
FROM pg_stat_statements
ORDER BY total_time DESC
LIMIT 10;
```

## Common Pitfalls

1. **Connection leaks**: Not properly closing database connections
2. **N+1 query problem**: Making a query for each item in a collection
3. **Over-indexing**: Creating too many indexes, slowing down writes
4. **Under-indexing**: Missing indexes on frequently queried columns
5. **Large transactions**: Long-running transactions causing lock contention
6. **String concatenation in queries**: Leading to SQL injection vulnerabilities
7. **Ignoring database logs**: Missing important error messages and warnings

## Related Rules

- [stack/stack-definition](../stack/stack-definition.mdc): Technology stack definition
- [patterns/error-handling](../patterns/error-handling.mdc): Error handling guidelines
- [lessons/technical/database-config](../lessons/technical/database-config.mdc): Database configuration lessons

## References

- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Prisma Documentation](https://www.prisma.io/docs)
- [Database Indexing Strategies](https://use-the-index-luke.com/)
- [SQL Performance Explained](https://sql-performance-explained.com/)

## Changelog

- 1.0.0: Initial version 
