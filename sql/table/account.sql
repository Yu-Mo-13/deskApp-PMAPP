CREATE TABLE account (
    id SERIAL PRIMARY KEY,
    account VARCHAR(100),
    app VARCHAR(200),
    deleteflg VARCHAR(1),
    created_at DATE,
    updated_at DATE
);
