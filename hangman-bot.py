# Purpose of game is to hang Ibrohim.

import asyncio
import logging
import random
import os
import csv
from aiohttp import web
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import FSInputFile, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InputMediaPhoto, InlineKeyboardMarkup, InlineKeyboardButton
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN not found in .env file")

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

# Game states
class GameStates(StatesGroup):
    selecting_language = State()
    playing = State()

# Translations for UI
TRANSLATIONS = {
    'en': {
        'welcome': '👋 Welcome to Hangman Game!\n\n🎯 Your goal is to guess the word before the hangman is complete.\n\nUse /play to start a new game!',
        'select_language': 'Please select your language:',
        'select_word_lang': 'Now select the language for game words:',
        'game_title': '🎮 <b>Hangman Game</b>',
        'category': '📂 Category',
        'wrong_guesses': 'Wrong guesses',
        'guessed_letters': 'Guessed letters',
        'tap_letter': '💡 Tap a letter to guess!',
        'choose_letter': 'Choose a letter:',
        'congratulations': '🎉 <b>Congratulations! You won!</b>',
        'game_over': '💀 <b>Game Over! You lost!</b>',
        'the_word_was': 'The word was',
        'better_luck': 'Better luck next time!',
        'start_new_game': 'Start a new game with /play',
        'game_ended': 'Game ended. Use /play to start a new game.',
        'game_stopped': '🛑 Game stopped!',
        'no_active_game': 'No active game. Start one with /play',
        'change_language': '🌐 Change Language',
        'play': '▶️ Play',
        'end': '🚫',
        'help_title': '📖 <b>How to play:</b>',
        'help_text': '1. Start a game with /play\n2. Send a letter to make a guess\n3. Try to guess the word before running out of attempts!\n\nYou have {max_guesses} wrong guesses before the game ends.\n\nCommands:\n/play - Start a new game\n/stop - Stop current game\n/help - Show this message'
    },
    'ru': {
        'welcome': '👋 Добро пожаловать в игру Виселица!\n\n🎯 Ваша цель - угадать слово до того, как виселица будет завершена.\n\nИспользуйте /play чтобы начать новую игру!',
        'select_word_lang': 'Теперь выберите язык для игровых слов:',
        'game_title': '🎮 <b>Игра Виселица</b>',
        'category': '📂 Категория',
        'wrong_guesses': 'Неверных попыток',
        'guessed_letters': 'Угаданные буквы',
        'tap_letter': '💡 Нажмите на букву, чтобы угадать!',
        'choose_letter': 'Выберите букву:',
        'congratulations': '🎉 <b>Поздравляем! Вы выиграли!</b>',
        'game_over': '💀 <b>Игра окончена! Вы проиграли!</b>',
        'the_word_was': 'Слово было',
        'better_luck': 'Удачи в следующий раз!',
        'start_new_game': 'Начните новую игру с /play',
        'game_ended': 'Игра окончена. Используйте /play для новой игры.',
        'game_stopped': '🛑 Игра остановлена!',
        'no_active_game': 'Нет активной игры. Начните с /play',
        'change_language': '🌐 Изменить язык',
        'play': '▶️ Играть',
        'end': '🚫',
        'help_title': '📖 <b>Как играть:</b>',
        'help_text': '1. Начните игру с /play\n2. Отправьте букву, чтобы сделать догадку\n3. Попробуйте угадать слово до того, как закончатся попытки!\n\nУ вас есть {max_guesses} неверных попыток до конца игры.\n\nКоманды:\n/play - Начать новую игру\n/stop - Остановить игру\n/help - Показать это сообщение'
    },
    'uz': {
        'welcome': '👋 Dargor o\'yiniga xush kelibsiz!\n\n🎯 Maqsadingiz - dargor to\'liq tayyorlanishidan oldin so\'zni topish.\n\n/play bilan yangi o\'yin boshlang!',
        'select_word_lang': 'Endi o\'yin so\'zlari uchun tilni tanlang:',
        'game_title': '🎮 <b>Dargor O\'yini</b>',
        'category': '📂 Kategoriya',
        'wrong_guesses': 'Noto\'g\'ri urinishlar',
        'guessed_letters': 'Topilgan harflar',
        'tap_letter': '💡 Harfni tanlang!',
        'choose_letter': 'Harfni tanlang:',
        'congratulations': '🎉 <b>Tabriklaymiz! Siz yutdingiz!</b>',
        'game_over': '💀 <b>O\'yin tugadi! Siz yutqazdingiz!</b>',
        'the_word_was': 'So\'z edi',
        'better_luck': 'Keyingi safar omad tilaymiz!',
        'start_new_game': '/play bilan yangi o\'yin boshlang',
        'game_ended': 'O\'yin tugadi. Yangi o\'yin uchun /play dan foydalaning.',
        'game_stopped': '🛑 O\'yin to\'xtatildi!',
        'no_active_game': 'Faol o\'yin yo\'q. /play bilan boshlang',
        'change_language': '🌐 Tilni o\'zgartirish',
        'play': '▶️ O\'ynash',
        'end': '🚫',
        'help_title': '📖 <b>Qanday o\'ynash:</b>',
        'help_text': '1. /play bilan o\'yin boshlang\n2. Harf yuboring\n3. Urinishlar tugashidan oldin so\'zni toping!\n\nSizda o\'yin tugashidan oldin {max_guesses} noto\'g\'ri urinish bor.\n\nKomandalar:\n/play - Yangi o\'yin boshlash\n/stop - O\'yinni to\'xtatish\n/help - Ushbu xabarni ko\'rsatish'
    }
}

