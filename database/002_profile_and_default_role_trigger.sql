-- URAFITE migration: preserve signup language and create default user role.
-- Run once in Supabase SQL Editor after deploying the initial schema.

CREATE OR REPLACE FUNCTION public.handle_new_user()
RETURNS TRIGGER
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = public
AS $$
BEGIN
    INSERT INTO public.profiles (id, email, display_name, preferred_language)
    VALUES (
        NEW.id,
        NEW.email,
        COALESCE(NEW.raw_user_meta_data ->> 'display_name', ''),
        CASE
            WHEN NEW.raw_user_meta_data ->> 'preferred_language' IN ('en', 'rw', 'fr')
            THEN NEW.raw_user_meta_data ->> 'preferred_language'
            ELSE 'en'
        END
    );

    INSERT INTO public.user_roles (user_id, role)
    VALUES (NEW.id, 'user')
    ON CONFLICT (user_id, role) DO NOTHING;

    RETURN NEW;
END;
$$;

-- The existing on_auth_user_created trigger continues to call this function.
