--
-- ���� ������������ � ������� SQLiteStudio v3.3.3 � �� ��� 16 14:33:55 2021
--
-- �������������� ��������� ������: System
--
PRAGMA foreign_keys = off;
BEGIN TRANSACTION;

-- �������: my_messages
CREATE TABLE my_messages (
    id         INTEGER NOT NULL
                       PRIMARY KEY
                       UNIQUE,
    message_id INTEGER NOT NULL
                       UNIQUE,
    message    TEXT    UNIQUE
                       NOT NULL
);


COMMIT TRANSACTION;
PRAGMA foreign_keys = on;