# Load words from CSV file
def load_words_from_csv(lang='en'):
    """Load words and categories from language-specific CSV file"""
    words_dict = {}
    filename = f'words-{lang}.csv'
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                word = row.get('word', '').strip().upper()
                category = row.get('category', '').strip()
                if word and category:  # Skip empty rows
                    words_dict[word] = category
    except Exception as e:
        logging.error(f"Error loading {filename}: {e}")
    if not words_dict:
        words_dict = {
            'PYTHON': 'programming',
            'TELEGRAM': 'technology',
            'COMPUTER': 'technology'
        }
    return words_dict

# User preferences storage
user_preferences = {}

# Multilingual welcome message
MULTILINGUAL_WELCOME = (
    "🇬🇧 Welcome to Hangman Game!\n"
    "Please select your language:\n\n"
    "🇷🇺 Добро пожаловать в игру Виселица!\n"
    "Пожалуйста, выберите язык:\n\n"
    "🇺🇿 Dargor o'yiniga xush kelibsiz!\n"
    "Iltimos, tilni tanlang:"
)

# Image progression based on wrong guesses
IMAGE_STAGES = [
    'images/blank.png',           # 0 wrong guesses
    'images/head.png',            # 1 wrong guess
    'images/head-torso.png',      # 2 wrong guesses
    'images/h-t-lh.png',          # 3 wrong guesses
    'images/h-t-hands.png',       # 4 wrong guesses
    'images/h-t-hands-lf.png',    # 5 wrong guesses
    'images/fresh-man.png',       # 6 wrong guesses
    'images/died-man.png'         # 7 wrong guesses (game over)
]

MAX_WRONG_GUESSES = len(IMAGE_STAGES) - 1

# Keyboard layouts for different languages
KEYBOARD_LAYOUT_EN = [
    ['A', 'B', 'C', 'D', 'E', 'F', 'G'],
    ['H', 'I', 'J', 'K', 'L', 'M', 'N'],
    ['O', 'P', 'Q', 'R', 'S', 'T', 'U'],
    ['V', 'W', 'X', 'Y', 'Z', "'"]
]

