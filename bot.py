import html
import os
from datetime import datetime, timezone

from telegram import (InlineKeyboardButton, InlineKeyboardMarkup,
                      LinkPreviewOptions, ReplyKeyboardMarkup, Update)
from telegram.constants import ParseMode
from telegram.ext import (Application, CallbackQueryHandler, CommandHandler,
                          ContextTypes, MessageHandler, filters)

TOKEN = os.environ["BOT_TOKEN"]
BOT_NAME = "SB24GZ Khmer"

BTN_DAILY = "ចំណេះដឹងប្រចាំថ្ងៃ"
BTN_TECH = "មគ្គុទ្ទេសក៍បច្ចេកវិទ្យា"
BTN_LEARN = "ធនធានសិក្សា"
BTN_HELP = "ជំនួយ"

MAIN_KEYBOARD = ReplyKeyboardMarkup(
    [[BTN_DAILY, BTN_TECH], [BTN_LEARN, BTN_HELP]], resize_keyboard=True
)

WELCOME = (
    f"សូមស្វាគមន៍មកកាន់ <b>{BOT_NAME}</b> ជាបូតផ្តល់ចំណេះដឹងជាភាសាខ្មែរ។\n\n"
    "អ្វីដែលអ្នកអាចធ្វើបាន៖\n"
    f"• {BTN_DAILY}៖ ការពិត ឬគន្លឹះខ្លីៗដែលមានប្រយោជន៍\n"
    f"• {BTN_TECH}៖ ពន្យល់អំពីកម្មវិធី និងឧបករណ៍ឌីជីថលទូទៅ\n"
    f"• {BTN_LEARN}៖ ព័ត៌មាន និងតំណសម្រាប់រៀន\n"
    f"• {BTN_HELP}៖ របៀបប្រើបូត\n\n"
    "សូមជ្រើសរើសពីម៉ឺនុយខាងក្រោម។"
)

HELP = (
    f"<b>{BOT_NAME}</b> | {BTN_HELP}\n\n"
    f"• {BTN_DAILY} បង្ហាញចំណេះដឹង ឬគន្លឹះមួយក្នុងមួយថ្ងៃ។\n"
    f"• {BTN_TECH} ពន្យល់ពីកម្មវិធីទូទៅ ដូចជា Telegram, Google Maps, Gmail "
    "និង Google Translate។\n"
    f"• {BTN_LEARN} បង្ហាញតំណសម្រាប់រៀន ជាមួយការពន្យល់ខ្លីៗ។\n\n"
    "វាយ /start ដើម្បីត្រឡប់ទៅម៉ឺនុយវិញ។"
)

DAILY = [
    "ប្រាសាទអង្គរវត្តស្ថិតនៅក្នុងខេត្តសៀមរាប ហើយជាប្រាសាទដ៏ធំមួយនៅលើពិភពលោក។",
    "បឹងទន្លេសាបគឺជាបឹងទឹកសាបធំជាងគេនៅអាស៊ីអាគ្នេយ៍។",
    "គន្លឹះសិក្សា៖ ត្រួតពិនិត្យមេរៀនម្តងទៀតក្នុងរយៈពេល ២៤ ម៉ោងបន្ទាប់ពីរៀន "
    "នឹងជួយឱ្យចងចាំបានល្អជាង។",
    "សុវត្ថិភាពឌីជីថល៖ កុំចែករំលែកលេខកូដ OTP ដែលទទួលបានតាមសារ ជាមួយអ្នកផ្សេង។",
    "អក្ខរក្រមខ្មែរមានព្យញ្ជនៈ ៣៣តួ។",
    "គន្លឹះការងារ៖ ចែកការងារធំជាភាគតូចៗ ហើយធ្វើម្តងមួយៗ "
    "ដើម្បីកាត់បន្ថយភាពតានតឹង។",
    "ទន្លេមេគង្គហូរកាត់ប្រទេសកម្ពុជាពីខាងជើងទៅខាងត្បូង។",
]

