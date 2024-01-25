CREATE TABLE authority (
    cd SMALLSERIAL PRIMARY KEY,
    name VARCHAR(30),
    adminflg VARCHAR(1),
    deleteflg VARCHAR(1),
    created_at DATE,
    updated_at DATE
);