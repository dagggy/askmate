
DROP TABLE IF EXISTS public.user;
ALTER TABLE IF EXISTS ONLY public.user_data DROP CONSTRAINT IF EXISTS pk_user_id CASCADE;

DROP TABLE IF EXISTS public.user_data;
CREATE TABLE public.user_data (
    user_id serial NOT NULL,
    login text,
    password text,
    username_link text,
    registration_date timestamp without time zone,
    questions_number integer,
    answers_number integer,
    comments_number integer,
    user_reputation integer
);

INSERT INTO public.user_data VALUES (1, 'user1@gmai.com', '$2b$12$p3dQ4fBedKSzzYpzjPDDLuHS5TJUJ1oTl6OAFinNkETgPGreIa/YW',NULL, '2017-04-28 08:29:00', 2, 7, 1, 5);
