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
    private static final int DATABASE_VERSION = 1;

    public DatabaseHelper(Context context) {
        super(context, DATABASE_NAME, null, DATABASE_VERSION);
    }

    @Override
    public void onCreate(SQLiteDatabase db) {
        // DB is pre-built. This is a no-op.
    }

    @Override
    public void onUpgrade(SQLiteDatabase db, int oldVersion, int newVersion) {
        // Handle future schema migrations here.
    }

    // ========== VERSION QUERIES ==========

    /** Returns version IDs from the versions table, ordered by language then name. */
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
            new String[]{versionId});
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
            new String[]{versionId});
        boolean english = false;
        if (cursor.moveToFirst()) {
            english = cursor.getInt(0) == 1;
        }
        cursor.close();
        return english;
    }

    // ========== BOOK QUERIES ==========

    /** Returns an ordered list of unique book names for a given version. */
    public List<String> getBooks(String versionId) {
        List<String> books = new ArrayList<>();
        SQLiteDatabase db = this.getReadableDatabase();
        Cursor cursor = db.rawQuery(
            "SELECT DISTINCT book_name FROM verses WHERE version_id=? ORDER BY book_number",
            new String[]{versionId}
        );
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
            new String[]{versionId}
        );
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
            new String[]{versionId, bookName}
        );
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
            new String[]{versionId, bookName, String.valueOf(chapter)}
        );

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
            new String[]{versionId, "%" + query + "%"}
        );
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
        db.update("verses", cv, "id=?", new String[]{String.valueOf(id)});
    }

    public void updateHighlight(int id, boolean isHighlighted) {
        SQLiteDatabase db = this.getWritableDatabase();
        ContentValues cv = new ContentValues();
        cv.put("is_highlighted", isHighlighted ? 1 : 0);
        db.update("verses", cv, "id=?", new String[]{String.valueOf(id)});
    }

    /** Fetch all bookmarked verses for a given version. */
    public List<BibleVerse> getBookmarkedVerses(String versionId) {
        List<BibleVerse> list = new ArrayList<>();
        SQLiteDatabase db = this.getReadableDatabase();
        Cursor cursor = db.rawQuery(
            "SELECT * FROM verses WHERE version_id=? AND is_bookmarked=1 ORDER BY book_number, chapter, verse",
            new String[]{versionId}
        );
        if (cursor.moveToFirst()) {
            do {
                list.add(cursorToVerse(cursor));
            } while (cursor.moveToNext());
        }
        cursor.close();
        return list;
    }

    // ========== HELPER ==========

    private BibleVerse cursorToVerse(Cursor cursor) {
        return new BibleVerse(
            cursor.getInt(cursor.getColumnIndexOrThrow("id")),
            cursor.getString(cursor.getColumnIndexOrThrow("version_id")),
            cursor.getInt(cursor.getColumnIndexOrThrow("book_number")),
            cursor.getString(cursor.getColumnIndexOrThrow("book_name")),
            cursor.getInt(cursor.getColumnIndexOrThrow("chapter")),
            cursor.getInt(cursor.getColumnIndexOrThrow("verse")),
            cursor.getString(cursor.getColumnIndexOrThrow("text")),
            cursor.getInt(cursor.getColumnIndexOrThrow("is_bookmarked")) == 1,
            cursor.getInt(cursor.getColumnIndexOrThrow("is_highlighted")) == 1
        );
    }
}
