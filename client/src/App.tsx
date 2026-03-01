import { Switch, Route } from "wouter";
import { queryClient } from "./lib/queryClient";
import { QueryClientProvider } from "@tanstack/react-query";
import { Toaster } from "@/components/ui/toaster";
import { TooltipProvider } from "@/components/ui/tooltip";
import NotFound from "@/pages/not-found";
import Reader from "@/pages/Reader";
import { useSyncBible } from "@/hooks/use-bible";
import { SyncScreen } from "@/components/SyncScreen";

function AppContent() {
  const { isSyncing } = useSyncBible();

  if (isSyncing) {
    return <SyncScreen />;
  }

  return (
    <Switch>
      <Route path="/" component={Reader} />
      <Route component={NotFound} />
    </Switch>
  );
}

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <TooltipProvider>
        <AppContent />
        <Toaster />
      </TooltipProvider>
    </QueryClientProvider>
  );
}

export default App;
