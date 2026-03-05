package com.example.offlinebible.data;

import android.content.ContentValues;
import android.content.Context;
import android.database.Cursor;
import android.database.sqlite.SQLiteDatabase;
import android.database.sqlite.SQLiteOpenHelper;
import com.example.offlinebible.models.BibleVerse;

import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

/**
 * All read/write operations against the bible.db.
 * The database is pre-populated and copied from assets by DatabaseCopier.
 */
public class DatabaseHelper extends SQLiteOpenHelper {

    private static final String DATABASE_NAME = "bible.db";
    private static final int DATABASE_VERSION = 2;

    public DatabaseHelper(Context context) {
        super(context, DATABASE_NAME, null, DATABASE_VERSION);
    }

    @Override
    public void onCreate(SQLiteDatabase db) {
        // DB is pre-built. This is a no-op.
    }

    @Override
    public void onUpgrade(SQLiteDatabase db, int oldVersion, int newVersion) {
        if (oldVersion < 2) {
            safeAddColumn(db, "verses", "highlight_color", "TEXT");
        }
    }

    @Override
    public void onOpen(SQLiteDatabase db) {
        super.onOpen(db);
        // Secondary safety check to ensure columns exist even if upgrade didn't trigger
        // correctly
        safeAddColumn(db, "verses", "highlight_color", "TEXT");
    }

    private void safeAddColumn(SQLiteDatabase db, String table, String column, String type) {
        try {
            db.execSQL("ALTER TABLE " + table + " ADD COLUMN " + column + " " + type);
        } catch (Exception e) {
            // Success or already exists
        }
    }

    // ========== VERSION QUERIES ==========

    /**
     * Returns version IDs from the versions table, ordered by language then name.
     */
    public List<String> getAvailableVersions() {
        List<String> versions = new ArrayList<>();
        SQLiteDatabase db = this.getReadableDatabase();
        Cursor cursor = db.rawQuery(
                "SELECT version_id FROM versions ORDER BY is_english DESC, language, version_id", null);
        if (cursor.moveToFirst()) {
            do {
                versions.add(cursor.getString(0));
            } while (cursor.moveToNext());
        }
        cursor.close();
        return versions;
    }

    /** Returns the display name for a version, e.g. "King James Version" */
    public String getVersionDisplayName(String versionId) {
        SQLiteDatabase db = this.getReadableDatabase();
        Cursor cursor = db.rawQuery(
                "SELECT display_name FROM versions WHERE version_id=?",
                new String[] { versionId });
        String name = versionId;
        if (cursor.moveToFirst()) {
            name = cursor.getString(0);
        }
        cursor.close();
        return name;
    }

    /** Returns true if a version is flagged as English in the versions table. */
    public boolean isEnglishVersion(String versionId) {
        SQLiteDatabase db = this.getReadableDatabase();
        Cursor cursor = db.rawQuery(
                "SELECT is_english FROM versions WHERE version_id=?",
                new String[] { versionId });
        boolean english = false;
        if (cursor.moveToFirst()) {
            english = cursor.getInt(0) == 1;
        }
        cursor.close();
        return english;
    }

    /** Returns the language name for a version, e.g. "Hausa" */
    public String getVersionLanguage(String versionId) {
        SQLiteDatabase db = this.getReadableDatabase();
        Cursor cursor = db.rawQuery(
                "SELECT language FROM versions WHERE version_id=?",
                new String[] { versionId });
        String lang = "English";
        if (cursor.moveToFirst()) {
            lang = cursor.getString(0);
        }
        cursor.close();
        return lang;
    }

    // ========== BOOK QUERIES ==========

    /** Returns an ordered list of unique book names for a given version. */
    public List<String> getBooks(String versionId) {
        List<String> books = new ArrayList<>();
        SQLiteDatabase db = this.getReadableDatabase();
        Cursor cursor = db.rawQuery(
                "SELECT DISTINCT book_name FROM verses WHERE version_id=? ORDER BY book_number",
                new String[] { versionId });
        if (cursor.moveToFirst()) {
            do {
                books.add(cursor.getString(0));
            } while (cursor.moveToNext());
        }
        cursor.close();
        return books;
    }

