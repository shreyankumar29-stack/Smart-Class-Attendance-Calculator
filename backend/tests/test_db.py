from db import get_db_connection

conn = get_db_connection()

cur = conn.cursor()

cur.execute("""
INSERT INTO subjects
(subject_name, subject_code, target_percentage)
VALUES
(%s,%s,%s)
""",
("Data Structures", "CSR123", 75))

conn.commit()

print("✅ Subject Added Successfully")

cur.close()
conn.close()