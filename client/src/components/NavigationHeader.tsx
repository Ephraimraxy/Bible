import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { ThemeToggle } from "./ThemeToggle";
import { useBooks, useChapters, useVersions } from "@/hooks/use-bible";
import { Settings, Search as SearchIcon, Volume2, Pause, Play, Square } from "lucide-react";
import { Button } from "./ui/button";
import { useTTS } from "@/hooks/use-tts";

interface NavigationHeaderProps {
  version: string;
  book: string;
  chapter: number;
  onVersionChange: (v: string) => void;
  onBookChange: (b: string) => void;
  onChapterChange: (c: number) => void;
  onSearchToggle: () => void;
  chapterText: string;
}

export function NavigationHeader({
  version,
  book,
  chapter,
  onVersionChange,
  onBookChange,
  onChapterChange,
  onSearchToggle,
  chapterText
}: NavigationHeaderProps) {
  const versions = useVersions() || ['KJV', 'Hausa Bible', 'Yoruba Bible', 'Igbo Bible'];
  const books = useBooks(version);
  const chapters = useChapters(version, book);
  
  const { speak, pause, resume, stop, isPlaying, isPaused, isSupported } = useTTS();
  
  // TTS is only allowed for English version as per requirements
  const canUseTTS = isSupported && version === 'KJV';

  const handleTtsToggle = () => {
    if (isPlaying) {
      pause();
    } else if (isPaused) {
      resume();
    } else {
      speak(`${book} Chapter ${chapter}. ${chapterText}`);
    }
  };

  return (
    <header className="sticky top-0 z-50 w-full border-b border-border/40 bg-background/80 backdrop-blur-xl supports-[backdrop-filter]:bg-background/60">
      <div className="flex h-16 items-center px-4 gap-2 md:gap-4 max-w-5xl mx-auto">
        
        {/* Version Selector */}
        <Select value={version} onValueChange={onVersionChange}>
          <SelectTrigger className="w-[100px] md:w-[140px] border-none shadow-none font-semibold hover:bg-accent/50 transition-colors focus:ring-0">
            <SelectValue placeholder="Version" />
          </SelectTrigger>
          <SelectContent>
            {versions.map(v => (
              <SelectItem key={v} value={v}>{v}</SelectItem>
            ))}
          </SelectContent>
        </Select>

        <div className="h-6 w-px bg-border mx-1 hidden md:block"></div>

        {/* Book Selector */}
        <Select value={book} onValueChange={onBookChange}>
          <SelectTrigger className="flex-1 md:w-[180px] border-none shadow-none font-semibold hover:bg-accent/50 transition-colors focus:ring-0 text-left">
            <SelectValue placeholder="Book" />
          </SelectTrigger>
          <SelectContent className="max-h-[60vh]">
            {books.map(b => (
              <SelectItem key={b} value={b}>{b}</SelectItem>
            ))}
          </SelectContent>
        </Select>

        {/* Chapter Selector */}
        <Select value={chapter.toString()} onValueChange={(val) => onChapterChange(parseInt(val, 10))}>
          <SelectTrigger className="w-[70px] border-none shadow-none font-semibold hover:bg-accent/50 transition-colors focus:ring-0">
            <SelectValue placeholder="Ch" />
          </SelectTrigger>
          <SelectContent className="max-h-[60vh] min-w-[80px]">
            {chapters.map(c => (
              <SelectItem key={c} value={c.toString()}>{c}</SelectItem>
            ))}
          </SelectContent>
        </Select>

        <div className="flex-1" />

        {/* Actions */}
        <div className="flex items-center gap-1 md:gap-2">
          {canUseTTS && (
            <div className="flex items-center bg-accent/50 rounded-full px-1">
              <Button 
                variant="ghost" 
                size="icon" 
                onClick={handleTtsToggle}
                className="h-9 w-9 rounded-full text-primary"
                title={isPlaying ? "Pause Reading" : "Read Chapter"}
              >
                {isPlaying ? <Pause className="h-4 w-4" /> : <Volume2 className="h-4 w-4" />}
              </Button>
              {(isPlaying || isPaused) && (
                <Button 
                  variant="ghost" 
                  size="icon" 
                  onClick={stop}
                  className="h-9 w-9 rounded-full text-muted-foreground hover:text-destructive"
                  title="Stop"
                >
                  <Square className="h-3.5 w-3.5 fill-current" />
                </Button>
              )}
            </div>
          )}

          <Button variant="ghost" size="icon" onClick={onSearchToggle} className="rounded-full">
            <SearchIcon className="h-5 w-5 text-muted-foreground" />
          </Button>
          
          <ThemeToggle />
        </div>
      </div>
    </header>
  );
}