    /** Returns a map of book_name -> book_number for a given version. */
    public Map<String, Integer> getBookMap(String versionId) {
        Map<String, Integer> map = new LinkedHashMap<>();
        SQLiteDatabase db = this.getReadableDatabase();
        Cursor cursor = db.rawQuery(
                "SELECT DISTINCT book_name, book_number FROM verses WHERE version_id=? ORDER BY book_number",
                new String[] { versionId });
        if (cursor.moveToFirst()) {
            do {
                map.put(cursor.getString(0), cursor.getInt(1));
            } while (cursor.moveToNext());
        }
        cursor.close();
        return map;
    }

    // ========== CHAPTER QUERIES ==========

    /** Returns the number of chapters for a given book in a given version. */
    public int getChapterCount(String versionId, String bookName) {
        SQLiteDatabase db = this.getReadableDatabase();
        Cursor cursor = db.rawQuery(
                "SELECT MAX(chapter) FROM verses WHERE version_id=? AND book_name=?",
                new String[] { versionId, bookName });
        int count = 0;
        if (cursor.moveToFirst()) {
            count = cursor.getInt(0);
        }
        cursor.close();
        return count;
    }

    // ========== VERSE QUERIES ==========

    /** Fetch all verses for a specific chapter. */
    public List<BibleVerse> getChapter(String versionId, String bookName, int chapter) {
        List<BibleVerse> list = new ArrayList<>();
        SQLiteDatabase db = this.getReadableDatabase();

        Cursor cursor = db.rawQuery(
                "SELECT * FROM verses WHERE version_id=? AND book_name=? AND chapter=? ORDER BY verse",
                new String[] { versionId, bookName, String.valueOf(chapter) });

        if (cursor.moveToFirst()) {
            do {
                list.add(cursorToVerse(cursor));
            } while (cursor.moveToNext());
        }
        cursor.close();
        return list;
    }

    // ========== SEARCH ==========

    /** Full-text search across an entire version. Returns matching verses. */
    public List<BibleVerse> searchVerses(String versionId, String query) {
        List<BibleVerse> list = new ArrayList<>();
        SQLiteDatabase db = this.getReadableDatabase();

        Cursor cursor = db.rawQuery(
                "SELECT * FROM verses WHERE version_id=? AND text LIKE ? LIMIT 200",
                new String[] { versionId, "%" + query + "%" });
        if (cursor.moveToFirst()) {
            do {
                list.add(cursorToVerse(cursor));
            } while (cursor.moveToNext());
        }
        cursor.close();
        return list;
    }

    // ========== BOOKMARK / HIGHLIGHT ==========

    public void updateBookmark(int id, boolean isBookmarked) {
        SQLiteDatabase db = this.getWritableDatabase();
        ContentValues cv = new ContentValues();
        cv.put("is_bookmarked", isBookmarked ? 1 : 0);
        db.update("verses", cv, "id=?", new String[] { String.valueOf(id) });
    }

    public void updateHighlight(int id, boolean isHighlighted, String color) {
        SQLiteDatabase db = this.getWritableDatabase();
        ContentValues cv = new ContentValues();
        cv.put("is_highlighted", isHighlighted ? 1 : 0);
        cv.put("highlight_color", color); // Can be null
        db.update("verses", cv, "id=?", new String[] { String.valueOf(id) });
    }

    /** Fetch all bookmarked verses for a given version. */
    public List<BibleVerse> getBookmarkedVerses(String versionId) {
        List<BibleVerse> list = new ArrayList<>();
        SQLiteDatabase db = this.getReadableDatabase();
        Cursor cursor = db.rawQuery(
                "SELECT * FROM verses WHERE version_id=? AND is_bookmarked=1 ORDER BY id",
                new String[] { versionId });
        if (cursor.moveToFirst()) {
            do {
                list.add(cursorToVerse(cursor));
            } while (cursor.moveToNext());
        }
        cursor.close();
        return list;
    }

    /** Fetch all highlighted verses (Favorites) for a given version. */
    public List<BibleVerse> getHighlightedVerses(String versionId) {
        List<BibleVerse> list = new ArrayList<>();
        SQLiteDatabase db = this.getReadableDatabase();
        Cursor cursor = db.rawQuery(
                "SELECT * FROM verses WHERE version_id=? AND is_highlighted=1 ORDER BY id",
                new String[] { versionId });
        if (cursor.moveToFirst()) {
            do {
                list.add(cursorToVerse(cursor));
            } while (cursor.moveToNext());
        }
        cursor.close();
        return list;
    }