# Russian Cyrillic alphabet (33 letters)
KEYBOARD_LAYOUT_RU = [
    ['А', 'Б', 'В', 'Г', 'Д', 'Е', 'Ё', 'Ж', 'З'],
    ['И', 'Й', 'К', 'Л', 'М', 'Н', 'О', 'П', 'Р'],
    ['С', 'Т', 'У', 'Ф', 'Х', 'Ц', 'Ч', 'Ш', 'Щ'],
    ['Ъ', 'Ы', 'Ь', 'Э', 'Ю', 'Я']
]

# Uzbek alphabet
KEYBOARD_LAYOUT_UZ = [
    ['A', 'B', 'C', 'D', 'E', 'F', 'G'],
    ['H', 'I', 'J', 'K', 'L', 'M', 'N'],
    ['O', 'P', 'Q', 'R', 'S', 'T', 'U'],
    ['V', 'X', 'Y', 'Z', "'"]
]

# Game data storage
games = {}

def get_text(user_id: int, key: str, **kwargs) -> str:
    """Get translated text for user's language"""
    lang = user_preferences.get(user_id, {}).get('lang', 'en')
    text = TRANSLATIONS.get(lang, TRANSLATIONS['en']).get(key, key)
    if kwargs:
        text = text.format(**kwargs)
    return text

def create_language_keyboard() -> InlineKeyboardMarkup:
    """Create inline keyboard for language selection"""
    keyboard = [
        [InlineKeyboardButton(text='🇬🇧 English', callback_data='lang_en'),
         InlineKeyboardButton(text='🇷🇺 Русский', callback_data='lang_ru'),
         InlineKeyboardButton(text='🇺🇿 O\'zbekcha', callback_data='lang_uz')]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def create_menu_keyboard(user_id: int) -> ReplyKeyboardMarkup:
    """Create menu keyboard after game ends"""
    keyboard = [
        [KeyboardButton(text=get_text(user_id, 'play'))],
        [KeyboardButton(text=get_text(user_id, 'change_language'))]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True, one_time_keyboard=False)

def create_keyboard(guessed_letters: set, word: str, user_id: int) -> ReplyKeyboardMarkup:
    """Create a keyboard with language-specific layout and END button"""
    # Get user's language and select appropriate keyboard layout
    lang = user_preferences.get(user_id, {}).get('lang', 'en')
    if lang == 'ru':
        layout = KEYBOARD_LAYOUT_RU
    elif lang == 'uz':
        layout = KEYBOARD_LAYOUT_UZ
    else:
        layout = KEYBOARD_LAYOUT_EN
    
    keyboard = []
    for row in layout:
        button_row = [KeyboardButton(text=letter) for letter in row]
        keyboard.append(button_row)
    # Add END button to the last row (fourth line)
    keyboard[-1].append(KeyboardButton(text=get_text(user_id, 'end')))
    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True,
        one_time_keyboard=False
    )

