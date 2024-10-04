BEGIN;

CREATE USER sql_misconceptions_admin WITH PASSWORD 'sql';

-- Grant create schema privileges
GRANT CREATE ON DATABASE postgres TO sql_misconceptions_admin;

COMMIT;