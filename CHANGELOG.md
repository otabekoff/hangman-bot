# Changelog

All notable changes to the Hangman Telegram Bot project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-10-05

### Added
- 🌍 **Multilingual Support**: Full interface in 3 languages (English, Russian, Uzbek)
- ⌨️ **Language-Specific Keyboards**:
  - English: A-Z alphabet (26 letters + apostrophe)
  - Russian: Complete Cyrillic alphabet (33 letters)
  - Uzbek: Latin-based alphabet with special characters (O', G', SH)
- 📚 **CSV Word Database**: Separate word files for each language
  - `words-en.csv` - English words with categories
  - `words-ru.csv` - Russian words with categories
  - `words-uz.csv` - Uzbek words with categories
- 🔘 **Inline Keyboard Language Selection**: User-friendly language picker on first start
- 🎯 **Category Display**: Shows word category during gameplay
- 💬 **Interactive Word Display**: Word shown as inline buttons (revealed letters or *)
- 🧹 **Session Management**: Automatic cleanup of game messages for better UX
- 🚫 **END Button**: Quick game termination button on keyboard
- 🌐 **Language Change Menu**: Easy language switching after game ends
- 🎮 **Menu Keyboard**: Play and Change Language buttons after game completion

### Changed
- Keyboard layout changed from QWERTY to alphabetical order
- Apostrophe added to all keyboard layouts for words like "don't", "o'zbek"
- END button integrated into the fourth row of keyboard instead of separate row
- Game messages now accumulate during play and clear only at game end
- Language selection now uses inline buttons instead of reply keyboard

### Technical
- Implemented FSM (Finite State Machine) for state management
- User preferences stored in memory for language settings
- Language-specific keyboard layout selection based on user preference
- Async/await pattern throughout for better performance
- Enhanced error handling and logging

## [0.1.0] - Initial Development

### Added
- Basic Hangman game mechanics
- Single language support (English)
- QWERTY keyboard layout
- 8-stage hangman image progression
- Word guessing with letter-by-letter input
- Basic commands: `/start`, `/play`, `/help`, `/stop`
- Telegram bot integration using aiogram 3.13.1
- Environment variable configuration with .env file

---

Copyright © 2025 Otabek Sadiridinov. All rights reserved.