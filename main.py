import requests
import pandas as pd
from datetime import datetime
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from difflib import SequenceMatcher

# ---------------- Formations ----------------
FORMATIONS = {
    "1.كلية الهندسة": [152, 94, 172, 162, 397, 289, 314],
    "2.كلية العلوم": [155, 97, 175, 165, 406, 292, 317],
    "3.كلية الطب": [138, 88, 183, 182, 393, 184, 308],
    "4.كلية الهندسة الخوارزمي": [153, 95, 173, 163, 400, 290, 315],
    "5.كلية طب الكندي": [139, 89, 186, 185, 394, 187, 309],
    "6.طب الاسنان": [140, 90, 190, 188, 395, 191, 310],
    "7.كلية الصيدلة": [141, 91, 193, 192, 396, 194, 311],  # NEW
    "8.كلية الطب البيطري": [142, 92, 196, 195, 398, 197, 312],
    "9.كلية التمريض": [143, 93, 200, 198, 399, 199, 313],
  "10.كلية علوم الهندسة الزراعية": [154, 831, 174, 164, 403, 291, 316],   
  "11.كلية العلوم للبنات": [157, 99, 177, 167, 410, 294, 319],   
  "12.كلية التربية البدنية وعلوم الرياضة": [158, 100, 178, 168, 413, 295, 320],   
  "13.كلية التربية البدنية وعلوم الرياضة للبنات": [159, 101, 179, 169, 415, 296, 321],   
  "14.كلية الفنون الجميلة": [161, 103, 181, 171, 417, 298, 323],   
  "15.كلية التربية للعلوم الصرفة ( أبن الهيثم)": [160, 102, 180, 170, 416, 297, 322],   
  "16.كلية العلوم السياسية": [202, 105, 222, 212, 404, 300, 325],   
  "17.كلية القانون": [201, 104, 221, 211, 402, 299, 324],   
  "18.كلية الاداب": [204, 107, 441, 214, 407, 302, 327],   
  "19.كلية العلوم الاسلامية": [203, 106, 223, 213, 405, 301, 326],   
  "20.كلية التربية أبن رشد للعلوم الانسانية": [208, 112, 229, 218, 412, 306, 330],   
  "21.كلية التربية للبنات": [206, 111, 226, 216, 411, 304, 329],   
  "22.كلية الاعلام": [435, 434, 437, 436, 439, 438, 440],   
  "23.كلية اللغات": [209, 65, 230, 228, 414, 307, 331],   
  "24.مركز الحاسبة الالكترونية": [239, 82, 254, 267, 689, 281, 340],   
  "25.المركز الوطني الريادي لبحوث السرطان": [231, 74, 246, 245, 420, 273, 332],   
  "26.مركز البحوث التربوية والنفسية": [233, 76, 248, 261, 425, 287, 334],   
  "27.مركز الدراسات الاستراتيجية والدولية": [232, 75, 247, 260, 421, 274, 333],   
  "28.مركز احياء التراث العلمي العربي": [235, 78, 250, 263, 432, 277, 336],   
  "29.مركز بحوث ومتحف التاريخ الطبيعي": [234, 77, 249, 262, 427, 276, 335],   
  "30.مركز بحوث السوق وحماية المستهلك": [237, 80, 252, 265, 431, 279, 338],   
  "31.مركز دراسات المراة": [236, 79, 251, 264, 430, 278, 337],   
  "32.مركز أبن سينا للتعليم الالكتروني": [240, 83, 255, 268, 426, 282, 341],   
  "33.مركز التعليم المستمر": [238, 81, 253, 266, 428, 280, 339],   
  "34.معهد الليزر للدراسات العليا": [242, 117, 257, 270, 422, 284, 343],   
  "35.المعهد العالي للدراسات المحاسبية والمالية": [241, 116, 256, 269, 424, 283, 342],   
  "36.مركز التخطيط الحضري والاقليمي للدراسات العليا": [244, 119, 259, 272, 419, 286, 345],   
  "37.معهد الهندسة الوراثية للتقنيات الاحيائية": [243, 118, 258, 271, 421, 285, 344],   
  "38.المركز الوطني للدراسات السكانية والديموغرافية": [1005, 1007, 1008, 1014, 1011, 1012, 1013],   
  "39.كلية الادارة والاقتصاد": [156, 98, 176, 166, 408, 293, 318],   
  "40.كلية التميز": [1382, 1384, 1386, 1388, 1390, 1392, 1394],     
  "41.كلية الذكاء الاصطناعي": [1383, 1385, 1387, 1389, 1391, 1393, 1395],      
  "42.المكتبة المركزية": [375, 564], 


}

# --- Step 1: Convert category IDs to JSON export URLs ---
def build_export_urls(user_input):
    urls = []
    if user_input in FORMATIONS:
        for cat_id in FORMATIONS[user_input]:
            urls.append(f"https://events.uobaghdad.edu.iq/export/categ/{cat_id}.json?pretty=yes")
    elif "/category/" in user_input:
        cat_id = user_input.split("/category/")[1].strip("/").split("/")[0]
        urls.append(f"https://events.uobaghdad.edu.iq/export/categ/{cat_id}.json?pretty=yes")
    else:
        raise ValueError("Invalid input: must be a category URL or تشكيل name.")
    return urls

# --- Step 2: Fetch event IDs + titles from Indico ---
def fetch_records(export_url, year):
    response = requests.get(export_url)
    response.raise_for_status()
    events = response.json().get("results", [])
    records = []
    for ev in events:
        date_str = ev.get("startDate", {}).get("date", "")
        if isinstance(date_str, str) and date_str.startswith(str(year)):
            if ev.get("title"):
                records.append((ev.get("id"), ev.get("title").strip()))
    return records

