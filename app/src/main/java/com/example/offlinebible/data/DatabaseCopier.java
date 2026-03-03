package com.example.offlinebible.data;

import android.content.Context;
import android.database.sqlite.SQLiteDatabase;
import android.database.sqlite.SQLiteOpenHelper;

import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;

/**
 * Copies the pre-built bible.db from the assets folder into application internal storage
 * on first launch. Subsequent launches just open the existing copy.
 */
public class DatabaseCopier extends SQLiteOpenHelper {

    private static final String DB_NAME = "bible.db";
    private static final int DB_VERSION = 1;
    private final Context context;
    private boolean needsCopy = false;

    public DatabaseCopier(Context context) {
        super(context, DB_NAME, null, DB_VERSION);
        this.context = context;
    }

    /**
     * Call this once during Application or Activity startup.
     * Copies the database from assets if it doesn't already exist.
     */
    public void createDatabaseIfNotExists() {
        File dbFile = context.getDatabasePath(DB_NAME);
        if (!dbFile.exists()) {
            // Ensure the databases directory exists
            dbFile.getParentFile().mkdirs();
            // Call getReadableDatabase() to trigger creation of an empty DB
            this.getReadableDatabase();
            this.close();
            // Now overwrite it with our pre-built copy
            copyDatabaseFromAssets();
        }
    }

    private void copyDatabaseFromAssets() {
        try {
            InputStream input = context.getAssets().open(DB_NAME);
            String outFileName = context.getDatabasePath(DB_NAME).getAbsolutePath();
            OutputStream output = new FileOutputStream(outFileName);

            byte[] buffer = new byte[4096];
            int length;
            while ((length = input.read(buffer)) > 0) {
                output.write(buffer, 0, length);
            }

            output.flush();
            output.close();
            input.close();
        } catch (IOException e) {
            throw new RuntimeException("Error copying database from assets", e);
        }
    }

    @Override
    public void onCreate(SQLiteDatabase db) {
        // Not used – DB is pre-built from assets
    }

    @Override
    public void onUpgrade(SQLiteDatabase db, int oldVersion, int newVersion) {
        // If you ship a new bible.db, delete the old one and re-copy
        context.deleteDatabase(DB_NAME);
        copyDatabaseFromAssets();
    }
}
