package com.example.offlinebible.data;

import android.content.Context;
import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;

/**
 * Copies the pre-built bible.db from the assets folder into application
 * internal storage.
 */
public class DatabaseCopier {

    private static final String DB_NAME = "bible.db";
    private final Context context;

    public DatabaseCopier(Context context) {
        this.context = context;
    }

    public void createDatabaseIfNotExists() {
        File dbFile = context.getDatabasePath(DB_NAME);
        if (!dbFile.exists()) {
            dbFile.getParentFile().mkdirs();
            copyDatabaseFromAssets();
        }
    }

    private void copyDatabaseFromAssets() {
        try (InputStream input = context.getAssets().open(DB_NAME);
                OutputStream output = new FileOutputStream(context.getDatabasePath(DB_NAME))) {

            byte[] buffer = new byte[4096];
            int length;
            while ((length = input.read(buffer)) > 0) {
                output.write(buffer, 0, length);
            }
            output.flush();
        } catch (IOException e) {
            throw new RuntimeException("Error copying database from assets", e);
        }
    }
}
