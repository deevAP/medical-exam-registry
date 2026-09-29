import sqlite3

def init_db():
    conn = sqlite3.connect("e_rejestracja_badan.db")
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS patients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            pesel TEXT UNIQUE NOT NULL
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS exams (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            exam_name TEXT NOT NULL,
            price REAL NOT NULL
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS registrations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER,
            exam_id INTEGER,
            registration_date TEXT NOT NULL,
            status TEXT DEFAULT 'Zaplanowane',
            FOREIGN KEY (patient_id) REFERENCES patients (id),
            FOREIGN KEY (exam_id) REFERENCES exams (id)
        )
    """)
    
    cursor.execute("SELECT COUNT(*) FROM exams")
    if cursor.fetchone()[0] == 0:
        default_exams = [
            ("Rezonans Magnetyczny (MRI)", 450.0),
            ("Tomografia Komputerowa (TK)", 350.0),
            ("USG Jamy Brzusznej", 150.0),
            ("Badanie krwi - Morfologia", 30.0)
        ]
        cursor.executemany("INSERT INTO exams (exam_name, price) VALUES (?, ?)", default_exams)

    conn.commit()
    conn.close()

def add_patient():
    print("\n--- REJESTRACJA NOWEGO PACJENTA ---")
    first_name = input("Podaj imię: ")
    last_name = input("Podaj nazwisko: ")
    pesel = input("Podaj PESEL (11 cyfr): ")
    
    try:
        conn = sqlite3.connect("e_rejestracja_badan.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO patients (first_name, last_name, pesel) VALUES (?, ?, ?)", 
                       (first_name, last_name, pesel))
        conn.commit()
        print(" Sukces: Pacjent został dodany!")
    except sqlite3.IntegrityError:
        print(" Błąd: Pacjent z takim numerem PESEL już istnieje w bazie.")
    finally:
        conn.close()

def list_patients():
    conn = sqlite3.connect("e_rejestracja_badan.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM patients")
    patients = cursor.fetchall()
    conn.close()
    
    print("\n--- LISTA PACJENTÓW ---")
    if not patients:
        print("Brak pacjentów w bazie.")
    for p in patients:
        print(f"ID: {p[0]} | Imię i nazwisko: {p[1]} {p[2]} | PESEL: {p[3]}")

def list_exams():
    conn = sqlite3.connect("e_rejestracja_badan.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM exams")
    exams = cursor.fetchall()
    conn.close()
    
    print("\n--- DOSTĘPNE BADANIA ---")
    for e in exams:
        print(f"ID Badania: {e[0]} | Nazwa: {e[1]} | Cena: {e[2]} PLN")

def register_for_exam():
    list_patients()
    try:
        patient_id = int(input("\nPodaj ID pacjenta: "))
        
        list_exams()
        exam_id = int(input("Podaj ID badania, na które chcesz zapisać pacjenta: "))
        registration_date = input("Podaj datę i godzinę badania (np. 2026-06-20 12:00): ")
        
        conn = sqlite3.connect("e_rejestracja_badan.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO registrations (patient_id, exam_id, registration_date) VALUES (?, ?, ?)",
                       (patient_id, exam_id, registration_date))
        conn.commit()
        conn.close()
        print(" Sukces: Pacjent został zarejestrowany na badanie!")
    except ValueError:
        print(" Błąd: Nieprawidłowe dane numeryczne.")

def list_registrations():
    conn = sqlite3.connect("e_rejestracja_badan.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT r.id, p.first_name, p.last_name, e.exam_name, r.registration_date, r.status, e.price
        FROM registrations r
        JOIN patients p ON r.patient_id = p.id
        JOIN exams e ON r.exam_id = e.id
    """)
    regs = cursor.fetchall()
    conn.close()
    
    print("\n--- ZAREJESTROWANE BADANIA ---")
    if not regs:
        print("Brak zapisów na badania.")
    for r in regs:
        print(f"Zapis ID: {r[0]} | Pacjent: {r[1]} {r[2]} | Badanie: {r[3]} | Data: {r[4]} | Status: {r[5]} | Cena: {r[6]} PLN")

def main():
    init_db()
    while True:
        print("\n=== SYSTEM E-REJESTRACJI BADAŃ ===")
        print("1. Dodaj pacjenta")
        print("2. Wyświetl listę pacjentów")
        print("3. Przeglądaj dostępne badania")
        print("4. Zapisz pacjenta na badanie")
        print("5. Wyświetl rejestracje na badania")
        print("6. Wyjdź")
        
        choice = input("Wybierz opcję (1-6): ")
        
        if choice == "1":
            add_patient()
        elif choice == "2":
            list_patients()
        elif choice == "3":
            list_exams()
        elif choice == "4":
            register_for_exam()
        elif choice == "5":
            list_registrations()
        elif choice == "6":
            print("Do widzenia!")
            break
        else:
            print("Nieznana opcja, spróbuj ponownie.")

if __name__ == "__main__":
    main()
