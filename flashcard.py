import sqlite3
import datetime


def init_db():
    conn = sqlite3.connect("flashcard.db")
    cursor = conn.cursor()
    cursor.execute('''
        PRAGMA foreign_keys = ON
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cards (
            id INTEGER PRIMARY KEY,
            question TEXT,
            reponse TEXT,
            probabilite REAL,
            id_theme INTEGER,
            FOREIGN KEY (id_theme) REFERENCES themes(id) ON DELETE RESTRICT)
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS themes (
            id INTEGER PRIMARY KEY,
            theme TEXT)
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS stats (
            id INTEGER PRIMARY KEY,
            bonnes_reponses INTEGER,
            mauvaises_reponses INTEGER,
            date DATE)
    ''')

    #insert theme
    cursor.execute('''
        INSERT INTO themes(id, theme) VALUES
            (1, 'Phyton'),
            (2, 'Java'),
            (3, 'JavaScript')
    ''')
    conn.commit()
    cursor.close()

#init_db()

def create_card(question, reponse, probabilite, id_theme):
    conn = sqlite3.connect("flashcard.db")
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO cards (question, reponse, probabilite, id_theme)
        VALUES (?, ?, ?, ?)
    ''', (question, reponse, probabilite, id_theme))
    conn.commit()
    cursor.close()

def get_card(id):
    conn = sqlite3.connect("flashcard.db")
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM cards WHERE id = ?
    ''', (id,))
    card = cursor.fetchone()[0]
    cursor.close()
    return card

def update_card(id, question, response, probabilite, id_theme):
    conn = sqlite3.connect("flashcard.db")
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE cards
        SET question = ?, reponse = ?, probabilite = ?, id_theme = ?
        WHERE id = ?
    ''', (question, response, probabilite, id_theme, id))
    conn.commit()
    cursor.close()

def delete_card(id):
    conn = sqlite3.connect("flashcard.db")
    cursor = conn.cursor()
    cursor.execute('''
        DELETE FROM cards WHERE id = ?
    ''', (id,))
    conn.commit()
    cursor.close()

def get_all_cards():
    conn = sqlite3.connect("flashcard.db")
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM cards
    ''')
    cards = cursor.fetchall()
    cursor.close()
    return cards

def get_number_of_cards():
    conn = sqlite3.connect("flashcard.db")
    cursor = conn.cursor()
    cursor.execute('''
        SELECT COUNT(*) FROM cards
    ''')
    count = cursor.fetchone()[0]
    cursor.close()
    return count

def get_cards_by_theme(id_theme):
    conn = sqlite3.connect("flashcard.db")
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM cards WHERE id_theme = ?
    ''', (id_theme,))
    cards = cursor.fetchall()
    cursor.close()
    return cards

#Crud theme
def create_theme(theme):
    conn = sqlite3.connect("flashcard.db")
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON;")
    cursor.execute('''
        INSERT INTO themes (theme)
        VALUES (?)
    ''', (theme,))
    conn.commit()
    cursor.close()

def get_theme(id):
    conn = sqlite3.connect("flashcard.db")
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM themes WHERE id = ?
    ''', (id,))
    theme = cursor.fetchone()[0]
    cursor.close()
    return theme

def update_theme(id_theme, theme):
    conn = sqlite3.connect("flashcard.db")
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE themes
        SET theme = ?
        WHERE id = ?
    ''', (theme, id_theme))
    conn.commit()
    cursor.close()

def delete_theme(id_theme):
    conn = sqlite3.connect("flashcard.db")
    cursor = conn.cursor()
    cursor.execute('''
        DELETE FROM themes WHERE id = ?
    ''', (id_theme,))
    conn.commit()
    cursor.close()

def get_all_themes():
    conn = sqlite3.connect("flashcard.db")
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM themes
    ''')
    themes = cursor.fetchall()
    cursor.close()
    return themes

#Stats
def update_stats(is_correct):
    conn = sqlite3.connect("flashcard.db")
    cursor = conn.cursor()
    today = datetime.now().strftime("%Y-%m-%d")
    cursor.execute('SELECT * FROM stats WHERE date = ?', (today,))
    stats = cursor.fetchone()
    if len(stats) > 0:
        if is_correct:
            cursor.execute('''
                UPDATE stats
                SET bonnes_reponses = bonnes_reponses + 1
                WHERE id = ?
            ''', (stats[0],))
        else:
            cursor.execute('''
                UPDATE stats
                SET mauvaises_reponses = mauvaises_reponses + 1
                WHERE id = ?
            ''', (stats[0],))
        conn.commit()
        cursor.close()
    else:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO stats (date, bonnes_reponses, mauvaises_reponses)
            VALUES (?, ?, ?)
        ''', (today, 1 if is_correct else 0, 0 if is_correct else 1))
        conn.commit()
        cursor.close()

def update_card_probability(card_id, is_correct):
    conn = sqlite3.connect("flashcard.db")
    cursor = conn.cursor()
    cursor.execute('''
        SELECT probabilite FROM cards WHERE id = ?
    ''', (card_id,))
    card = cursor.fetchone()

    cursor.execute('''
        UPDATE cards
        SET probabilite = probabilite + ?
        WHERE id = ?
    ''', (1 if is_correct else -1, card_id))
    conn.commit()
    cursor.close()

def get_stats():
    conn = sqlite3.connect("flashcard.db")
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM stats')
    stats = cursor.fetchall()
    cursor.close()
    return stats