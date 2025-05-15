from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto
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
    },
    {
        "title": "🤗 Обнимашки дома",
        "image": "home.jpg",
        "caption": "Це шо ТаймСквэр\n\nЦена: 3 поцелуйчика💋"
    },
    {
        "title": "🍽️ Пойти в ррресторранн",
        "image": "restaurant.jpg",
        "caption": "ну ты губу то раскатала бом-бом\n(по особым случаям)\n\nЦена: 10 поцелуйчиков💋"
    },
    {
        "title": "🎭 Театр",
        "image": "teatr.jpg",
        "caption": "вам кофе с сахаром или с моими ....\n(по особым случаям)\n\nЦена: 15 поцелуйчиков💋"
    },
    {
        "title": "🧹 Уборка дома",
        "image": "clining.jpg",
        "caption": "хи-хи-хи-ХА-ХА-ХА-ХА\n\nЦена: БЕСПЛАТНО"
    },
    {
        "title": "🚴 Покатушки на великах",
        "image": "bicycle.jpg",
        "caption": "А начиналось так красииивааа....\n\nЦена: 5 поцелуйчиков💋"
    },
    {
        "title": "🐠 Музеи, океанариумы, зоопарки, гончарка",
        "image": "zoo.jpg",
        "caption": "жизнь это вызов - я бы пропустил звонок\n(по особым случаям)\n\nЦена: 15 поцелуйчиков💋"
    },
    {
        "title": "🍾 Приготовлю завтрак",
        "image": "breakfast.jpg",
        "caption": "я в прошлой жизни тот еще повар😎\n(по особым случаям)\n\nЦена: 15 поцелуйчиков💋"
    },
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

Сегодня (и навсегда) с вами основатель данного сервиса, спонсор ваших капризов, человек исполняющий желания,  амбассадор фирмы \"Ммммативация есть всигдаааааааааа!\", величайшииииий...... Эррррболллллл!🦁

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
    keyboard.append([InlineKeyboardButton("ЭТО МОЙ ВЫБОР", callback_data="pay")])
    reply_markup = InlineKeyboardMarkup(keyboard)

    item = catalog_items[0]
    with open(item["image"], "rb") as photo:
        await context.bot.send_photo(
            chat_id=msg.chat_id,
            photo=photo,
            caption=item["caption"],
            reply_markup=reply_markup
        )

    context.user_data['selected_item'] = catalog_items[0]

    try:
        await msg.delete()
    except:
        pass

# --- Обработка кнопок ---
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

    elif query.data.startswith("catalog_"):
        index = int(query.data.split("_")[1])
        item = catalog_items[index]
        context.user_data['selected_item'] = item

        keyboard = [
            [InlineKeyboardButton(i["title"], callback_data=f"catalog_{idx}")]
            for idx, i in enumerate(catalog_items)
        ]
        keyboard.append([InlineKeyboardButton("ЭТО МОЙ ВЫБОР", callback_data="pay")])
        reply_markup = InlineKeyboardMarkup(keyboard)

        with open(item["image"], "rb") as photo:
            await query.message.edit_media(
                media=InputMediaPhoto(media=photo, caption=item["caption"]),
                reply_markup=reply_markup
            )

    elif query.data == "pay":
        with open("pay.jpg", "rb") as photo:
            keyboard = [[InlineKeyboardButton("Оплатить...😏", callback_data="do_pay")]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.message.edit_media(
                media=InputMediaPhoto(media=photo),
                reply_markup=reply_markup
            )

    elif query.data == "do_pay":
        selected = context.user_data.get('selected_item')
        if selected:
            price_line = selected["caption"].split("\n")[-1]
            await query.message.edit_text(
                text="Готово! Данная услуга вам обойдется в один очень долгий и очень страстный поцелуй с объятиями"
            )

            user = update.effective_user
            await context.bot.send_message(
                chat_id=f"@{ADMIN_USERNAME}",
                text=f"📩 Новый выбор из каталога!\n"
                     f"Пользователь: @{user.username or user.id}\n"
                     f"Выбрал: {selected['title']}\n"
                     f"{price_line}"
            )
        else:
            await query.message.edit_text("Ошибка: услуга не выбрана.")

# --- Обработка текста ---
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

# --- Запуск ---
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("help", help_command))
app.add_handler(CommandHandler("myoffer", myoffer))
app.add_handler(CommandHandler("catalog", catalog))
app.add_handler(CallbackQueryHandler(button))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

print("Бот запущен...")
app.run_polling()
