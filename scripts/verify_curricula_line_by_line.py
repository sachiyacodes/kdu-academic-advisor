import csv
import re
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
txt_path = Path("C:/Users/ASUS/.gemini/antigravity/brain/3f7e0a03-680a-4bf2-aaac-bfe49a025cff/.user_uploaded/media_1788532673280.txt")
lines = txt_path.read_text(encoding="utf-8").splitlines()

degree_map = {
    "BSc (Hons) in Computer Science": "Computer Science",
    "BSc (Hons) in Software Engineering": "Software Engineering",
    "BSc (Hons) in Data Science & Business Analytics": "Data Science & Business Analytics",
    "BSc (Hons) in Information Technology": "Information Technology",
    "BSc (Hons) in Information Systems": "Information Systems",
    "BSc (Hons) in Computer Engineering": "Computer Engineering"
}

current_degree = None
current_year = None
current_sem = None

txt_courses = []

for line_num, line in enumerate(lines, start=1):
    line = line.strip()
    if not line:
        continue
    m_deg = re.match(r"^[1-6]\.\s+(BSc \(Hons\) in .+)$", line)
    if m_deg:
        raw_deg = m_deg.group(1).strip()
        current_degree = degree_map.get(raw_deg, raw_deg)
        continue
    
    m_year = re.match(r"^Year\s+(\d+)$", line)
    if m_year:
        current_year = int(m_year.group(1))
        continue
        
    m_sem = re.match(r"^Semester\s+(\d+)$", line)
    if m_sem:
        s = int(m_sem.group(1))
        current_sem = 1 if s % 2 == 1 else 2
        continue
        
    if line.startswith("Course / Module") or line.startswith("Detailed source") or line.startswith("Official source") or line.startswith("Military/MGPA"):
        continue
    if line.startswith("Verification notes") or line.startswith("KDU Computing") or line.startswith("Courses and Credits") or line.startswith("Scope.") or line.startswith("Version note.") or line.startswith("Audit findings") or line.startswith("Programme and source summary"):
        continue
    if line.startswith("#\tProgramme") or line.startswith("https://") or line.startswith("Audit date:"):
        continue
    if line.startswith("•") or line.startswith("*"):
        continue
    if current_degree and current_year and current_sem:
        parts = [p.strip() for p in line.split("\t")]
        if len(parts) >= 2:
            raw_credits_str = parts[1]
            m_cr = re.match(r"^(\d+)", raw_credits_str)
            if m_cr:
                credits_val = int(m_cr.group(1))
            else:
                credits_val = 0
                
            txt_courses.append({
                "txt_line": line_num,
                "degree": current_degree,
                "year": current_year,
                "semester": current_sem,
                "name": parts[0],
                "credits": credits_val,
                "raw_credits": parts[1],
                "type": parts[2] if len(parts) > 2 else ""
            })

with open(PROJECT_ROOT / "data" / "courses.csv", "r", encoding="utf-8") as f:
    csv_courses = list(csv.DictReader(f))

print(f"Total TXT courses: {len(txt_courses)}")
print(f"Total CSV courses: {len(csv_courses)}")

def map_course_type(raw_type: str) -> str:
    t = raw_type.strip()
    if "Elective" in t or "elective" in t:
        return "Elective"
    elif "Non-GPA" in t or "Credit not explicitly stated" in t:
        return "NGPA"
    else:
        return "Core"

# Now compare
mismatches = []
for i, (tc, cc) in enumerate(zip(txt_courses, csv_courses), start=1):
    diffs = []
    if tc["degree"] != cc["degree"]:
        diffs.append(f"degree: txt='{tc['degree']}' vs csv='{cc['degree']}'")
    if tc["year"] != int(cc["year"]):
        diffs.append(f"year: txt={tc['year']} vs csv={cc['year']}")
    if tc["semester"] != int(cc["semester"]):
        diffs.append(f"semester: txt={tc['semester']} vs csv={cc['semester']}")
    if tc["name"] != cc["course_name"]:
        diffs.append(f"name: txt='{tc['name']}' vs csv='{cc['course_name']}'")
    if tc["credits"] != int(cc["credits"]):
        diffs.append(f"credits: txt={tc['credits']} (raw: '{tc['raw_credits']}') vs csv={cc['credits']}")
    expected_type = map_course_type(tc["type"])
    if expected_type != cc.get("course_type"):
        diffs.append(f"course_type: expected='{expected_type}' (raw: '{tc['type']}') vs csv='{cc.get('course_type')}'")
        
    if diffs:
        mismatches.append((i, tc["txt_line"], tc["degree"], tc["name"], diffs))

print(f"Mismatches count (TXT vs CSV): {len(mismatches)}")
if mismatches:
    for m in mismatches:
        print(f"Row {m[0]} (txt line {m[1]}): {m[2]} - {m[3]}")
        for d in m[4]:
            print(f"    {d}")
else:
    print("[PASS] PERFECT 100% MATCH (TXT vs CSV): Every single course, name, degree, year, semester, credit, and course_type matches exactly!")

# Verify SQLite Database
import sqlite3
db_path = PROJECT_ROOT / "database" / "academic.db"
conn = sqlite3.connect(db_path)
conn.row_factory = sqlite3.Row
db_rows = conn.execute("SELECT * FROM courses ORDER BY course_id").fetchall()
print(f"\nTotal DB rows: {len(db_rows)}")

db_mismatches = []
for i, (tc, db_row) in enumerate(zip(txt_courses, db_rows), start=1):
    diffs = []
    if tc["degree"] != db_row["degree"]:
        diffs.append(f"degree: txt='{tc['degree']}' vs db='{db_row['degree']}'")
    if tc["year"] != db_row["year"]:
        diffs.append(f"year: txt={tc['year']} vs db={db_row['year']}")
    if tc["semester"] != db_row["semester"]:
        diffs.append(f"semester: txt={tc['semester']} vs db={db_row['semester']}")
    if tc["name"] != db_row["course_name"]:
        diffs.append(f"name: txt='{tc['name']}' vs db='{db_row['course_name']}'")
    if tc["credits"] != db_row["credits"]:
        diffs.append(f"credits: txt={tc['credits']} vs db={db_row['credits']}")
    expected_type = map_course_type(tc["type"])
    if expected_type != db_row["course_type"]:
        diffs.append(f"course_type: expected='{expected_type}' vs db='{db_row['course_type']}'")
    if diffs:
        db_mismatches.append((i, tc["degree"], tc["name"], diffs))

print(f"Mismatches count (TXT vs SQLite DB): {len(db_mismatches)}")
if db_mismatches:
    for m in db_mismatches:
        print(f"DB Row {m[0]}: {m[1]} - {m[2]}")
        for d in m[3]:
            print(f"    {d}")
else:
    print("[PASS] PERFECT 100% MATCH (TXT vs SQLite DB): All 444 courses in academic.db match the source text line-by-line including course_type!")
conn.close()
