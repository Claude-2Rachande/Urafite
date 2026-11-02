# URAFITE multilingual QA notes

## Languages covered
- English (`en`)
- Kinyarwanda (`rw`)
- French (`fr`)

## UI areas reviewed in `app.py`
- Pre-login language selector, sign-in tabs, registration form, validation and authentication messages
- Sidebar navigation, role labels, sign-out and language selector
- Home page and the three pathway cards
- RECOVER check-in, choice labels, reflections, guidance and support notices
- REBUILD budgeting fields, goal choices, metrics and explanatory notices
- RECONNECT interests, education/career choices, example pathways and action-plan controls
- Hiro text/voice controls, privacy notices, predefined response categories and browser speech error message
- Professional Support guidance and safety notices
- Supabase setup/session errors shown in the application

## Implementation notes
- English remains the internal value for application logic; translated labels are used for display.
- The selected language can be chosen before sign-in.
- A newly registered profile receives the selected language through signup metadata and the database trigger.
- On sign-in, the saved profile language is restored unless the user explicitly selected another language during the current visit.
- Changing language while signed in attempts to save the preference to `profiles.preferred_language`.
- The Supabase publishable key is used; the secret/service-role key is not required by this app.

## Validation performed
- Python syntax compilation passed (`python -m py_compile app.py`).
- Static audit checked the user-facing Streamlit labels and static choice options against both translation dictionaries.
- Remaining untranslated static title strings are the URAFITE brand and pathway names; these are intentional product labels, not mixed-language sentences.

## Manual checks still required on the deployed/local browser
1. Test each language before sign-in, then inspect both sign-in and registration tabs.
2. Sign in and visit Home, RECOVER, REBUILD, RECONNECT, Hiro, and Professional Support in each language.
3. Change language from the sidebar and confirm labels, helper text, options, metrics and notices update together.
4. Sign out and back in to confirm the saved language is restored.
5. Test voice mode separately. Browser speech voices may not support Kinyarwanda even when the interface and transcript are in Kinyarwanda.

## Scope limitations
- The opportunity examples in this MVP are illustrative, not verified live vacancies or scholarships.
- The current package does not yet include the full administrator content-management interface or automated analytics dashboard discussed for later development.
- Kinyarwanda and French wording should receive native-speaker/professional review before public launch, especially recovery and safeguarding language.
