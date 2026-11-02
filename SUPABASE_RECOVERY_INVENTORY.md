# URAFITE Supabase recovery inventory

This inventory is based on the user's Supabase SQL exports and screenshots shared during the recovery session. It is documentation, not a full database backup.

## Confirmed public tables and columns

- `profiles`: `id uuid`, `email text`, `display_name text`, `preferred_language text`, `created_at timestamptz`, `updated_at timestamptz`
- `user_roles`: `id bigint`, `user_id uuid`, `role text`, `created_at timestamptz`
- `opportunities`: `id uuid`, `title text`, `category text`, `organisation text`, `country text`, `description text`, `eligibility text`, `application_url text`, `deadline date`, `status text`, `created_by uuid`, `created_at timestamptz`, `updated_at timestamptz`
- `learning_resources`: `id uuid`, `title text`, `resource_type text`, `category text`, `description text`, `content_url text`, `language text`, `contributor_name text`, `professional_credentials text`, `status text`, `created_by uuid`, `created_at timestamptz`, `updated_at timestamptz`
- `platform_events`: `id bigint`, `user_id uuid`, `event_type text`, `related_record_id uuid`, `metadata jsonb`, `created_at timestamptz`
- `grant_records`: `id uuid`, `funder text`, `project_name text`, `award_amount numeric`, `target_participants integer`, `start_date date`, `end_date date`, `reporting_deadline date`, `status text`, `notes text`, `created_by uuid`, `created_at timestamptz`, `updated_at timestamptz`

## Confirmed references to auth.users

- `profiles.id` -> `auth.users.id` (ON DELETE CASCADE)
- `user_roles.user_id` -> `auth.users.id` (ON DELETE CASCADE)
- `opportunities.created_by` -> `auth.users.id` (default delete behaviour)
- `learning_resources.created_by` -> `auth.users.id` (default delete behaviour)
- `platform_events.user_id` -> `auth.users.id` (ON DELETE SET NULL)
- `grant_records.created_by` -> `auth.users.id` (ON DELETE SET NULL)

No foreign keys directly between the six public tables were returned by the export.

## Other confirmed configuration
- RLS enabled on all six tables.
- 27 RLS policies exported. Duplicate/overlapping policy names exist; do not remove policies without reviewing complete expressions.
- Functions: `handle_new_user()`, `has_admin_role()`, `is_super_admin()`.
- Trigger: `auth.on_auth_user_created`, AFTER INSERT on `auth.users`, calls `handle_new_user()`.
- Existing user account was verified with role `super_admin`.
- 18 indexes were exported. Some indexes may overlap; do not drop them without query-plan and usage review.

## Not included / not yet recovered
- A full SQL schema dump with exact CREATE TABLE / CREATE POLICY statements.
- Actual user/content/event/grant table data.
- All exact index definitions and complete constraint definitions in executable migration form.
- Auth provider settings, email templates, redirect URLs, storage buckets, secrets, Edge Functions, and project-level settings.

For a real backup, use Supabase's supported database backup/export process or `pg_dump` with appropriate database credentials. Never place passwords, access tokens, or service-role keys in this folder or GitHub.
