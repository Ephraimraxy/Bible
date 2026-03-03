# Bible Reader Offline 📖

A fully offline, feature-rich Android Bible application designed for speed, reliability, and ease of use. This app provides instant access to 16 complete Bible translations across 8 languages without requiring an internet connection.

## 🌟 Key Features

*   **100% Offline Access:** Read the Bible anytime, anywhere. No internet connection required after the initial installation.
*   **16 Complete Translations:** Includes popular English versions and essential African languages.
*   **Lightning Fast:** Powered by a pre-compiled, highly optimized 180MB SQLite database containing nearly 500,000 verses.
*   **Clean User Interface:** Built with modern Android UI principles for a distraction-free reading experience.
*   **Quick Navigation:** Easily jump between books, chapters, and verses.
*   **Search Functionality:** Instantly find verses containing specific keywords (coming soon/if implemented).

## 📚 Included Translations

The database (`bible.db`) contains 66 books (Genesis through Revelation) for every included version:

### English
*   **NIV** - New International Version (Alternative: World English Bible)
*   **NLT** - New Living Translation (Alternative: Free Bible Version)
*   **AMP** - Amplified Bible (Alternative: Literal Standard Version)
*   **NKJV** - New King James Version (Alternative: Revised Version 1885)
*   **NASB** - New American Standard Bible (Alternative: Douay-Rheims American)
*   **KJV** - King James Version
*   **ASV** - American Standard Version
*   **BBE** - Bible in Basic English

### African Languages
*   **SWA** - Swahili Contemporary Bible
*   **AMH** - Amharic Bible
*   **HAU** - Hausa Contemporary Bible
*   **IGB** - Igbo Contemporary Bible
*   **YOR** - Yoruba Contemporary Bible

### Other Languages
*   **FRA** - La Bible de l'Épée (French)
*   **SCH** - Schlachter (German)
*   **RVR** - Reina Valera (Spanish)

## 🛠️ Technical Details

*   **Platform:** Android (Java/XML)
*   **Database:** SQLite (`app/src/main/assets/bible.db`)
*   **Architecture:** The massive local database is handled via **Git Large File Storage (LFS)**. 

## 🚀 Cloning & Setup

Because this repository uses Git LFS for the 180MB SQLite database, you need to have Git LFS installed on your system before cloning.

1.  **Install Git LFS:**
    ```bash
    git lfs install
    ```
2.  **Clone the Repository:**
    ```bash
    git clone https://github.com/Ephraimraxy/Bible.git
    ```
3.  **Open in Android Studio:**
    Open the cloned folder in Android Studio. Ensure Gradle syncs successfully.
4.  **Run the App:**
    Build and run the project on an emulator or a physical Android device.

## 🤝 Contributing

Contributions are welcome! Feel free to open issues or submit pull requests for UI improvements, bug fixes, or entirely new features.

---
*Built with ❤️ for accessible, offline Bible study.*
