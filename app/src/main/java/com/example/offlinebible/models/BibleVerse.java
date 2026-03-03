package com.example.offlinebible.models;

public class BibleVerse {
    private int id;
    private String versionId;
    private int bookNumber;
    private String bookName;
    private int chapter;
    private int verse;
    private String text;
    private boolean isBookmarked;
    private boolean isHighlighted;

    public BibleVerse(int id, String versionId, int bookNumber, String bookName, 
                      int chapter, int verse, String text, boolean isBookmarked, boolean isHighlighted) {
        this.id = id;
        this.versionId = versionId;
        this.bookNumber = bookNumber;
        this.bookName = bookName;
        this.chapter = chapter;
        this.verse = verse;
        this.text = text;
        this.isBookmarked = isBookmarked;
        this.isHighlighted = isHighlighted;
    }

    // Getters and Setters
    public int getId() { return id; }
    public String getVersionId() { return versionId; }
    public String getBookName() { return bookName; }
    public int getChapter() { return chapter; }
    public int getVerse() { return verse; }
    public String getText() { return text; }
    public boolean isBookmarked() { return isBookmarked; }
    public void setBookmarked(boolean bookmarked) { isBookmarked = bookmarked; }
    public boolean isHighlighted() { return isHighlighted; }
    public void setHighlighted(boolean highlighted) { isHighlighted = highlighted; }
}
