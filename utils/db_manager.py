import sqlite3
import hashlib
import os

current_dir=os.path.dirname(os.path.abspath(__file__))
project_root=os.path.dirname(current_dir)
DB_PATH=os.path.join(project_root,"eduai_valut.db")
def connection():
    conn=sqlite3.connect(DB_PATH)
    conn.row_factory=sqlite3.Row
    return conn
def save_documnet_to_db(filename,raw_text):
    conn=connection()
    cursor=conn.cursor()
    try:
        cursor.execute("SELECT id FROM documents WHERE filename=?",(filename,))
        exists=cursor.fetchone()
        if not exists:
            cursor.execute("INSERT INTO documents (filename, processed_text)VALUES (?,?)",(filename,raw_text))
            conn.commit()
            print(f"Document '{filename}' saved to database.")
        else:
            print(f"Document '{filename}' already exists in the database.")
        conn.close()
    except Exception as e:
        print(f"Error saving document to database: {e}")
    finally:
        conn.close()
def get_all_document():
    conn=connection()
    cursor=conn.cursor()
    cursor.execute("SELECT id,filename,Upload_date,processed_text FROM documents ORDER BY upload_date DESC")
    rows=cursor.fetchall()
    conn.close()
    return rows
def generate_text_hash(text):
    return hashlib.sha256(text.encode('utf-8')).hexdigest()
def check_cache(text_hash,request_type):
        conn=connection()
        cursor=conn.cursor()
        cursor.execute("SELECT cached_response FROM response_cache WHERE text_hash=? AND request_type=?",(text_hash,request_type))
        result=cursor.fetchone()
        conn.close()
        if result:
            return result['cached_response']
        else:
            return None
def save_to_cache(text_hash,request_type,cached_response):
        conn=connection()
        cursor=conn.cursor()
        try:
            cursor.execute("INSERT OR REPLACE INTO response_cache (text_hash, request_type, cached_response) VALUES (?,?,?)",(text_hash,request_type,cached_response))
            conn.commit()
            print("response cached cleanly.")
        except Exception as e:
            print(f"Error saving to cache: {e}")    
        finally:
             conn.close()
def get_user_data():
     documents=get_all_document()
     library_items=[]
     conn=connection()
     cursor=conn.cursor()
     for i in documents:
        text_hash=generate_text_hash(i['processed_text'])
        cursor.execute("SELECT cached_response FROM response_cache WHERE text_hash=? AND request_type='summary'",(text_hash,))
        cache_row=cursor.fetchone()
        if cache_row:
            summary=cache_row['cached_response']
        else:
            print("summary not generated yet")
        library_items.append({
            "id": i['id'],
            "filename": i['filename'],
            "upload_date": i['Upload_date'],
            "summary":summary})
     conn.close()
     return library_items


                   


