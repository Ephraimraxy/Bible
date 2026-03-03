package com.example.offlinebible.ui;

import android.app.AlertDialog;
import android.os.Bundle;
import android.speech.tts.TextToSpeech;
import android.text.Editable;
import android.text.TextWatcher;
import android.view.View;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.EditText;
import android.widget.ImageButton;
import android.widget.Spinner;
import android.widget.TextView;
import android.widget.Toast;

import androidx.appcompat.app.AppCompatActivity;
import androidx.appcompat.app.AppCompatDelegate;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;

import com.example.offlinebible.R;
import com.example.offlinebible.adapters.VerseAdapter;
import com.example.offlinebible.data.DatabaseCopier;
import com.example.offlinebible.data.DatabaseHelper;
import com.example.offlinebible.models.BibleVerse;

import java.util.ArrayList;
import java.util.List;
import java.util.Locale;

public class MainActivity extends AppCompatActivity implements VerseAdapter.OnVerseInteractionListener {

    private DatabaseHelper dbHelper;
    private RecyclerView rvVerses;
    private VerseAdapter adapter;
    private TextToSpeech tts;
    private boolean ttsReady = false;
    private boolean isSpeaking = false;

    private Spinner spinnerVersion, spinnerBook, spinnerChapter;
    private ImageButton btnNightMode, btnSearch, btnMenu;
    private View layoutReader;
    private androidx.cardview.widget.CardView cardRead, cardSearch, cardHymns, cardFavorites;
    private TextView tvDailyVerse;

    private List<String> versionList = new ArrayList<>();
    private List<String> bookList = new ArrayList<>();
    private List<Integer> chapterList = new ArrayList<>();

    private String currentVersion = "KJV";
    private String currentBook = "Genesis";
    private int currentChapter = 1;
    private boolean isNightMode = false;
    private boolean currentVersionIsEnglish = true;

    // Flags to prevent spinner callbacks during programmatic updates
    private boolean suppressVersionCallback = false;
    private boolean suppressBookCallback = false;
    private boolean suppressChapterCallback = false;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        // 1. Copy pre-built DB from assets if needed
        DatabaseCopier copier = new DatabaseCopier(this);
        copier.createDatabaseIfNotExists();

        // 2. Open helper
        dbHelper = new DatabaseHelper(this);

        // 3. Wire up views
        rvVerses = findViewById(R.id.rvVerses);
        rvVerses.setLayoutManager(new LinearLayoutManager(this));

        spinnerVersion = findViewById(R.id.spinnerVersion);
        spinnerBook = findViewById(R.id.spinnerBook);
        spinnerChapter = findViewById(R.id.spinnerChapter);

        btnNightMode = findViewById(R.id.btnNightMode);
        btnSearch = findViewById(R.id.btnSearchTop);
        btnMenu = findViewById(R.id.btnMenu);

        layoutReader = findViewById(R.id.layoutReader);
        cardRead = findViewById(R.id.cardRead);
        cardSearch = findViewById(R.id.cardSearch);
        cardHymns = findViewById(R.id.cardHymns);
        cardFavorites = findViewById(R.id.cardFavorites);
        tvDailyVerse = findViewById(R.id.tvDailyVerse);

        // Populate a random daily verse
        tvDailyVerse.setText("\"For I know the plans I have for you,\" declares the Lord, \"plans to prosper you and not to harm you...\"");

        // Hide reader by default
        layoutReader.setVisibility(View.GONE);

        // 4. Initialise spinners from database
        initVersionSpinner();

        // 5. TTS
        initTTS();

        // 6. Navigation / Home Actions
        cardRead.setOnClickListener(v -> {
            layoutReader.setVisibility(View.VISIBLE);
            Toast.makeText(this, "Opening Bible Reader...", Toast.LENGTH_SHORT).show();
            rvVerses.requestFocus();
        });

        cardSearch.setOnClickListener(v -> showSearchDialog());
        btnSearch.setOnClickListener(v -> showSearchDialog());

