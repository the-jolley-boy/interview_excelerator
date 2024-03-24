import sqlite3

class Database:
    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.cur = self.conn.cursor()

    def create_tables(self):
        # Create tables
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS interviews (
                id INTEGER PRIMARY KEY,
                company_name TEXT
            )
        """)

        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS settings (
                setting_name TEXT PRIMARY KEY,
                setting_value TEXT
            )
        """)

        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS questions (
                id INTEGER PRIMARY KEY,
                interview_id INTEGER,
                question_text TEXT,
                answer_text TEXT,
                FOREIGN KEY (interview_id) REFERENCES interviews (id)
            )
        """)

        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS voice_responses (
                id INTEGER PRIMARY KEY,
                interview_id INTEGER,
                question_text TEXT,
                response_text TEXT,
                FOREIGN KEY (interview_id) REFERENCES interviews (id)
            )
        """)
        
        # Insert default settings
        default_settings = [
            ('input_device_id', ''),
            ('openai_key', '')
        ]
        self.cur.executemany("INSERT OR IGNORE INTO settings (setting_name, setting_value) VALUES (?, ?)", default_settings)
        self.conn.commit()

    def close(self):
        self.conn.close()

    def insert_interview(self, company_name):
        self.cur.execute("INSERT INTO interviews (company_name) VALUES (?)", (company_name,))
        self.conn.commit()

    def insert_setting(self, setting_name, setting_value):
        self.cur.execute("INSERT OR REPLACE INTO settings (setting_name, setting_value) VALUES (?, ?)", (setting_name, setting_value))
        self.conn.commit()

    def insert_voice_response(self, interview_id, question_text, response_text):
        self.cur.execute("INSERT INTO voice_responses (interview_id, question_text, response_text) VALUES (?, ?, ?)", (interview_id, question_text, response_text))
        self.conn.commit()

    def get_past_responses_by_interview_id(self, interview_id):
        self.cur.execute("SELECT question_text, response_text FROM voice_responses WHERE interview_id = ?", (interview_id,))
        return self.cur.fetchall()
    
    def get_interviews(self):
        self.cur.execute("SELECT company_name FROM interviews")
        return [row[0] for row in self.cur.fetchall()]

    def get_questions_by_interview_id(self, interview_id):
        self.cur.execute("SELECT question_text, answer_text FROM questions WHERE interview_id = ?", (interview_id,))
        question_answers = self.cur.fetchall()
        return question_answers

    def get_interview_id(self, interview_name):
        self.cur.execute("SELECT id FROM interviews WHERE company_name = ?", (interview_name,))
        result = self.cur.fetchone()
        if result:
            return result[0]  # Assuming the ID is in the first column
        else:
            return None

    def add_question_and_answer(self, interview_id, question_text, answer_text):
        self.cur.execute("""
            INSERT INTO questions (interview_id, question_text, answer_text)
            VALUES (?, ?, ?)
        """, (interview_id, question_text, answer_text))
        self.conn.commit()

    def get_device_id(self):
        self.cur.execute("SELECT setting_value FROM settings WHERE setting_name = ?", ('input_device_id',))
        result = self.cur.fetchone()
        if result:
            return int(result[0])
        return None

    def get_interview_data(self):
        self.cur.execute("SELECT * FROM interviews")  # Adjust SQL as needed for your table structure
        return self.cur.fetchall()

    def get_questions_data(self):
        self.cur.execute("SELECT * FROM questions")  # Adjust SQL as needed for your table structure
        return self.cur.fetchall()

    def get_settings_data(self):
        self.cur.execute("SELECT * FROM settings")  # Adjust SQL as needed for your table structure
        return self.cur.fetchall()

    def get_voice_resp_data(self):
        self.cur.execute("SELECT * FROM voice_responses")  # Adjust SQL as needed for your table structure
        return self.cur.fetchall()

    def delete_question_and_answer(self, interview_id, question_text):
        # SQL DELETE statement to remove the specified question and answer
        delete_query = "DELETE FROM questions WHERE interview_id = ? AND question_text = ?"
        self.cur.execute(delete_query, (interview_id, question_text))
        self.conn.commit()

    def update_question_and_answer(self, interview_id, old_question_text, new_question_text, new_answer_text):
        # SQL UPDATE statement to modify the existing question and answer
        update_query = """
        UPDATE questions 
        SET question_text = ?, answer_text = ? 
        WHERE interview_id = ? AND question_text = ?
        """
        self.cur.execute(update_query, (new_question_text, new_answer_text, interview_id, old_question_text))
        self.conn.commit()

    def get_ai_key(self):
        self.cur.execute("SELECT setting_value FROM settings WHERE setting_name = ?", ('openai_key',))
        result = self.cur.fetchone()
        if result:
            return result[0]
        return None
