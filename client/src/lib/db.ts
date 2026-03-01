import Dexie, { type Table } from 'dexie';

// --- Types ---
export interface LocalVerse {
  id?: number;
  version: string;
  book: string;
  chapter: number;
  verse: number;
  text: string;
}

export interface LocalBookmark {
  id?: number;
  version: string;
  book: string;
  chapter: number;
  verse: number;
  createdAt: number;
}

export interface LocalHighlight {
  id?: number;
  version: string;
  book: string;
  chapter: number;
  verse: number;
  color: string;
  createdAt: number;
}

// --- Database Configuration ---
export class BibleDatabase extends Dexie {
  verses!: Table<LocalVerse>;
  bookmarks!: Table<LocalBookmark>;
  highlights!: Table<LocalHighlight>;

  constructor() {
    super('BibleAppDB');
    
    // Define schema
    // verses index: optimize for [version+book] lookups, and full text search
    this.version(1).stores({
      verses: '++id, version, book, chapter, [version+book], [version+book+chapter]',
      bookmarks: '++id, [version+book+chapter+verse]',
      highlights: '++id, [version+book+chapter+verse]'
    });
  }
}

export const db = new BibleDatabase();

// --- Standard Book Order (Fallback for Sorting) ---
export const BIBLE_BOOKS = [
  "Genesis", "Exodus", "Leviticus", "Numbers", "Deuteronomy", "Joshua", "Judges", "Ruth", "1 Samuel", "2 Samuel", "1 Kings", "2 Kings", "1 Chronicles", "2 Chronicles", "Ezra", "Nehemiah", "Esther", "Job", "Psalms", "Proverbs", "Ecclesiastes", "Song of Solomon", "Isaiah", "Jeremiah", "Lamentations", "Ezekiel", "Daniel", "Hosea", "Joel", "Amos", "Obadiah", "Jonah", "Micah", "Nahum", "Habakkuk", "Zephaniah", "Haggai", "Zechariah", "Malachi",
  "Matthew", "Mark", "Luke", "John", "Acts", "Romans", "1 Corinthians", "2 Corinthians", "Galatians", "Ephesians", "Philippians", "Colossians", "1 Thessalonians", "2 Thessalonians", "1 Timothy", "2 Timothy", "Titus", "Philemon", "Hebrews", "James", "1 Peter", "2 Peter", "1 John", "2 John", "3 John", "Jude", "Revelation"
];