class HangmanGame:
    def __init__(self, user_id, chat_id, word_lang='en'):
        self.user_id = user_id
        self.chat_id = chat_id
        self.word_lang = word_lang
        # Load words for selected language
        words_dict = load_words_from_csv(word_lang)
        # Select a random word with its category
        self.word = random.choice(list(words_dict.keys()))
        self.category = words_dict[self.word]
        self.guessed_letters = set()
        self.wrong_guesses = 0
        self.game_over = False
        self.won = False
        self.last_message_id = None  # Store last bot message ID for editing
        self.last_image_path = None  # Track last image path for edit logic
        self.session_message_ids = []  # Track all message IDs for cleanup
    
    def get_display_word(self):
        """Return the word as a list of revealed or hidden letters (for inline keyboard)"""
        return [letter if letter in self.guessed_letters else '*' for letter in self.word]
    def get_word_inline_keyboard(self):
        """Return InlineKeyboardMarkup for the word display"""
        buttons = [InlineKeyboardButton(text=ch, callback_data='noop') for ch in self.get_display_word()]
        return InlineKeyboardMarkup(inline_keyboard=[buttons])
    
    def guess_letter(self, letter):
        """Process a letter guess"""
        letter = letter.upper()
        if letter in self.guessed_letters:
            return "already_guessed"
        self.guessed_letters.add(letter)
        if letter in self.word:
            # Check if won
            if all(l in self.guessed_letters for l in self.word):
                self.game_over = True
                self.won = True
            return "correct"
        else:
            self.wrong_guesses += 1
            # Fix: allow progression to final image (7th step)
            if self.wrong_guesses > MAX_WRONG_GUESSES:
                self.wrong_guesses = MAX_WRONG_GUESSES
            if self.wrong_guesses == MAX_WRONG_GUESSES:
                self.game_over = True
            return "wrong"
    
    def get_current_image(self):
        """Get the current hangman image based on wrong guesses"""
        return IMAGE_STAGES[min(self.wrong_guesses, len(IMAGE_STAGES) - 1)]
    
    def get_status_text(self):
        """Get the game status text (no word display)"""
        text = f"{get_text(self.user_id, 'game_title')}\n\n"
        text += f"{get_text(self.user_id, 'category')}: <b>{self.category}</b>\n\n"
        text += f"{get_text(self.user_id, 'wrong_guesses')}: {self.wrong_guesses}/{MAX_WRONG_GUESSES}\n"
        if self.guessed_letters:
            text += f"{get_text(self.user_id, 'guessed_letters')}: {', '.join(sorted(self.guessed_letters))}\n"
        if not self.game_over:
            text += f"\n{get_text(self.user_id, 'tap_letter')}"
        return text

@dp.message(Command('start'))
async def cmd_start(message: types.Message, state: FSMContext):
    """Handle /start command"""
    if not message.from_user:
        return
    user_id = message.from_user.id
    
    # Check if user has preferences
    if user_id not in user_preferences:
        await message.answer(
            MULTILINGUAL_WELCOME,
            reply_markup=create_language_keyboard()
        )
        await state.set_state(GameStates.selecting_language)
    else:
        await message.answer(
            get_text(user_id, 'welcome'),
            reply_markup=create_menu_keyboard(user_id)
        )

@dp.callback_query(F.data.startswith('lang_'))
async def handle_language_selection(callback: types.CallbackQuery, state: FSMContext):
    """Handle language selection from inline keyboard"""
    if not callback.from_user or not callback.data or not callback.message:
        return
    
    user_id = callback.from_user.id
    selected_lang = callback.data.split('_')[1]  # Extract 'en', 'ru', or 'uz'
    
    if user_id not in user_preferences:
        user_preferences[user_id] = {}
    user_preferences[user_id]['lang'] = selected_lang
    
    # Edit the message to show confirmation
    if isinstance(callback.message, types.Message):
        await callback.message.edit_text(
            get_text(user_id, 'welcome'),
            reply_markup=None
        )
        await bot.send_message(
            chat_id=callback.message.chat.id,
            text='✅',
            reply_markup=create_menu_keyboard(user_id)
        )
    await state.clear()
    await callback.answer()

@dp.message(Command('help'))
async def cmd_help(message: types.Message):
    """Handle /help command"""
    if not message.from_user:
        return
    user_id = message.from_user.id
    await message.answer(
        get_text(user_id, 'help_title') + '\n\n' + get_text(user_id, 'help_text', max_guesses=MAX_WRONG_GUESSES),
        parse_mode='HTML'
    )

