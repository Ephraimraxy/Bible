package com.example.offlinebible.ui;

import android.app.AlertDialog;
import android.content.Intent;
import android.os.Bundle;
import android.speech.tts.TextToSpeech;
import android.text.Editable;
import android.text.TextWatcher;
import android.view.View;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.EditText;
import android.widget.ImageButton;
import android.widget.ImageView;
import android.widget.Spinner;
import android.widget.TextView;
import android.widget.Toast;
import android.os.Handler;
import android.os.Looper;
import android.view.ViewGroup;
import android.graphics.Color;
import androidx.annotation.NonNull;
import androidx.annotation.Nullable;

import androidx.appcompat.app.AppCompatActivity;
import androidx.appcompat.app.AppCompatDelegate;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;

import com.example.offlinebible.R;
import com.example.offlinebible.adapters.VerseAdapter;
import com.example.offlinebible.adapters.VersionSpinnerAdapter;
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
    private int currentReadingIndex = -1;

    private Handler carouselHandler = new Handler(Looper.getMainLooper());
    private Runnable carouselRunnable;
    private BibleVerse currentCarouselVerse;

    private Spinner spinnerVersion, spinnerBook, spinnerChapter;
    private ImageButton btnSearch, btnMenu, btnGlobalTTS, btnTextSettings;
    private View layoutReader, layoutHome;
    private androidx.cardview.widget.CardView cardRead, cardSearch, cardBookmarks, cardFavorites, cardHymns, cardAbout;
    private TextView tvDailyVerse;

    private List<String> versionList = new ArrayList<>();
    private List<String> bookList = new ArrayList<>();
    private List<String> chapterList = new ArrayList<>();

    private String currentVersion = "KJV";
    private String currentBook = "Genesis";
    private int currentChapter = 1;
    private boolean currentVersionIsEnglish = true;

    // Flags to prevent spinner callbacks during programmatic updates
    private boolean suppressVersionCallback = false;
    private boolean suppressBookCallback = false;
    private boolean suppressChapterCallback = false;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        // FORCIBLY DISABLE DARK MODE - Pure Light Theme Only
        AppCompatDelegate.setDefaultNightMode(AppCompatDelegate.MODE_NIGHT_NO);

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

        btnSearch = findViewById(R.id.btnSearchTop);
        btnMenu = findViewById(R.id.btnMenu);
        btnGlobalTTS = findViewById(R.id.btnGlobalTTS);
        btnTextSettings = findViewById(R.id.btnTextSettings);

        layoutHome = findViewById(R.id.layoutHome);
        layoutReader = findViewById(R.id.layoutReader);
        cardRead = findViewById(R.id.cardRead);
        cardSearch = findViewById(R.id.cardSearch);
        cardBookmarks = findViewById(R.id.cardBookmarks);
        cardFavorites = findViewById(R.id.cardFavorites);
        cardHymns = findViewById(R.id.cardHymns);
        cardAbout = findViewById(R.id.cardAbout);
        tvDailyVerse = findViewById(R.id.tvDailyVerse);

        // Hide reader by default
        layoutReader.setVisibility(View.GONE);

        // 4. Initialise spinners from database
        initVersionSpinner();

        // 5. TTS & Carousel
        initTTS();
        startDailyVerseCarousel();

        // 6. Navigation / Home Actions
        cardRead.setOnClickListener(v -> {
            showReader();
        });

        cardSearch.setOnClickListener(v -> showSearchDialog());
        btnSearch.setOnClickListener(v -> showSearchDialog());

        cardBookmarks.setOnClickListener(v -> showBookmarks());
        cardFavorites.setOnClickListener(v -> showFavorites());
        cardHymns.setOnClickListener(v -> {
            Intent intent = new Intent(MainActivity.this, HymnListActivity.class);
            startActivity(intent);
        });
        cardAbout.setOnClickListener(v -> showAboutDialog());

        btnMenu.setOnClickListener(v -> showHome());

        btnGlobalTTS.setOnClickListener(v -> toggleGlobalTTS());
        btnTextSettings.setOnClickListener(v -> showTextSettingsDialog());

        // Click daily verse to open reader
        tvDailyVerse.setOnClickListener(v -> {
            if (currentCarouselVerse != null) {
                currentBook = currentCarouselVerse.getBookName();
                currentChapter = currentCarouselVerse.getChapter();

                // Programmatically select in spinners to trigger chain reactions
                suppressBookCallback = false;
                initBookSpinner(); // This will load chapters and verses

                showReader();

                new Handler(Looper.getMainLooper()).postDelayed(() -> {
                    int pos = currentCarouselVerse.getVerse() - 1;
                    rvVerses.scrollToPosition(pos);
                    if (adapter != null) {
                        adapter.setFocusedPosition(pos);
                    }
                }, 800);
            }
        });

        // Menu button effect
        btnMenu.setOnClickListener(v -> {
            v.animate().scaleX(0.9f).scaleY(0.9f).setDuration(100).withEndAction(() -> {
                v.animate().scaleX(1.0f).scaleY(1.0f).setDuration(100).start();
                showHome();
            }).start();
        });
    }

    private void showReader() {
        layoutHome.setVisibility(View.GONE);
        layoutReader.setVisibility(View.VISIBLE);
        layoutReader.setVisibility(View.VISIBLE);
        updateTTSLanguage(); // Refresh TTS button state dynamically
        spinnerVersion.setSelection(versionList.indexOf(currentVersion));
        rvVerses.requestFocus();
    }

    private void showHome() {
        layoutReader.setVisibility(View.GONE);
        layoutHome.setVisibility(View.VISIBLE);
    }

    // ===================== VERSION SPINNER =====================

    private void initVersionSpinner() {
        versionList = dbHelper.getAvailableVersions();
        VersionSpinnerAdapter vAdapter = new VersionSpinnerAdapter(this, versionList, dbHelper);
        spinnerVersion.setAdapter(vAdapter);

        spinnerVersion.setOnItemSelectedListener(new AdapterView.OnItemSelectedListener() {
            @Override
            public void onItemSelected(AdapterView<?> parent, View view, int pos, long id) {
                if (suppressVersionCallback) {
                    suppressVersionCallback = false;
                    return;
                }
                currentVersion = versionList.get(pos);
                currentVersionIsEnglish = dbHelper.isEnglishVersion(currentVersion);
                updateTTSLanguage(); // Check if this language (Hausa/Igbo/Yoruba/etc) is supported by TTS
                suppressBookCallback = false; // Reset suppression on manual selection
                initBookSpinner();
            }

            @Override
            public void onNothingSelected(AdapterView<?> parent) {
            }
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
        ArrayAdapter<String> bAdapter = new ArrayAdapter<String>(this, R.layout.item_spinner_pill, bookList) {
            @NonNull
            @Override
            public View getView(int position, @Nullable View convertView, @NonNull ViewGroup parent) {
                TextView tv = (TextView) super.getView(position, convertView, parent);
                tv.setTextColor(Color.WHITE);
                return tv;
            }
        };
        bAdapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item);
        suppressBookCallback = true;
        spinnerBook.setAdapter(bAdapter);

        // Match selection or default to first
        int bookIndex = bookList.indexOf(currentBook);
        if (bookIndex >= 0) {
            spinnerBook.setSelection(bookIndex);
        } else if (!bookList.isEmpty()) {
            currentBook = bookList.get(0);
            currentChapter = 1; // RESET CHAPTER as well for new book/version safety
            spinnerBook.setSelection(0);
        }

        spinnerBook.setOnItemSelectedListener(new AdapterView.OnItemSelectedListener() {
            @Override
            public void onItemSelected(AdapterView<?> parent, View view, int pos, long id) {
                if (suppressBookCallback) {
                    suppressBookCallback = false;
                    return;
                }
                currentBook = bookList.get(pos);
                initChapterSpinner();
            }

            @Override
            public void onNothingSelected(AdapterView<?> parent) {
            }
        });

        initChapterSpinner();
    }

    // ===================== CHAPTER SPINNER =====================

    private void initChapterSpinner() {
        int count = dbHelper.getChapterCount(currentVersion, currentBook);
        chapterList.clear();
        for (int i = 1; i <= count; i++) {
            chapterList.add(String.valueOf(i));
        }

        ArrayAdapter<String> cAdapter = new ArrayAdapter<String>(this, R.layout.item_spinner_pill,
                chapterList) {
            @NonNull
            @Override
            public View getView(int position, @Nullable View convertView, @NonNull ViewGroup parent) {
                TextView tv = (TextView) super.getView(position, convertView, parent);
                tv.setTextColor(Color.WHITE);
                return tv;
            }
        };
        cAdapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item);

        suppressChapterCallback = true;
        spinnerChapter.setAdapter(cAdapter);

        // Match selection or default to first if out of bounds
        int chapIndex = chapterList.indexOf(String.valueOf(currentChapter));
        if (chapIndex >= 0) {
            spinnerChapter.setSelection(chapIndex);
        } else if (!chapterList.isEmpty()) {
            currentChapter = 1;
            spinnerChapter.setSelection(0);
        }

        spinnerChapter.setOnItemSelectedListener(new AdapterView.OnItemSelectedListener() {
            @Override
            public void onItemSelected(AdapterView<?> parent, View view, int pos, long id) {
                if (suppressChapterCallback) {
                    suppressChapterCallback = false;
                    return;
                }
                currentChapter = Integer.parseInt(chapterList.get(pos));
                loadChapter();
            }

            @Override
            public void onNothingSelected(AdapterView<?> parent) {
            }
        });

        loadChapter();
    }

    // ===================== LOAD CHAPTER =====================

    private List<BibleVerse> verses;

    private void loadChapter() {
        // Stop any ongoing TTS when navigating
        stopTTS();

        verses = dbHelper.getChapter(currentVersion, currentBook, currentChapter);

        // Header is now fixed "JK Bible", no dynamic update needed here for now

        if (adapter == null) {
            adapter = new VerseAdapter(this, verses, currentVersionIsEnglish, this);
            rvVerses.setAdapter(adapter);
        } else {
            adapter.setReadingPosition(-1);
            adapter.setFocusedPosition(-1); // Reset focus highlight on chapter change
            adapter.updateVerses(verses, currentVersionIsEnglish);
        }

        // Update TTS button visibility based on dynamic language support
        updateTTSLanguage();

        // Scroll to top
        rvVerses.scrollToPosition(0);
    }

    private void showFavorites() {
        showReader();
        List<BibleVerse> favs = dbHelper.getHighlightedVerses(currentVersion);
        if (favs.isEmpty()) {
            Toast.makeText(this, "No favorites yet. Long-press a verse to highlight it!", Toast.LENGTH_LONG).show();
        }
        updateReaderList(favs, "Favorites");
    }

    private void showBookmarks() {
        showReader();
        List<BibleVerse> marks = dbHelper.getBookmarkedVerses(currentVersion);
        if (marks.isEmpty()) {
            Toast.makeText(this, "No bookmarks yet. Click the star icon next to a verse!", Toast.LENGTH_LONG).show();
        }
        updateReaderList(marks, "Bookmarks");
    }

    private void updateReaderList(List<BibleVerse> list, String title) {
        if (adapter == null) {
            adapter = new VerseAdapter(this, list, currentVersionIsEnglish, this);
            rvVerses.setAdapter(adapter);
        } else {
            adapter.updateVerses(list, currentVersionIsEnglish);
        }
        rvVerses.scrollToPosition(0);
        Toast.makeText(this, title + " loaded", Toast.LENGTH_SHORT).show();
    }

    private void showTextSettingsDialog() {
        android.content.SharedPreferences prefs = getSharedPreferences("JKBiblePrefs", MODE_PRIVATE);
        float currentSize = prefs.getFloat("font_size", 18f);
        float currentSpacing = prefs.getFloat("line_spacing", 1.6f);

        AlertDialog.Builder builder = new AlertDialog.Builder(this);
        builder.setTitle("Text Settings");

        android.view.View dialogView = getLayoutInflater().inflate(R.layout.dialog_text_settings, null);
        builder.setView(dialogView);

        android.widget.SeekBar sbSize = dialogView.findViewById(R.id.sbFontSize);
        android.widget.SeekBar sbSpacing = dialogView.findViewById(R.id.sbLineSpacing);
        final TextView tvSizeVal = dialogView.findViewById(R.id.tvFontSizeVal);
        final TextView tvSpacingVal = dialogView.findViewById(R.id.tvLineSpacingVal);

        // Font Size: 12 - 36 (Seekbar 0-24)
        sbSize.setMax(24);
        sbSize.setKeyProgressIncrement(1);
        sbSize.setProgress((int) (currentSize - 12));
        tvSizeVal.setText((int) currentSize + "sp");

        // Line Spacing: 1.0 - 2.5 (Seekbar 0-15, divide by 10)
        sbSpacing.setMax(15);
        sbSpacing.setProgress((int) ((currentSpacing - 1.0f) * 10));
        tvSpacingVal.setText(String.format("%.1f", currentSpacing));

        sbSize.setOnSeekBarChangeListener(new android.widget.SeekBar.OnSeekBarChangeListener() {
            @Override
            public void onProgressChanged(android.widget.SeekBar sb, int p, boolean b) {
                tvSizeVal.setText((p + 12) + "sp");
                prefs.edit().putFloat("font_size", (float) (p + 12)).apply();
                if (adapter != null)
                    adapter.notifyDataSetChanged();
            }

            @Override
            public void onStartTrackingTouch(android.widget.SeekBar sb) {
            }

            @Override
            public void onStopTrackingTouch(android.widget.SeekBar sb) {
            }
        });

        sbSpacing.setOnSeekBarChangeListener(new android.widget.SeekBar.OnSeekBarChangeListener() {
            @Override
            public void onProgressChanged(android.widget.SeekBar sb, int p, boolean b) {
                float val = 1.0f + (p / 10.0f);
                tvSpacingVal.setText(String.format("%.1f", val));
                prefs.edit().putFloat("line_spacing", val).apply();
                if (adapter != null)
                    adapter.notifyDataSetChanged();
            }

            @Override
            public void onStartTrackingTouch(android.widget.SeekBar sb) {
            }

            @Override
            public void onStopTrackingTouch(android.widget.SeekBar sb) {
            }
        });

        builder.setPositiveButton("Done", null);
        builder.show();
    }

    // ===================== TEXT-TO-SPEECH (GLOBAL) =====================

    private void initTTS() {
        tts = new TextToSpeech(this, status -> {
            if (status == TextToSpeech.SUCCESS) {
                updateTTSLanguage(); // Set initial language
                tts.setOnUtteranceProgressListener(new android.speech.tts.UtteranceProgressListener() {
                    @Override
                    public void onStart(String utteranceId) {
                        try {
                            int verseNum = Integer.parseInt(utteranceId.replace("verse_", ""));
                            // Auto-scroll and Highlight on UI thread
                            runOnUiThread(() -> {
                                if (adapter != null) {
                                    adapter.setReadingPosition(verseNum - 1);
                                }
                                rvVerses.smoothScrollToPosition(verseNum - 1);
                            });
                        } catch (Exception e) {
                        }
                    }

                    @Override
                    public void onDone(String utteranceId) {
                        try {
                            int verseNum = Integer.parseInt(utteranceId.replace("verse_", ""));
                            currentReadingIndex = verseNum; // The NEXT verse to read is index
                            if (adapter != null && verses != null && currentReadingIndex < verses.size()) {
                                // Keep going
                                tts.speak(verses.get(currentReadingIndex).getText(), TextToSpeech.QUEUE_ADD, null,
                                        "verse_" + verses.get(currentReadingIndex).getVerse());
                            } else {
                                // Done reading chapter
                                runOnUiThread(() -> {
                                    isSpeaking = false;
                                    btnGlobalTTS.setImageResource(android.R.drawable.ic_media_play);
                                });
                            }
                        } catch (Exception e) {
                        }
                    }

                    @Override
                    public void onError(String utteranceId) {
                        runOnUiThread(() -> stopTTS());
                    }
                });
            }
        });
    }

    private void toggleGlobalTTS() {
        if (!currentVersionIsEnglish)
            return;
        if (!ttsReady || adapter == null || verses == null || verses.isEmpty())
            return;

        if (isSpeaking) {
            stopTTS();
        } else {
            isSpeaking = true;
            btnGlobalTTS.setImageResource(android.R.drawable.ic_media_pause);
            if (currentReadingIndex == -1 || currentReadingIndex >= verses.size()) {
                currentReadingIndex = 0; // Start from beginning of chapter
            }

            // Start speaking first verse in queue
            tts.speak(verses.get(currentReadingIndex).getText(), TextToSpeech.QUEUE_FLUSH, null,
                    "verse_" + verses.get(currentReadingIndex).getVerse());
        }
    }

    private void stopTTS() {
        if (tts != null) {
            tts.stop();
        }
        isSpeaking = false;
        currentReadingIndex = -1;
        if (adapter != null) {
            adapter.setReadingPosition(-1);
        }
        btnGlobalTTS.setImageResource(android.R.drawable.ic_media_play);
    }

    // ===================== DAILY VERSE CAROUSEL =====================

    private void startDailyVerseCarousel() {
        final Handler handler = new Handler();
        final Runnable runnable = new Runnable() {
            @Override
            public void run() {
                BibleVerse nextVerse = dbHelper.getRandomVerse(currentVersion);
                if (nextVerse != null) {
                    currentCarouselVerse = nextVerse;

                    // Simple fade animation
                    tvDailyVerse.animate().alpha(0f).setDuration(500).withEndAction(() -> {
                        tvDailyVerse.setText("\"" + nextVerse.getText().replaceAll("^\\d+\\s*", "") + "\"");
                        tvDailyVerse.animate().alpha(1f).setDuration(500).start();
                    }).start();
                }
                handler.postDelayed(this, 10000); // 10 seconds
            }
        };
        handler.post(runnable);
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
    public void onHighlight(BibleVerse verse, int position, String color) {
        dbHelper.updateHighlight(verse.getId(), color != null, color);
        verse.setHighlighted(color != null);
        verse.setHighlightColor(color);

        // Also add to favorites/bookmarks if color is selected
        if (color != null) {
            verse.setBookmarked(true);
            dbHelper.updateBookmark(verse.getId(), true);
        }

        if (adapter != null)
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

        showReader();

        if (adapter == null) {
            adapter = new VerseAdapter(this, results, currentVersionIsEnglish, this);
            rvVerses.setAdapter(adapter);
        } else {
            adapter.updateVerses(results, currentVersionIsEnglish);
        }
        rvVerses.scrollToPosition(0);
    }

    // ===================== ABOUT & HYMNS = heml =====================

    private void showAboutDialog() {
        AlertDialog.Builder builder = new AlertDialog.Builder(this);

        // Use a ScrollView to accommodate the rich biography
        android.widget.ScrollView scrollView = new android.widget.ScrollView(this);
        TextView tvMessage = new TextView(this);
        tvMessage.setPadding(50, 40, 50, 40);
        tvMessage.setTextSize(15);
        tvMessage.setLineSpacing(0, 1.4f);
        tvMessage.setTextColor(Color.BLACK);

        StringBuilder bio = new StringBuilder();
        bio.append("🌟 SPECIAL DEDICATION 🌟\n\n");
        bio.append("PROFESSOR JOHN KENNEDY OPARA, OFR, PhD\n");
        bio.append("______________________________________\n\n");

        bio.append(
                "This Bible application is specially dedicated to Professor John Kennedy Opara—a Father, a Mentor, and a true Man of God whose life is a living testimony of love for the Holy Scriptures.\n\n");

        bio.append("🎖 NATIONAL HONOR & SERVICE\n");
        bio.append(
                "Professor John Kennedy Opara is an Officer of the Order of the Federal Republic (OFR), a prestigious national honor awarded for his patriotic and distinguished service to Nigeria. He served with distinction as the Pioneer Executive Secretary of the Nigerian Christian Pilgrim Commission (NCPC) from 2008 to 2016, where he revolutionized the spiritual administrative framework for pilgrims nationwide.\n\n");

        bio.append("🎓 ACADEMIC EXCELLENCE\n");
        bio.append(
                "A giant in the academic world, Prof. John Kennedy Opara holds a PhD in Microbiology and is a proud alumnus of the world’s most prestigious institutions, including:\n");
        bio.append("• Harvard University\n");
        bio.append("• Stanford University\n");
        bio.append("• University of Oxford\n");
        bio.append("• University of Cambridge\n");
        bio.append("• Columbia University\n\n");

        bio.append("🚜 VISIONARY LEADERSHIP (CSS GROUP)\n");
        bio.append(
                "As the Founder and CEO of CSS Group (\"Called Servant to Service\"), he has redefined integrated farming in Africa. Through CSS Global Integrated Farms, he is transforming the agricultural sector, focusing on food security, reducing unemployment, and empowering the next generation of Nigerian youth through his innovative \"7Ps Business Model.\"\n\n");

        bio.append("📖 SPIRITUAL PHILOSOPHY\n");
        bio.append(
                "Driven by the mandate in 1 Corinthians 7:20, he views leadership as a divine calling to serve. His unwavering faith and dedication to mentoring others continue to inspire millions to find purpose through the Word of God.\n\n");

        bio.append("______________________________________\n");
        bio.append("JK BIBLE - CSS EDITION v1.0\n");
        bio.append("Dedicated by your son and mentee.");

        tvMessage.setText(bio.toString());
        scrollView.addView(tvMessage);

        builder.setView(scrollView);
        builder.setPositiveButton("Honor & Respect", null);
        builder.show();
    }

    private void updateTTSLanguage() {
        if (tts == null)
            return;

        String langName = dbHelper.getVersionLanguage(currentVersion);
        Locale locale = getLocaleForLanguage(langName);

        int result = tts.isLanguageAvailable(locale);
        ttsReady = (result != TextToSpeech.LANG_MISSING_DATA && result != TextToSpeech.LANG_NOT_SUPPORTED);

        if (ttsReady) {
            tts.setLanguage(locale);
            btnGlobalTTS.setVisibility(View.VISIBLE);
        } else {
            // Only show if English as a fallback, or hide if no dialect support
            if (langName.equalsIgnoreCase("English")) {
                tts.setLanguage(Locale.ENGLISH);
                btnGlobalTTS.setVisibility(View.VISIBLE);
                ttsReady = true;
            } else {
                btnGlobalTTS.setVisibility(View.GONE);
            }
        }
    }

    private Locale getLocaleForLanguage(String langName) {
        if (langName == null)
            return Locale.ENGLISH;
        switch (langName.toLowerCase()) {
            case "hausa":
                return new Locale("ha");
            case "igbo":
                return new Locale("ig");
            case "yoruba":
                return new Locale("yo");
            case "spanish":
                return new Locale("es");
            case "french":
                return Locale.FRENCH;
            case "german":
                return Locale.GERMAN;
            case "swahili":
                return new Locale("sw");
            case "amharic":
                return new Locale("am");
            default:
                return Locale.ENGLISH;
        }
    }

    // ===================== LIFECYCLE =====================

    @Override
    protected void onDestroy() {
        if (tts != null) {
            tts.stop();
            tts.shutdown();
        }
        if (carouselHandler != null && carouselRunnable != null) {
            carouselHandler.removeCallbacks(carouselRunnable);
        }
        super.onDestroy();
    }
}