TECH = {
    "telegram": ("Telegram",
        "Telegram ជាកម្មវិធីផ្ញើសារ ដែលអនុញ្ញាតឱ្យអ្នកជជែក បង្កើតក្រុម "
        "និងតាមដានឆានែលព័ត៌មាន។\n\nគន្លឹះ៖ បើកការផ្ទៀងផ្ទាត់ពីរជាន់ "
        "(Two-Step Verification) ដើម្បីការពារគណនី។"),
    "maps": ("Google Maps",
        "Google Maps ជួយអ្នករកទីតាំង មើលផ្លូវ និងប៉ាន់ស្មានពេលវេលាធ្វើដំណើរ។"
        "\n\nគន្លឹះ៖ អ្នកអាចទាញយកផែនទីទុកប្រើពេលគ្មានអ៊ីនធឺណិត។"),
    "gmail": ("Gmail",
        "Gmail ជាសេវាអ៊ីមែលរបស់ Google សម្រាប់ផ្ញើ និងទទួលសារអេឡិចត្រូនិក។"
        "\n\nគន្លឹះ៖ ប្រើពាក្យសម្ងាត់ខ្លាំង ហើយកុំចុចតំណក្នុងអ៊ីមែលដែលមិនស្គាល់។"),
    "translate": ("Google Translate",
        "Google Translate ជួយបកប្រែអត្ថបទរវាងភាសាច្រើន រួមទាំងភាសាខ្មែរ។"
        "\n\nគន្លឹះ៖ ពិនិត្យលទ្ធផលម្តងទៀត ព្រោះការបកប្រែស្វ័យប្រវត្តិអាចមានកំហុស។"),
}

# (name, Khmer description, link)
RESOURCES = [
    ("Khan Academy",
     "វីដេអូមេរៀនគណិតវិទ្យា វិទ្យាសាស្ត្រ និងមុខវិជ្ជាផ្សេងៗ ជាភាសាអង់គ្លេស។",
     "https://www.khanacademy.org"),
    ("freeCodeCamp",
     "មេរៀនសរសេរកូដជាក់ស្តែង ជាភាសាអង់គ្លេស។",
     "https://www.freecodecamp.org"),
    ("Coursera",
     "វគ្គសិក្សាពីសាកលវិទ្យាល័យ និងស្ថាប័នជាច្រើន ជាភាសាអង់គ្លេស។",
     "https://www.coursera.org"),
    ("Wikipedia ភាសាខ្មែរ",
     "សព្វវចនាធិប្បាយសេរីជាភាសាខ្មែរ សម្រាប់អានស្វែងយល់ពីប្រធានបទផ្សេងៗ។",
     "https://km.wikipedia.org"),
]


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        WELCOME, parse_mode=ParseMode.HTML, reply_markup=MAIN_KEYBOARD)


async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        HELP, parse_mode=ParseMode.HTML, reply_markup=MAIN_KEYBOARD)


async def daily(update: Update, context: ContextTypes.DEFAULT_TYPE):
    day = datetime.now(timezone.utc).date().toordinal()
    text = DAILY[day % len(DAILY)]
    await update.message.reply_text(
        f"<b>{BOT_NAME}</b> | {BTN_DAILY}\n\n{html.escape(text)}",
        parse_mode=ParseMode.HTML)


async def tech_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    buttons = [[InlineKeyboardButton(title, callback_data=f"tech_{key}")]
               for key, (title, _) in TECH.items()]
    await update.message.reply_text(
        f"<b>{BOT_NAME}</b> | {BTN_TECH}\n\nសូមជ្រើសរើសកម្មវិធី៖",
        parse_mode=ParseMode.HTML,
        reply_markup=InlineKeyboardMarkup(buttons))


async def tech_item(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    title, text = TECH[query.data.split("_", 1)[1]]
    await query.message.reply_text(
        f"<b>{BOT_NAME}</b> | {html.escape(title)}\n\n{html.escape(text)}",
        parse_mode=ParseMode.HTML)


async def learn(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lines = [f"<b>{BOT_NAME}</b> | {BTN_LEARN}\n"]
    for name, desc, url in RESOURCES:
        lines.append(f'• <a href="{url}">{html.escape(name)}</a> - {html.escape(desc)}')
    await update.message.reply_text(
        "\n".join(lines),
        parse_mode=ParseMode.HTML,
        link_preview_options=LinkPreviewOptions(is_disabled=True))


async def fallback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"{BOT_NAME}៖ សូមជ្រើសរើសជម្រើសពីម៉ឺនុយខាងក្រោម។",
        reply_markup=MAIN_KEYBOARD)


def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(MessageHandler(filters.Text([BTN_DAILY]), daily))
    app.add_handler(MessageHandler(filters.Text([BTN_TECH]), tech_menu))
    app.add_handler(MessageHandler(filters.Text([BTN_LEARN]), learn))
    app.add_handler(MessageHandler(filters.Text([BTN_HELP]), help_cmd))
    app.add_handler(CallbackQueryHandler(tech_item, pattern="^tech_"))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, fallback))
    app.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    main()