@dp.message(Command('play'))
async def cmd_play(message: types.Message, state: FSMContext):
    """Start a new game"""
    if not message.from_user:
        return
    user_id = message.from_user.id
    
    # Check if user has set preferences
    if user_id not in user_preferences or 'lang' not in user_preferences[user_id]:
        await message.answer(
            MULTILINGUAL_WELCOME,
            reply_markup=create_language_keyboard()
        )
        await state.set_state(GameStates.selecting_language)
        return
    
    # Delete user's command message
    try:
        await message.delete()
    except:
        pass
    
    # Create new game
    word_lang = user_preferences[user_id]['lang']
    games[user_id] = HangmanGame(user_id, message.chat.id, word_lang)
    game = games[user_id]
    
    # Set state to playing
    await state.set_state(GameStates.playing)
    
    # Send game start message with image and keyboard
    image_path = game.get_current_image()
    photo = FSInputFile(image_path)
    inline_keyboard = game.get_word_inline_keyboard()
    sent_message = await bot.send_photo(
        chat_id=message.chat.id,
        photo=photo,
        caption=game.get_status_text(),
        parse_mode='HTML',
        reply_markup=inline_keyboard
    )
    game.last_message_id = sent_message.message_id
    game.session_message_ids.append(sent_message.message_id)
    # Send QWERTY reply keyboard in a separate message
    keyboard = create_keyboard(game.guessed_letters, game.word, user_id)
    keyboard_message = await bot.send_message(
        chat_id=message.chat.id,
        text=get_text(user_id, 'choose_letter'),
        reply_markup=keyboard
    )
    game.session_message_ids.append(keyboard_message.message_id)

@dp.message(Command('stop'))
async def cmd_stop(message: types.Message, state: FSMContext):
    """Stop the current game"""
    if not message.from_user:
        return
    user_id = message.from_user.id
    
    if user_id in games:
        game = games[user_id]
        # Delete all session messages
        for msg_id in game.session_message_ids:
            try:
                await bot.delete_message(chat_id=game.chat_id, message_id=msg_id)
            except:
                pass
        del games[user_id]
        await state.clear()
        await message.answer(
            f"{get_text(user_id, 'game_stopped')}\n\n"
            f"{get_text(user_id, 'the_word_was')}: <b>{game.word}</b>\n\n"
            f"{get_text(user_id, 'start_new_game')}",
            parse_mode='HTML',
            reply_markup=create_menu_keyboard(user_id)
        )
    else:
        await message.answer(
            get_text(user_id, 'no_active_game'),
            reply_markup=create_menu_keyboard(user_id)
        )

