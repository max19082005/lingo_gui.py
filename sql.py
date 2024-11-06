import sqlite3


def init_database():
    connection = sqlite3.connect("lingo.db")
    cursor = connection.cursor()
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS words (id INTEGER PRIMARY KEY AUTOINCREMENT, word TEXT, tip TEXT)")
    connection.commit()
    connection.close()


def drop_database():
    connection = sqlite3.connect("lingo.db")
    cursor = connection.cursor()
    cursor.execute("DROP TABLE IF EXISTS words")
    connection.commit()
    connection.close()


def recreate_table():
    drop_database()
    connection = sqlite3.connect("lingo.db")
    cursor = connection.cursor()
    """ADD SOMETHING NEW TO THIS TABLE"""
    cursor.execute(
        "CREATE TABLE words (id INTEGER PRIMARY KEY AUTOINCREMENT, word TEXT, tip TEXT)")
    connection.commit()
    connection.close()


def add_word_to_database(word: str, tip: str):
    connection = sqlite3.connect("lingo.db")
    cursor = connection.cursor()
    cursor.execute("INSERT INTO words (word, tip) VALUES (?, ?)",
                   (word.capitalize(), tip,))
    connection.commit()
    connection.close()


def print_all_records():
    connection = sqlite3.connect("lingo.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM words")
    records = cursor.fetchall()
    for record in records:
        print(record)
    connection.close()


def get_words_from_database():
    # Получение списка слов из базы данных
    connection = sqlite3.connect("lingo.db")
    cursor = connection.cursor()
    cursor.execute("SELECT word FROM words")
    words = cursor.fetchall()
    connection.close()
    words = [word[0] for word in words]
    return words


def get_tips_from_database(word):
    # Получение списка слов из базы данных
    connection = sqlite3.connect("lingo.db")
    cursor = connection.cursor()
    print("get_tips_from_database: " + word)
    cursor.execute(f"SELECT tip FROM words WHERE word='{word}'")
    tips = cursor.fetchall()
    connection.close()
    print(tips)
    return tips[0][0]


def delete_word_from_database(word):
    connection = sqlite3.connect("lingo.db")
    cursor = connection.cursor()
    cursor.execute("DELETE FROM words WHERE word=?", (word,))
    connection.commit()
    connection.close()

word_tip_list = [
    # ("Stoel", "Waar ze op zitten"),
    ("Tafel", "Waar je aan eet"),
    ("Fiets", "Twee wielen en trappers"),
    ("Bloem", "Heeft mooie kleuren"),
    ("Water", "Een vloeistof"),
    ("Lucht", "Om in te ademen"),
    ("Aarde", "De planeet waar we op wonen"),
    ("Wolke", "In de lucht"),
    ("Radio", "Apparaat voor geluid"),
    ("Feest", "Gelegenheid om te vieren"),
    ("Sport", "Fysieke activiteit"),
    ("Fruit", "Eetbaar voedsel"),
    ("Slang", "Glibberig dier"),
    ("Haven", "Plaats voor schepen"),
    ("Truck", "Groot voertuig"),
    ("Steen", "Hard materiaal"),
    ("Steen", "Hard materiaal"),
    ("Pizza", "Gebakken deeg met beleg"),
    ("Vogel", "Vliegend dier"),
    ("Stift", "Schrijfinstrument"),
    ("Piano", "Muziekinstrument"),
    ("Wagen", "Voertuig"),
    ("Bakje", "Klein container"),
    ("Grote", "Van grote omvang"),
    ("Pasta", "Deegproduct"),
    ("Boven", "Niet lager"),
    ("Garen", "Draad voor naaien"),
    ("Bosje", "Een paar dingen bij elkaar"),
    ("Bende", "Groep mensen"),
    ("Boter", "Zuivelproduct"),
    ("Koers", "Richting"),
    ("Radar", "Detectiesysteem"),
    ("Bakje", "Klein container"),
    ("Peper", "Kruid"),
    ("Laken", "Beddengoed"),]


if __name__ == "__main__":
    init_database()
    recreate_table()
    for word, tip in word_tip_list:
        add_word_to_database(word=word, tip=tip)
    print_all_records()