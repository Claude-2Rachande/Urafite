# URAFITE administration and impact QA

## Included in this build
- Administrator-only navigation, gated by the authenticated `admin` or `super_admin` role.
- Impact & Evidence dashboard with aggregate counts and CSV exports.
- Opportunity creation and status management.
- Heal and Learn Centre: published resources filtered by selected language.
- Heal and Learn Centre Manager: submit resources for review and approve/reject them.
- Grant & Programme Tracker with basic funding records and CSV export.
- English, Kinyarwanda and French labels for the newly added management pages.

## Required setup
1. Run `database/003_impact_and_reporting.sql` in Supabase SQL Editor.
2. Confirm the current signed-in account has `super_admin` in `public.user_roles`.
3. Restart Streamlit and test each admin page.

## Important limitations
- This is an initial administration/impact MVP, not a full M&E system.
- Platform event instrumentation in all existing user workflows is not yet complete, so event charts may initially be empty.
- User registration counts, published content and grant records are read from Supabase.
- Grant expenditure, budgets, verified outcome surveys, evidence uploads, donor-specific report templates, contributor self-service accounts and detailed audit logs are not implemented yet.
- Language strings added in this module have been translated in code, but native-speaker review and browser QA are still required.
- No live Supabase or browser test was performed during package generation.