# --- Step 3: Load titles from uploaded Excel file ---
def load_titles_from_excel(filepath, column_index=0):
    df = pd.read_excel(filepath, header=None)
    if column_index >= df.shape[1]:
        raise ValueError("Invalid column index selected.")
    titles = df.iloc[:, column_index].dropna().astype(str).str.strip().tolist()
    return titles, df.shape[1]

# --- Step 4: Compare titles with 80% similarity ---
def compare_titles(indico_records, excel_titles, threshold=0.8):
    matches = {}
    points = 0
    excel_titles_normalized = [t.strip().lower() for t in excel_titles]
    for ev_id, title in indico_records:
        title_norm = title.strip().lower()
        for excel_title in excel_titles_normalized:
            similarity = SequenceMatcher(None, title_norm, excel_title).ratio()
            if similarity >= threshold:
                matches[ev_id] = (title, round(similarity * 100, 1))
                points += 1
                break
    return matches, points

# --- Step 5: Save results ---
def save_results(indico_records, matches, points, year, formation_name, excel_titles_count):
    formation_titles_count = len(indico_records)
    completeness = round((points / formation_titles_count) * 100, 1) if formation_titles_count else 0
    relative_to_30 = round((completeness / 30) * 100, 1) if formation_titles_count else 0

    df = pd.DataFrame({
        "Event ID": [ev_id for ev_id, _ in indico_records],
        "Indico Titles": [title for _, title in indico_records],
        "Matched": [matches[ev_id][0] if ev_id in matches else "" for ev_id, _ in indico_records],
        "Similarity (%)": [matches[ev_id][1] if ev_id in matches else "" for ev_id, _ in indico_records]
    })

    summary = {
        "Event ID": "TOTALS",
        "Indico Titles": "",
        "Matched": f"{points} / {formation_titles_count} ({completeness}%)",
        "Similarity (%)": f"Relative to 30% baseline: {relative_to_30}% | Excel Titles Compared: {excel_titles_count} | Formation Titles Compared: {formation_titles_count}"
    }
    df = pd.concat([df, pd.DataFrame([summary])], ignore_index=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"title_comparison_{formation_name}_{year}_{timestamp}.xlsx"

    with pd.ExcelWriter(filename, engine="openpyxl") as writer:
        df.to_excel(writer, sheet_name="Comparison", index=False)
        # ❌ لم نعد نضيف السطر الأول الطويل

    return filename, completeness, relative_to_30, formation_titles_count

# ---------------- GUI ----------------
def run_analysis():
    formation_name = formation_combo.get().strip()
    year = year_entry.get().strip()
    filepath = file_entry.get().strip()
    column_index = column_entry.get().strip()

    if not formation_name or not year.isdigit() or not filepath or not column_index.isdigit():
        messagebox.showerror("Error", "Please select a تشكيل, year, Excel file, and column index.")
        return

    try:
        export_urls = build_export_urls(formation_name)
        indico_records = []
        for url in export_urls:
            indico_records.extend(fetch_records(url, int(year)))

        excel_titles, total_cols = load_titles_from_excel(filepath, int(column_index))
        matches, points = compare_titles(indico_records, excel_titles, threshold=0.8)
        filename, completeness, relative_to_30, formation_titles_count = save_results(
            indico_records, matches, points, year, formation_name, len(excel_titles)
        )

        messagebox.showinfo("Success",
            f"Excel file created:\n{filename}\n\n"
            f"Total matches: {points} / {formation_titles_count}\n"
            f"Completeness: {completeness}%\n"
            f"Relative to 30% baseline: {relative_to_30}%\n"
            f"Excel Titles Compared: {len(excel_titles)}\n"
            f"Formation Titles Compared: {formation_titles_count}\n"
            f"(Your file has {total_cols} columns, you used column {column_index})")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def browse_file():
    filepath = filedialog.askopenfilename(
        title="Select Excel File",
        filetypes=[("Excel files", "*.xlsx *.xls")]
    )
    if filepath:
        file_entry.delete(0, tk.END)
        file_entry.insert(0, filepath)

root = tk.Tk()
root.title("Event Title Comparison (80% Match) v4.2 مقارنة الخطة ")

tk.Label(root, text="اختر التشكيل:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
formation_combo = ttk.Combobox(root, values=list(FORMATIONS.keys()), state="readonly", width=40)
formation_combo.grid(row=0, column=1, padx=5, pady=5)
formation_combo.current(0)

tk.Label(root, text="ادخل عام تقييم النشاطات: مثلا 2026").grid(row=1, column=0, padx=5, pady=5, sticky="e")
year_entry = tk.Entry(root, width=10)
year_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")

tk.Label(root, text="Upload the Excel حمل ملف الاكسل:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
file_entry = tk.Entry(root, width=50)
file_entry.grid(row=2, column=1, padx=5, pady=5, sticky="w")
tk.Button(root, text="Browse", command=browse_file).grid(row=2, column=2, padx=5, pady=5)

tk.Label(root, text="Column Index (0 = first column): الرقم الافتراضي =  2").grid(row=3, column=0, padx=5, pady=5, sticky="e")
column_entry = tk.Entry(root, width=10)
column_entry.grid(row=3, column=1, padx=5, pady=5, sticky="w")

tk.Button(root, text="Compare Titles قارن", command=run_analysis).grid(row=4, column=0, columnspan=3, pady=10)
tk.Label(root, text="كلما زاد عدد النشاطات زاد الوقت لاظهار النتائج الرجاء الانتظار ").grid(row=5, column=2, padx=5, pady=5, sticky="e")

root.mainloop()
