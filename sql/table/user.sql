CREATE TABLE muser (
    id SMALLSERIAL PRIMARY KEY,
    engname VARCHAR(15),
    jpnname VARCHAR(20),
    password VARCHAR(20),
    authcd VARCHAR(1),
    deleteflg VARCHAR(1),
    created_at DATE,
    updated_at DATE
)