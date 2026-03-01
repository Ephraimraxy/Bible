## Packages
dexie | IndexedDB wrapper for offline storage
dexie-react-hooks | React hooks for Dexie
use-debounce | For search input debouncing

## Notes
- App uses Dexie (IndexedDB) for 100% offline functionality
- First load will hit GET /api/sync to populate the local database
- TTS (Text-to-Speech) is restricted to English versions ('KJV') natively via window.speechSynthesis
- Uses Lucide React for iconography
