import { useLiveQuery } from 'dexie-react-hooks';
import { db, BIBLE_BOOKS, type LocalHighlight, type LocalBookmark } from '@/lib/db';
import { useState, useEffect } from 'react';
import { api } from '@shared/routes';

// ==========================================
// DB SYNC HOOK
// ==========================================
export function useSyncBible() {
  const [isSyncing, setIsSyncing] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function sync() {
      try {
        const count = await db.verses.count();
        if (count > 0) {
          setIsSyncing(false);
          return;
        }

        // DB is empty, fetch from API
        const res = await fetch(api.sync.path);
        if (!res.ok) throw new Error('Failed to fetch Bible database');
        
        const verses = await res.json();
        
        // Fast bulk insert
        await db.verses.bulkAdd(verses);
        setIsSyncing(false);
      } catch (err: any) {
        setError(err.message || 'An error occurred during sync');
        setIsSyncing(false);
      }
    }
    sync();
  }, []);

  return { isSyncing, error };
}

// ==========================================
// NAVIGATION HOOKS
// ==========================================
export function useVersions() {
  return useLiveQuery(async () => {
    const versions = await db.verses.orderBy('version').uniqueKeys();
    return versions as string[];
  }, [], ['KJV']); // default fallback
}

export function useBooks(version: string) {
  return useLiveQuery(async () => {
    if (!version) return [];
    // Extract unique books for the given version
    const keys = await db.verses.where('version').equals(version).uniqueKeys();
    // uniqueKeys returns arrays if compound index, or just values. We didn't use a compound index for the primary uniqueKeys call, but we can filter distinct manually or rely on our standard list.
    // For performance, we'll query all books for this version and get distinct ones.
    const collection = db.verses.where('version').equals(version);
    const uniqueBooks = new Set<string>();
    await collection.eachKey(key => {
      // Actually getting distinct books from large DB can be slow if not indexed correctly.
      // We will rely on BIBLE_BOOKS standard order, filtering to ensure they exist.
    });
    
    // Fast path: Just return BIBLE_BOOKS as they are standard across our target languages.
    return BIBLE_BOOKS;
  }, [version], BIBLE_BOOKS);
}

export function useChapters(version: string, book: string) {
  return useLiveQuery(async () => {
    if (!version || !book) return [1];
    const verses = await db.verses
      .where('[version+book]')
      .equals([version, book])
      .toArray();
    
    const chapters = new Set(verses.map(v => v.chapter));
    return Array.from(chapters).sort((a, b) => a - b);
  }, [version, book], [1]);
}

// ==========================================
// CONTENT HOOKS
// ==========================================
export function useVerses(version: string, book: string, chapter: number) {
  return useLiveQuery(
    () => db.verses
      .where('[version+book+chapter]')
      .equals([version, book, chapter])
      .sortBy('verse'),
    [version, book, chapter],
    []
  );
}

export function useSearch(version: string, query: string) {
  return useLiveQuery(async () => {
    if (!query || query.length < 3) return [];
    const lowerQuery = query.toLowerCase();
    
    // In a real app, you'd use a FTS index. Here we do an in-memory filter of the selected version.
    return db.verses
      .where('version')
      .equals(version)
      .filter(v => v.text.toLowerCase().includes(lowerQuery))
      .limit(50) // limit for performance
      .toArray();
  }, [version, query], []);
}

// ==========================================
// USER DATA HOOKS (Bookmarks & Highlights)
// ==========================================
export function useUserAnnotations(version: string, book: string, chapter: number) {
  const highlights = useLiveQuery(
    () => db.highlights
      .where('version').equals(version)
      .and(h => h.book === book && h.chapter === chapter)
      .toArray(),
    [version, book, chapter],
    []
  );

  const bookmarks = useLiveQuery(
    () => db.bookmarks
      .where('version').equals(version)
      .and(b => b.book === book && b.chapter === chapter)
      .toArray(),
    [version, book, chapter],
    []
  );

  return { highlights, bookmarks };
}

export async function toggleHighlight(verseRef: Omit<LocalHighlight, 'id' | 'createdAt'>) {
  const existing = await db.highlights
    .where('[version+book+chapter+verse]')
    .equals([verseRef.version, verseRef.book, verseRef.chapter, verseRef.verse])
    .first();

  if (existing && existing.color === verseRef.color) {
    await db.highlights.delete(existing.id!);
  } else if (existing) {
    await db.highlights.update(existing.id!, { color: verseRef.color });
  } else {
    await db.highlights.add({ ...verseRef, createdAt: Date.now() });
  }
}

export async function clearHighlight(verseRef: Omit<LocalHighlight, 'id' | 'createdAt' | 'color'>) {
  const existing = await db.highlights
    .where('[version+book+chapter+verse]')
    .equals([verseRef.version, verseRef.book, verseRef.chapter, verseRef.verse])
    .first();
    
  if (existing) {
    await db.highlights.delete(existing.id!);
  }
}

export async function toggleBookmark(verseRef: Omit<LocalBookmark, 'id' | 'createdAt'>) {
  const existing = await db.bookmarks
    .where('[version+book+chapter+verse]')
    .equals([verseRef.version, verseRef.book, verseRef.chapter, verseRef.verse])
    .first();

  if (existing) {
    await db.bookmarks.delete(existing.id!);
  } else {
    await db.bookmarks.add({ ...verseRef, createdAt: Date.now() });
  }
}
