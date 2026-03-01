import { BookOpen } from "lucide-react";
import { useSyncBible } from "@/hooks/use-bible";

export function SyncScreen() {
  const { error } = useSyncBible();

  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-background text-foreground p-6">
      <div className="relative animate-fade-in flex flex-col items-center max-w-md text-center space-y-6">
        <div className="w-24 h-24 bg-primary/5 rounded-3xl flex items-center justify-center shadow-inner relative overflow-hidden">
          <BookOpen className="w-12 h-12 text-primary relative z-10" />
          {!error && (
            <div className="absolute bottom-0 left-0 right-0 bg-primary/10 h-1/2 animate-pulse rounded-b-3xl"></div>
          )}
        </div>
        
        <div className="space-y-2">
          <h1 className="text-2xl font-bold tracking-tight">
            {error ? "Setup Failed" : "Preparing Your Bible"}
          </h1>
          <p className="text-muted-foreground text-sm">
            {error 
              ? error 
              : "Downloading database for offline use. This will only take a moment..."}
          </p>
        </div>

        {!error && (
          <div className="w-full h-2 bg-secondary rounded-full overflow-hidden">
            <div className="h-full bg-primary w-1/2 animate-[bounce_1s_infinite_alternate]" style={{ transformOrigin: 'left' }}></div>
          </div>
        )}
      </div>
    </div>
  );
}
