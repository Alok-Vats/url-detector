# Database Migrations

This folder contains a normalized target schema for the project database.

## Migration order

1. `migrations/001_create_reputation_tables.sql`
2. `migrations/002_create_model_and_scan_tables.sql`
3. `migrations/003_create_indexes.sql`
4. `migrations/004_seed_reputation_lists.sql`

## Example usage with SQLite

```bash
sqlite3 database/project.sqlite < database/migrations/001_create_reputation_tables.sql
sqlite3 database/project.sqlite < database/migrations/002_create_model_and_scan_tables.sql
sqlite3 database/project.sqlite < database/migrations/003_create_indexes.sql
sqlite3 database/project.sqlite < database/migrations/004_seed_reputation_lists.sql
```

See [docs/database-schema.md](/home/n0b0dy/Desktop/mProject/docs/database-schema.md) for the table design and [database/queries/example_queries.sql](/home/n0b0dy/Desktop/mProject/database/queries/example_queries.sql) for common SQL examples.
