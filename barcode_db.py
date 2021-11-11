import sqlite3

con = sqlite3.connect('barcodes.db')
barcodes = con.cursor()
barcodes.execute('''
    CREATE TABLE IF NOT EXISTS vid_details (
        vid_id VARCHAR(11),
        title TINYTEXT,
        width SMALLINT,
        height SMALLINT,
        filename VARCHAR
    )
''')
con.close()

def get_random_barcode():
    con = sqlite3.connect('barcodes.db')
    barcodes = con.cursor()
    file = barcodes.execute('''
        SELECT filename FROM vid_details
        ORDER BY RANDOM()
        LIMIT 1
    ''')
    name = file.fetchall()[0][0]
    con.close()
    return name

def add_new_barcode(video_id, title, width, height, filename):
    print("Inserting barcode:", video_id)
    con = sqlite3.connect('barcodes.db')
    barcodes = con.cursor()
    barcodes.execute('''
        INSERT INTO vid_details (vid_id, title, width, height, filename)
        VALUES (?, ?, ?, ?, ?)
    ''', (video_id, title, width, height, filename))
    con.commit()
    con.close()

def contains_video(video_id, total_samples):
    con = sqlite3.connect('barcodes.db')
    barcodes = con.cursor()
    exists = barcodes.execute('''
        SELECT * FROM vid_details
        WHERE vid_id =:id AND width=:samples
    ''', {'id': video_id, 'samples': total_samples} ).fetchall()
    return exists
