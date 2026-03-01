import { Dialog, DialogContent, DialogHeader, DialogTitle } from "@/components/ui/dialog";
import { Input } from "@/components/ui/input";
import { Search as SearchIcon, Book } from "lucide-react";
import { useState } from "react";
import { useDebounce } from "use-debounce";
import { useSearch } from "@/hooks/use-bible";

interface SearchDialogProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  version: string;
  onSelect: (book: string, chapter: number, verse: number) => void;
}

export function SearchDialog({ open, onOpenChange, version, onSelect }: SearchDialogProps) {
  const [query, setQuery] = useState("");
  const [debouncedQuery] = useDebounce(query, 400);
  const results = useSearch(version, debouncedQuery);

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="sm:max-w-[600px] h-[80vh] flex flex-col p-0 gap-0 overflow-hidden bg-background/95 backdrop-blur-xl">
        <DialogHeader className="px-4 py-4 border-b border-border/50">
          <DialogTitle className="sr-only">Search Bible</DialogTitle>
          <div className="relative">
            <SearchIcon className="absolute left-3 top-1/2 -translate-y-1/2 h-5 w-5 text-muted-foreground" />
            <Input
              placeholder={`Search in ${version}...`}
              className="pl-10 h-12 text-base bg-secondary/50 border-transparent focus-visible:ring-primary/20 rounded-xl"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              autoFocus
            />
          </div>
        </DialogHeader>

        <div className="flex-1 overflow-y-auto p-2">
          {query.length > 0 && query.length < 3 && (
            <div className="text-center py-10 text-muted-foreground text-sm">
              Type at least 3 characters to search...
            </div>
          )}

          {debouncedQuery.length >= 3 && results?.length === 0 && (
            <div className="text-center py-10 text-muted-foreground text-sm">
              No results found for "{debouncedQuery}"
            </div>
          )}

          <div className="space-y-1 px-2 pb-4">
            {results?.map((verse) => (
              <button
                key={verse.id}
                onClick={() => {
                  onSelect(verse.book, verse.chapter, verse.verse);
                  onOpenChange(false);
                }}
                className="w-full text-left p-3 rounded-xl hover:bg-accent/60 transition-colors group flex flex-col gap-1"
              >
                <div className="flex items-center gap-2 text-xs font-semibold text-primary/80">
                  <Book className="h-3 w-3" />
                  {verse.book} {verse.chapter}:{verse.verse}
                </div>
                <div className="text-sm scripture-text line-clamp-2 text-foreground/90 group-hover:text-foreground">
                  {verse.text}
                </div>
              </button>
            ))}
          </div>
        </div>
      </DialogContent>
    </Dialog>
  );
}
