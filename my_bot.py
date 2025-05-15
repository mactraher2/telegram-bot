from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters
import os

# --- Настройки ---
TOKEN = os.getenv("BOT_TOKEN")
ADMIN_USERNAME = "squezzzzzz"

# --- Каталог ---
catalog_items = [
    {
        "title": "🚶‍♀️ Прогулка на улице",
        "image": "walking.jpg",
        "caption": "ну чо погнали!\n\nЦена: 5 поцелуйчиков💋"
    },
    {
        "title": "🎬 Кино",
        "image": "cinema.jpg",
        "caption": "мммм, как интересноооо\n\nЦена: 6 поцелуйчиков💋"
    }
]

# --- Команда /start ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [
            InlineKeyboardButton("Catalog", callback_data="catalog"),
            InlineKeyboardButton("MyOffer", callback_data="myoffer")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    with open("start.jpg", "rb") as photo:
        await context.bot.send_photo(
            chat_id=update.effective_chat.id,
            photo=photo,
            caption="""У-У-У-А-А-А-А-А-А🦍\nДоброе утро Мартышка! Вас приветствует ГИД по развлечениям!

Сегодня (и навсегда) с вами основатель данного сервиса, спонсор ваших капризов, человек исполняющий желания,  амбассадор фирмы "Ммммативация есть всигдаааааааааа!", величайшииииий...... Эррррболллллл!🦁

В нашем сервисе вы можете выбрать чего вы желаете сегодня и как хотите провести день! Скорее торопитесь перейти к нашему каталогу! Ваш выбор будет неограничен! Если вы не найдете чего искали, выбирайте команду /myoffer и напишите чего вы хотите!

P.s. данный Бот работает исключительно в свободное время и в выходные, а также тогда, когда основатель в настроении, и его не обижают и не бьют...)""",
            reply_markup=reply_markup
        )

    try:
        await update.message.delete()
    except:
        pass

# --- Команда /help ---
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [
            InlineKeyboardButton("/start", callback_data="start"),
            InlineKeyboardButton("/myoffer", callback_data="myoffer"),
        ],
        [
            InlineKeyboardButton("/help", callback_data="help"),
            InlineKeyboardButton("/catalog", callback_data="catalog"),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    with open("help.jpg", "rb") as photo:
        await context.bot.send_photo(
            chat_id=update.effective_chat.id,
            photo=photo,
            caption="/start - У-У-У-А-А-А-А-А-А🦍\n/myoffer - добей меня, если сможешь!!! (шуткааааа)\n/help - ты уже здесь, не паникуй 😿\n/catalog - выбирай, что хочешь, бэйба😏",
            reply_markup=reply_markup
        )

    try:
        await update.message.delete()
    except:
        pass

# --- Команда /myoffer ---
async def myoffer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message if update.message else update.callback_query.message

    with open("offer.jpg", "rb") as photo:
        await context.bot.send_photo(
            chat_id=msg.chat_id,
            photo=photo,
            caption="Напиши чего ты хочешь, и я обязательно постараюсь выполнить твое.....желание....!"
        )

    context.user_data['awaiting_offer'] = True

    try:
        await msg.delete()
    except:
        pass

# --- Команда /catalog ---
async def catalog(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message if update.message else update.callback_query.message

    keyboard = [
        [InlineKeyboardButton(item["title"], callback_data=f"catalog_{i}")]
        for i, item in enumerate(catalog_items)
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await context.bot.send_message(
        chat_id=msg.chat_id,
        text="Выберите одно из развлечений ниже:",
        reply_markup=reply_markup
    )

    try:
        await msg.delete()
    except:
        pass

# --- Обработка нажатий кнопок ---
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "start":
        await start(update, context)
    elif query.data == "myoffer":
        await myoffer(update, context)
    elif query.data == "help":
        await help_command(update, context)
    elif query.data == "catalog":
        await catalog(update, context)
    elif query.data == "pay":
        await query.message.reply_text("Готово! Данная услуга вам обойдется в один очень долгий и очень страстный поцелуй с объятиями)")
    elif query.data.startswith("catalog_"):
        index = int(query.data.split("_")[1])
        item = catalog_items[index]

        with open(item["image"], "rb") as photo:
            await query.message.reply_photo(
                photo=photo,
                caption=item["caption"]
            )

        try:
            await query.message.delete()
        except:
            pass

# --- Обработка текстовых сообщений ---
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get('awaiting_offer'):
        user_text = update.message.text
        try:
            await update.message.delete()
        except:
            pass

        if update.effective_user.username != ADMIN_USERNAME:
            await context.bot.send_message(
                chat_id=f"@{ADMIN_USERNAME}",
                text=f"Новое желание от @{update.effective_user.username or update.effective_user.id}:\n{user_text}"
            )

        with open("pay.jpg", "rb") as photo:
            keyboard = [[InlineKeyboardButton("Оплатить...😏", callback_data="pay")]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await context.bot.send_photo(
                chat_id=update.effective_chat.id,
                photo=photo,
                reply_markup=reply_markup
            )

        context.user_data['awaiting_offer'] = False

# --- Запуск бота ---
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("help", help_command))
app.add_handler(CommandHandler("myoffer", myoffer))
app.add_handler(CommandHandler("catalog", catalog))
app.add_handler(CallbackQueryHandler(button))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

print("Бот запущен...")
app.run_polling()