        cardHymns.setOnClickListener(v -> Toast.makeText(this, "Hymns feature coming soon!", Toast.LENGTH_SHORT).show());
        cardFavorites.setOnClickListener(v -> Toast.makeText(this, "Favorites feature coming soon!", Toast.LENGTH_SHORT).show());

        btnNightMode.setOnClickListener(v -> toggleNightMode());
        btnMenu.setOnClickListener(v -> Toast.makeText(this, "Menu coming soon!", Toast.LENGTH_SHORT).show());
    }

    // ===================== VERSION SPINNER =====================

    private void initVersionSpinner() {
        versionList = dbHelper.getAvailableVersions();
        ArrayAdapter<String> vAdapter = new ArrayAdapter<>(this,
                android.R.layout.simple_spinner_dropdown_item, versionList);
        spinnerVersion.setAdapter(vAdapter);

        spinnerVersion.setOnItemSelectedListener(new AdapterView.OnItemSelectedListener() {
            @Override
            public void onItemSelected(AdapterView<?> parent, View view, int pos, long id) {
                if (suppressVersionCallback) { suppressVersionCallback = false; return; }
                currentVersion = versionList.get(pos);
                currentVersionIsEnglish = dbHelper.isEnglishVersion(currentVersion);
                initBookSpinner();
            }
            @Override public void onNothingSelected(AdapterView<?> parent) {}
        });

        // Trigger initial book population
        if (!versionList.isEmpty()) {
            currentVersion = versionList.get(0);
            currentVersionIsEnglish = dbHelper.isEnglishVersion(currentVersion);
            initBookSpinner();
        }
    }

    // ===================== BOOK SPINNER =====================

    private void initBookSpinner() {
        bookList = dbHelper.getBooks(currentVersion);
        ArrayAdapter<String> bAdapter = new ArrayAdapter<>(this,
                android.R.layout.simple_spinner_dropdown_item, bookList);
        suppressBookCallback = true;
        spinnerBook.setAdapter(bAdapter);

        spinnerBook.setOnItemSelectedListener(new AdapterView.OnItemSelectedListener() {
            @Override
            public void onItemSelected(AdapterView<?> parent, View view, int pos, long id) {
                if (suppressBookCallback) { suppressBookCallback = false; return; }
                currentBook = bookList.get(pos);
                currentChapter = 1;
                initChapterSpinner();
            }
            @Override public void onNothingSelected(AdapterView<?> parent) {}
        });

        if (!bookList.isEmpty()) {
            currentBook = bookList.get(0);
            currentChapter = 1;
            initChapterSpinner();
        }
    }

    // ===================== CHAPTER SPINNER =====================

    private void initChapterSpinner() {
        int count = dbHelper.getChapterCount(currentVersion, currentBook);
        chapterList = new ArrayList<>();
        for (int i = 1; i <= count; i++) chapterList.add(i);

        ArrayAdapter<Integer> cAdapter = new ArrayAdapter<>(this,
                android.R.layout.simple_spinner_dropdown_item, chapterList);
        suppressChapterCallback = true;
        spinnerChapter.setAdapter(cAdapter);

        spinnerChapter.setOnItemSelectedListener(new AdapterView.OnItemSelectedListener() {
            @Override
            public void onItemSelected(AdapterView<?> parent, View view, int pos, long id) {
                if (suppressChapterCallback) { suppressChapterCallback = false; return; }
                currentChapter = chapterList.get(pos);
                loadChapter();
            }
            @Override public void onNothingSelected(AdapterView<?> parent) {}
        });

        loadChapter();
    }

    // ===================== LOAD CHAPTER =====================

    private void loadChapter() {
        // Stop any ongoing TTS when navigating
        stopTTS();

        List<BibleVerse> verses = dbHelper.getChapter(currentVersion, currentBook, currentChapter);

        // Header is now fixed "JK Bible", no dynamic update needed here for now

        if (adapter == null) {
            adapter = new VerseAdapter(this, verses, currentVersionIsEnglish, this);
            rvVerses.setAdapter(adapter);
        } else {
            adapter.updateVerses(verses, currentVersionIsEnglish);
        }

        // Scroll to top
        rvVerses.scrollToPosition(0);
    }

    // ===================== TEXT-TO-SPEECH =====================

    private void initTTS() {
        tts = new TextToSpeech(this, status -> {
            if (status == TextToSpeech.SUCCESS) {
                int result = tts.setLanguage(Locale.ENGLISH);
                ttsReady = (result != TextToSpeech.LANG_MISSING_DATA
                        && result != TextToSpeech.LANG_NOT_SUPPORTED);
            }
        });
    }

    @Override
    public void onPlayVoice(BibleVerse verse) {
        // Rule: English versions ONLY
        if (!currentVersionIsEnglish) {
            Toast.makeText(this, "Voice reading is only available for English versions.",
                    Toast.LENGTH_SHORT).show();
            return;
        }
        if (!ttsReady) {
            Toast.makeText(this, "Text-to-Speech engine not ready.", Toast.LENGTH_SHORT).show();
            return;
        }

        if (isSpeaking) {
            stopTTS();
        } else {
            tts.speak(verse.getText(), TextToSpeech.QUEUE_FLUSH, null, "verse_" + verse.getId());
            isSpeaking = true;
        }
    }

    private void stopTTS() {
        if (tts != null && isSpeaking) {
            tts.stop();
            isSpeaking = false;
        }
    }

    // ===================== BOOKMARK =====================

    @Override
    public void onToggleBookmark(BibleVerse verse, int position) {
        boolean newState = !verse.isBookmarked();
        verse.setBookmarked(newState);
        dbHelper.updateBookmark(verse.getId(), newState);
        adapter.notifyItemChanged(position);

        Toast.makeText(this, newState ? "Bookmarked" : "Bookmark removed", Toast.LENGTH_SHORT).show();
    }

    // ===================== HIGHLIGHT =====================

    @Override
    public void onToggleHighlight(BibleVerse verse, int position) {
        boolean newState = !verse.isHighlighted();
        verse.setHighlighted(newState);
        dbHelper.updateHighlight(verse.getId(), newState);
        adapter.notifyItemChanged(position);
    }

    // ===================== SEARCH DIALOG =====================

    private void showSearchDialog() {
        AlertDialog.Builder builder = new AlertDialog.Builder(this);
        builder.setTitle("Search in " + currentVersion);

        final EditText input = new EditText(this);
        input.setHint("Type a word or phrase...");
        builder.setView(input);

        builder.setPositiveButton("Search", (dialog, which) -> {
            String query = input.getText().toString().trim();
            if (!query.isEmpty()) {
                performSearch(query);
            }
        });
        builder.setNegativeButton("Cancel", null);
        builder.show();
    }

    private void performSearch(String query) {
        List<BibleVerse> results = dbHelper.searchVerses(currentVersion, query);
        if (results.isEmpty()) {
            Toast.makeText(this, "No results found for \"" + query + "\"", Toast.LENGTH_SHORT).show();
            return;
        }

        Toast.makeText(this, results.size() + " results found", Toast.LENGTH_SHORT).show();

        layoutReader.setVisibility(View.VISIBLE);

        if (adapter == null) {
            adapter = new VerseAdapter(this, results, currentVersionIsEnglish, this);
            rvVerses.setAdapter(adapter);
        } else {
            adapter.updateVerses(results, currentVersionIsEnglish);
        }
        rvVerses.scrollToPosition(0);
    }

    // ===================== NIGHT MODE =====================

    private void toggleNightMode() {
        isNightMode = !isNightMode;
        AppCompatDelegate.setDefaultNightMode(
                isNightMode ? AppCompatDelegate.MODE_NIGHT_YES : AppCompatDelegate.MODE_NIGHT_NO
        );
    }

    // ===================== LIFECYCLE =====================

    @Override
    protected void onDestroy() {
        if (tts != null) {
            tts.stop();
            tts.shutdown();
        }
        super.onDestroy();
    }
}