    /** Get a random verse for the carousel. */
    public BibleVerse getRandomVerse(String versionId) {
        SQLiteDatabase db = this.getReadableDatabase();
        Cursor cursor = db.rawQuery(
                "SELECT * FROM verses WHERE version_id=? ORDER BY RANDOM() LIMIT 1",
                new String[] { versionId });
        BibleVerse verse = null;
        if (cursor.moveToFirst()) {
            verse = cursorToVerse(cursor);
        }
        cursor.close();
        return verse;
    }

    // ========== HELPER ==========

    private BibleVerse cursorToVerse(Cursor cursor) {
        int idIdx = cursor.getColumnIndex("id");
        int vIdx = cursor.getColumnIndex("version_id");
        int bnIdx = cursor.getColumnIndex("book_number");
        int bNmIdx = cursor.getColumnIndex("book_name");
        int cIdx = cursor.getColumnIndex("chapter");
        int vsIdx = cursor.getColumnIndex("verse");
        int tIdx = cursor.getColumnIndex("text");
        int bMkIdx = cursor.getColumnIndex("is_bookmarked");
        int hIdx = cursor.getColumnIndex("is_highlighted");
        int hCIdx = cursor.getColumnIndex("highlight_color");

        return new BibleVerse(
                idIdx != -1 ? cursor.getInt(idIdx) : 0,
                vIdx != -1 ? cursor.getString(vIdx) : "",
                bnIdx != -1 ? cursor.getInt(bnIdx) : 0,
                bNmIdx != -1 ? cursor.getString(bNmIdx) : "",
                cIdx != -1 ? cursor.getInt(cIdx) : 1,
                vsIdx != -1 ? cursor.getInt(vsIdx) : 1,
                tIdx != -1 ? cursor.getString(tIdx) : "",
                bMkIdx != -1 && cursor.getInt(bMkIdx) == 1,
                hIdx != -1 && cursor.getInt(hIdx) == 1,
                hCIdx != -1 ? cursor.getString(hCIdx) : null);
    }

    // ========== HYMNS QUERIES ==========

    /** Returns all hymns ordered by their hymn number. */
    public List<com.example.offlinebible.models.Hymn> getAllHymns() {
        List<com.example.offlinebible.models.Hymn> result = new ArrayList<>();
        SQLiteDatabase db = this.getReadableDatabase();
        Cursor cursor = db.rawQuery("SELECT hymn_id, hymn_number, title FROM hymns ORDER BY hymn_number", null);
        if (cursor.moveToFirst()) {
            do {
                result.add(new com.example.offlinebible.models.Hymn(
                        cursor.getInt(0),
                        cursor.getInt(1),
                        cursor.getString(2)));
            } while (cursor.moveToNext());
        }
        cursor.close();
        return result;
    }

    /** Returns stanzas for a specific hymn ID. */
    public List<String> getStanzas(int hymnId) {
        List<String> result = new ArrayList<>();
        SQLiteDatabase db = this.getReadableDatabase();
        Cursor cursor = db.rawQuery(
                "SELECT stanza_text FROM hymn_stanzas WHERE hymn_id=? ORDER BY stanza_number",
                new String[] { String.valueOf(hymnId) });
        if (cursor.moveToFirst()) {
            do {
                result.add(cursor.getString(0));
            } while (cursor.moveToNext());
        }
        cursor.close();
        return result;
    }

    /** Searches hymns by title or number. */
    public List<com.example.offlinebible.models.Hymn> searchHymns(String query) {
        List<com.example.offlinebible.models.Hymn> result = new ArrayList<>();
        SQLiteDatabase db = this.getReadableDatabase();
        String sql = "SELECT hymn_id, hymn_number, title FROM hymns WHERE title LIKE ? OR hymn_number LIKE ? ORDER BY hymn_number";
        String wild = "%" + query + "%";
        Cursor cursor = db.rawQuery(sql, new String[] { wild, wild });
        if (cursor.moveToFirst()) {
            do {
                result.add(new com.example.offlinebible.models.Hymn(
                        cursor.getInt(0),
                        cursor.getInt(1),
                        cursor.getString(2)));
            } while (cursor.moveToNext());
        }
        cursor.close();
        return result;
    }
}
