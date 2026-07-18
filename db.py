import sqlite3
import os
import logging
from kivy.app import App

db_path = None
_db_initialized = False

def get_db_path():
    global db_path
    if not db_path:
        app = App.get_running_app()
        if app:
            db_path = os.path.join(app.user_data_dir, 'music_stats.db')
        else:
            # Fallback for service.py or before app starts
            # Try to get the package directory via jnius if on android
            try:
                from jnius import autoclass
                PythonActivity = autoclass('org.kivy.android.PythonActivity')
                # If running in service, PythonActivity might not have mActivity, we can use PythonService
                try:
                    context = PythonActivity.mActivity.getApplicationContext()
                except:
                    PythonService = autoclass('org.kivy.android.PythonService')
                    context = PythonService.mService.getApplicationContext()
                db_path = os.path.join(context.getFilesDir().getAbsolutePath(), 'music_stats.db')
            except Exception:
                db_path = 'music_stats.db'
    return db_path

def ensure_db():
    global _db_initialized
    if not _db_initialized:
        conn = sqlite3.connect(get_db_path())
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS song_stats (
                song_name TEXT PRIMARY KEY,
                play_count INTEGER DEFAULT 0
            )
        ''')
        conn.commit()
        conn.close()
        _db_initialized = True

def increment_play_count(song_name):
    try:
        ensure_db()
        conn = sqlite3.connect(get_db_path())
        cursor = conn.cursor()
        cursor.execute('SELECT play_count FROM song_stats WHERE song_name = ?', (song_name,))
        row = cursor.fetchone()
        if row:
            count = row[0] + 1
            cursor.execute('UPDATE song_stats SET play_count = ? WHERE song_name = ?', (count, song_name))
        else:
            count = 1
            cursor.execute('INSERT INTO song_stats (song_name, play_count) VALUES (?, ?)', (song_name, count))
        conn.commit()
        conn.close()
        return count
    except Exception as e:
        logging.error(f"DB Error: {e}")
        return 0

def get_top_songs(limit=25):
    try:
        ensure_db()
        conn = sqlite3.connect(get_db_path())
        cursor = conn.cursor()
        cursor.execute('SELECT song_name FROM song_stats ORDER BY play_count DESC LIMIT ?', (limit,))
        songs = [row[0] for row in cursor.fetchall()]
        conn.close()
        return songs
    except Exception as e:
        logging.error(f"DB Error getting top songs: {e}")
        return []
