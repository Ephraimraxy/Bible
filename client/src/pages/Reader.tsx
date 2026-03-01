import { useState, useMemo, useEffect } from "react";
import { NavigationHeader } from "@/components/NavigationHeader";
import { SearchDialog } from "@/components/SearchDialog";
import { VerseActionMenu } from "@/components/VerseActionMenu";
import { useVerses, useUserAnnotations, toggleHighlight, clearHighlight, toggleBookmark } from "@/hooks/use-bible";

export default function Reader() {
  const [version, setVersion] = useState("KJV");
  const [book, setBook] = useState("Genesis");
  const [chapter, setChapter] = useState(1);
  const [searchOpen, setSearchOpen] = useState(false);
  const [selectedVerses, setSelectedVerses] = useState<Set<number>>(new Set());

  const verses = useVerses(version, book, chapter);
  const { highlights, bookmarks } = useUserAnnotations(version, book, chapter);

  // Clear selections when chapter changes
  useEffect(() => {
    setSelectedVerses(new Set());
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }, [version, book, chapter]);

  const chapterTextForTTS = useMemo(() => {
    return verses?.map(v => v.text).join(" ") || "";
  }, [verses]);

  const toggleVerseSelection = (verseNum: number) => {
    const next = new Set(selectedVerses);
    if (next.has(verseNum)) next.delete(verseNum);
    else next.add(verseNum);
    setSelectedVerses(next);
  };

  const handleHighlight = async (color: string) => {
    for (const v of Array.from(selectedVerses)) {
      if (color) {
        await toggleHighlight({ version, book, chapter, verse: v, color });
      } else {
        await clearHighlight({ version, book, chapter, verse: v });
      }
    }
    setSelectedVerses(new Set());
  };

  const handleBookmark = async () => {
    for (const v of Array.from(selectedVerses)) {
      await toggleBookmark({ version, book, chapter, verse: v });
    }
    setSelectedVerses(new Set());
  };

  const handleCopy = async () => {
    if (!verses) return;
    const sortedSelected = Array.from(selectedVerses).sort((a, b) => a - b);
    const textToCopy = sortedSelected.map(vNum => {
      const vText = verses.find(v => v.verse === vNum)?.text;
      return `[${book} ${chapter}:${vNum}] ${vText}`;
    }).join("\n");
    
    await navigator.clipboard.writeText(textToCopy);
    setSelectedVerses(new Set());
  };

  // Determine if all selected are bookmarked to show the right icon state
  const isAllSelectedBookmarked = useMemo(() => {
    if (selectedVerses.size === 0 || !bookmarks) return false;
    return Array.from(selectedVerses).every(vNum => 
      bookmarks.some(b => b.verse === vNum)
    );
  }, [selectedVerses, bookmarks]);

  const handleSearchSelect = (b: string, c: number, v: number) => {
    setBook(b);
    setChapter(c);
    // In a real app, we would scroll to the verse. For minimal implementation, we just set the chapter.
    setTimeout(() => {
      const el = document.getElementById(`verse-${v}`);
      if (el) {
        el.scrollIntoView({ behavior: 'smooth', block: 'center' });
        el.classList.add('bg-primary/10', 'transition-colors', 'duration-1000');
        setTimeout(() => el.classList.remove('bg-primary/10'), 2000);
      }
    }, 500);
  };

  return (
    <div className="min-h-screen flex flex-col bg-background selection:bg-primary/20">
      <NavigationHeader
        version={version}
        book={book}
        chapter={chapter}
        onVersionChange={setVersion}
        onBookChange={(b) => { setBook(b); setChapter(1); }}
        onChapterChange={setChapter}
        onSearchToggle={() => setSearchOpen(true)}
        chapterText={chapterTextForTTS}
      />

      <main className="flex-1 w-full max-w-3xl mx-auto px-4 sm:px-6 py-12 md:py-16 pb-32">
        <div className="mb-12 text-center animate-slide-up">
          <h1 className="text-4xl md:text-5xl font-serif text-foreground font-semibold mb-2">
            {book}
          </h1>
          <div className="text-xl text-muted-foreground font-serif">
            Chapter {chapter}
          </div>
        </div>

        <div className="space-y-1">
          {verses?.map((verse) => {
            const isSelected = selectedVerses.has(verse.verse);
            const hl = highlights?.find(h => h.verse === verse.verse);
            const isBm = bookmarks?.some(b => b.verse === verse.verse);

            return (
              <div 
                key={verse.id} 
                id={`verse-${verse.verse}`}
                onClick={() => toggleVerseSelection(verse.verse)}
                className={`
                  group relative px-3 py-1.5 md:py-2 rounded-xl transition-all cursor-pointer scripture-text text-lg md:text-xl
                  ${isSelected ? 'bg-secondary ring-1 ring-border shadow-sm' : 'hover:bg-secondary/50'}
                `}
              >
                {/* Bookmarked indicator */}
                {isBm && !isSelected && (
                  <div className="absolute -left-1 sm:-left-3 top-3 w-1.5 h-1.5 rounded-full bg-primary" />
                )}

                <span 
                  className={`
                    inline-block mr-3 text-xs font-sans font-bold select-none align-top mt-[0.4rem]
                    ${isSelected ? 'text-primary' : 'text-muted-foreground/60 group-hover:text-muted-foreground'}
                  `}
                >
                  {verse.verse}
                </span>

                <span 
                  className={`
                    transition-colors rounded-sm 
                    ${hl ? `bg-[hsl(var(--hl-${hl.color}))] text-[hsl(var(--foreground))]` : 'text-foreground/90'}
                  `}
                >
                  {verse.text}
                </span>
              </div>
            );
          })}
        </div>

        {!verses?.length && (
          <div className="text-center py-20 text-muted-foreground font-serif">
            Loading chapter text...
          </div>
        )}
      </main>

      <VerseActionMenu
        selectedCount={selectedVerses.size}
        isBookmarked={isAllSelectedBookmarked}
        onClear={() => setSelectedVerses(new Set())}
        onHighlight={handleHighlight}
        onBookmark={handleBookmark}
        onCopy={handleCopy}
      />

      <SearchDialog
        open={searchOpen}
        onOpenChange={setSearchOpen}
        version={version}
        onSelect={handleSearchSelect}
      />
    </div>
  );
}
