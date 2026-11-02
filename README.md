# URAFITE — Emergency delivery build

This package is the enhanced version of the project you uploaded as `URAFITE1.zip`.

## Included
- Multilingual Streamlit app (English, Kinyarwanda, French)
- Supabase email/password authentication
- RECOVER, REBUILD, RECONNECT, Hiro, Professional Support
- User-facing **Heal and Learn Centre**
- Administrator-only pages: Administration, Impact & Evidence, Opportunity Manager, Heal and Learn Centre Manager, Grant & Programme Tracker
- Existing database migration reference: `database/002_profile_and_default_role_trigger.sql`

## IMPORTANT: Existing Supabase project
Your current Supabase project was inspected during this session. It already contains:
- `profiles`, `user_roles`, `opportunities`, `learning_resources`, `platform_events`, `grant_records`
- the three functions `handle_new_user`, `has_admin_role`, `is_super_admin`
- the `on_auth_user_created` trigger
- your `super_admin` account
- RLS policies on all six tables

**Do not run an additional schema migration just because it is included in a package.**
This build does not include the earlier `003_impact_and_reporting.sql`, because your existing database already has `grant_records` and its current policies. Replacing those policies without a full policy review could change access controls.

The `002` file is retained as a reference for a fresh installation. Do not rerun it on the existing project unless there is a specific reason and you have a database backup.

## Configure locally (Windows / Git Bash)
1. Extract this ZIP into a NEW folder. Keep your old project as a backup.
2. Copy `.streamlit/secrets.toml.example` to `.streamlit/secrets.toml`.
3. Put your Supabase Project URL and **publishable key** in `secrets.toml`:
   ```toml
   SUPABASE_URL = "https://YOUR_PROJECT_REF.supabase.co"
   SUPABASE_KEY = "sb_publishable_..."
   ```
4. Never put the secret/service-role key in this Streamlit app or GitHub.
5. In Git Bash, open the new folder and run:
   ```bash
   python -m venv venv
   source venv/Scripts/activate
   pip install -r requirements.txt
   streamlit run app.py
   ```

## First test (do these in order)
1. Sign in using your existing super-admin account.
2. Confirm the sidebar identifies the Super Administrator.
3. Open Administration.
4. Open Opportunity Manager and check that existing rows load. Do not publish test information publicly.
5. Open Heal and Learn Centre Manager; check existing resources load.
6. Open Grant & Programme Tracker; check existing grant rows load.
7. Open Impact & Evidence; confirm counts load.
8. Sign out and test a normal user account. Confirm management pages are not accessible.

If any page shows a Supabase error, copy the full error text (but never share credentials or access tokens) and fix that before deployment.

## Deploy
- Push the project to GitHub, excluding `.streamlit/secrets.toml`.
- Create/deploy the Streamlit Community Cloud app with `app.py` as the entry point.
- Add `SUPABASE_URL` and `SUPABASE_KEY` in Streamlit Cloud app Secrets.
- Test the deployed URL using your super-admin account before sharing it.

## Honest MVP limitations
- Hiro uses predefined responses; it is not connected to a live AI model.
- `platform_events` exists, but this app build does not automatically log every user interaction. The activity chart may be empty or incomplete until event tracking is implemented.
- Impact counts describe platform usage and content records, not verified recovery outcomes or clinical impact.
- No public launch should collect sensitive recovery disclosures or detailed personal financial information without reviewed consent, safeguarding, retention and privacy controls.
- The app was syntax-checked and its ZIP integrity was checked. It has **not** been tested against your live Supabase project or deployed to Streamlit Cloud in this session.
