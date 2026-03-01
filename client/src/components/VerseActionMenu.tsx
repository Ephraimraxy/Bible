import { Bookmark, BookmarkCheck, Copy, Palette, X } from "lucide-react";
import { Button } from "./ui/button";

interface VerseActionMenuProps {
  selectedCount: number;
  isBookmarked: boolean;
  onClear: () => void;
  onBookmark: () => void;
  onHighlight: (color: string) => void;
  onCopy: () => void;
}

export function VerseActionMenu({
  selectedCount,
  isBookmarked,
  onClear,
  onBookmark,
  onHighlight,
  onCopy
}: VerseActionMenuProps) {
  if (selectedCount === 0) return null;

  const colors = [
    { id: 'yellow', class: 'bg-[hsl(var(--hl-yellow))] hover:bg-[hsl(var(--hl-yellow))/0.8]' },
    { id: 'green', class: 'bg-[hsl(var(--hl-green))] hover:bg-[hsl(var(--hl-green))/0.8]' },
    { id: 'blue', class: 'bg-[hsl(var(--hl-blue))] hover:bg-[hsl(var(--hl-blue))/0.8]' },
    { id: 'pink', class: 'bg-[hsl(var(--hl-pink))] hover:bg-[hsl(var(--hl-pink))/0.8]' },
  ];

  return (
    <div className="fixed bottom-6 left-1/2 -translate-x-1/2 z-50 animate-slide-up">
      <div className="bg-popover text-popover-foreground shadow-xl shadow-black/10 border border-border/50 rounded-full px-4 py-2 flex items-center gap-2 md:gap-4 backdrop-blur-md">
        
        <div className="text-sm font-medium px-2 border-r border-border hidden sm:block">
          {selectedCount} selected
        </div>

        {/* Highlights */}
        <div className="flex items-center gap-1.5 px-2 border-r border-border">
          <Palette className="w-4 h-4 text-muted-foreground mr-1" />
          {colors.map(c => (
            <button
              key={c.id}
              onClick={() => onHighlight(c.id)}
              className={`w-6 h-6 rounded-full shadow-sm transition-transform hover:scale-110 ${c.class}`}
              title={`Highlight ${c.id}`}
            />
          ))}
          <Button variant="ghost" size="icon" className="w-8 h-8 rounded-full" onClick={() => onHighlight('')} title="Remove Highlight">
            <X className="w-4 h-4 text-muted-foreground" />
          </Button>
        </div>

        {/* Actions */}
        <div className="flex items-center gap-1">
          <Button variant="ghost" size="icon" className="w-9 h-9 rounded-full" onClick={onCopy} title="Copy">
            <Copy className="w-4 h-4" />
          </Button>
          <Button 
            variant="ghost" 
            size="icon" 
            className="w-9 h-9 rounded-full" 
            onClick={onBookmark} 
            title={isBookmarked ? "Remove Bookmark" : "Bookmark"}
          >
            {isBookmarked ? (
              <BookmarkCheck className="w-4 h-4 text-primary fill-primary" />
            ) : (
              <Bookmark className="w-4 h-4" />
            )}
          </Button>
        </div>

        <Button variant="ghost" size="icon" className="w-8 h-8 rounded-full ml-1 hover:bg-destructive/10 hover:text-destructive" onClick={onClear}>
          <X className="w-4 h-4" />
        </Button>
      </div>
    </div>
  );
}
