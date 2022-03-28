--
-- Файл сгенерирован с помощью SQLiteStudio v3.3.3 в Чт дек 16 14:33:55 2021
--
-- Использованная кодировка текста: System
--
PRAGMA foreign_keys = off;
BEGIN TRANSACTION;

-- Таблица: my_messages
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