@dp.message(GameStates.playing, F.text)
async def handle_guess(message: types.Message, state: FSMContext):
    """Handle letter guesses during the game"""
    if not message.from_user or not message.text:
        return
    
    user_id = message.from_user.id
    
    if user_id not in games:
        await message.answer(get_text(user_id, 'no_active_game'))
        await state.clear()
        return
    
    game = games[user_id]
    text = message.text.strip()
    
    # Check for END button
    if text == get_text(user_id, 'end'):
        await cmd_stop(message, state)
        return
    
    # Validate input (single letter)
    if len(text) != 1 or not text.isalpha():
        # Delete invalid input message
        try:
            await message.delete()
        except:
            pass
        return
    
    # Delete user's guess message
    try:
        await message.delete()
    except:
        pass
    
    # Process the guess
    result = game.guess_letter(text)
    
    # Prepare response
    if result == "already_guessed":
        return
    image_path = game.get_current_image()
    if game.last_message_id:
        try:
            inline_keyboard = game.get_word_inline_keyboard()
            photo = FSInputFile(image_path)
            if game.game_over:
                # Send final result message
                if game.won:
                    caption = (
                        f"{get_text(user_id, 'congratulations')}\n\n"
                        f"{get_text(user_id, 'category')}: <b>{game.category}</b>\n"
                        f"{get_text(user_id, 'the_word_was')}: <b>{game.word}</b>\n\n"
                        f"{get_text(user_id, 'wrong_guesses')}: {game.wrong_guesses}/{MAX_WRONG_GUESSES}\n\n"
                        f"{get_text(user_id, 'start_new_game')}"
                    )
                    sent_message = await bot.send_photo(
                        chat_id=game.chat_id,
                        photo=photo,
                        caption=caption,
                        parse_mode='HTML',
                        reply_markup=ReplyKeyboardRemove()
                    )
                else:
                    caption = (
                        f"{get_text(user_id, 'game_over')}\n\n"
                        f"{get_text(user_id, 'category')}: <b>{game.category}</b>\n"
                        f"{get_text(user_id, 'the_word_was')}: <b>{game.word}</b>\n\n"
                        f"{get_text(user_id, 'better_luck')}\n\n"
                        f"{get_text(user_id, 'start_new_game')}"
                    )
                    sent_message = await bot.send_photo(
                        chat_id=game.chat_id,
                        photo=photo,
                        caption=caption,
                        parse_mode='HTML',
                        reply_markup=ReplyKeyboardRemove()
                    )
                # Delete all previous session messages except the final result
                for msg_id in game.session_message_ids:
                    try:
                        await bot.delete_message(chat_id=game.chat_id, message_id=msg_id)
                    except:
                        pass
                # Save only the final result message id
                game.session_message_ids = [sent_message.message_id]
                await bot.send_message(
                    chat_id=game.chat_id,
                    text=get_text(user_id, 'game_ended'),
                    reply_markup=create_menu_keyboard(user_id)
                )
                del games[user_id]
                await state.clear()
            else:
                caption = f"{game.get_status_text()}"
                sent_message = await bot.send_photo(
                    chat_id=game.chat_id,
                    photo=photo,
                    caption=caption,
                    parse_mode='HTML',
                    reply_markup=inline_keyboard
                )
                game.session_message_ids.append(sent_message.message_id)
                # Send QWERTY reply keyboard in a separate message
                keyboard = create_keyboard(game.guessed_letters, game.word, user_id)
                keyboard_message = await bot.send_message(
                    chat_id=game.chat_id,
                    text=get_text(user_id, 'choose_letter'),
                    reply_markup=keyboard
                )
                game.session_message_ids.append(keyboard_message.message_id)
                game.last_message_id = sent_message.message_id
        except Exception as e:
            logging.error(f"Error sending message: {e}")

@dp.message()
async def handle_other_messages(message: types.Message, state: FSMContext):
    """Handle messages when not in game"""
    if not message.from_user or not message.text:
        return
    
    user_id = message.from_user.id
    text = message.text
    
    # Handle menu buttons
    if text == get_text(user_id, 'play'):
        await cmd_play(message, state)
        return
    
    if text == get_text(user_id, 'change_language'):
        await message.answer(
            MULTILINGUAL_WELCOME,
            reply_markup=create_language_keyboard()
        )
        await state.set_state(GameStates.selecting_language)
        return
    
    # Delete user's message
    try:
        await message.delete()
    except:
        pass
    
    # Send temporary error message
    temp_msg = await bot.send_message(
        chat_id=message.chat.id,
        text=get_text(user_id, 'start_new_game')
    )
    
    # Delete the error message after 3 seconds
    await asyncio.sleep(3)
    try:
        await bot.delete_message(chat_id=message.chat.id, message_id=temp_msg.message_id)
    except:
        pass

async def health_check(request):
    """Health check endpoint to keep the machine active"""
    return web.Response(text="Bot is running!", status=200)

async def create_app():
    """Create aiohttp web application for health checks"""
    app = web.Application()
    app.router.add_get('/health', health_check)
    app.router.add_get('/', health_check)
    return app

async def main():
    """Main function to start the bot"""
    logging.info("Starting bot...")
    
    # Create and start web server for health checks
    app = await create_app()
    runner = web.AppRunner(app)
    await runner.setup()
    
    port = int(os.getenv('PORT', 8080))
    site = web.TCPSite(runner, '0.0.0.0', port)
    
    try:
        # Start web server
        await site.start()
        logging.info(f"Health check server started on port {port}")
        
        # Start bot polling
        await dp.start_polling(bot)
    finally:
        await runner.cleanup()
        await bot.session.close()

if __name__ == '__main__':
    asyncio.run(main())

