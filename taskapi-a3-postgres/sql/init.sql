-- Reference copy of the schema. The app creates this automatically on
-- startup (see app/repository.py: init_table()), so you never need to run
-- this by hand — it's here so the schema is visible without reading code.

CREATE TABLE IF NOT EXISTS tasks (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    done BOOLEAN NOT NULL DEFAULT FALSE
);
