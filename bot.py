import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)
TOKEN = os.getenv("TOKEN")

questions = [
    {
        "question": "🌍 Какая планета третья от Солнца?",
        "options": ["Марс", "Венера", "Земля"],
        "answer_index": 2
    },
    {
        "question": "💧 Сколько водородов в молекуле воды?",
        "options": ["1", "2", "3"],
        "answer_index": 1
    },
    {
        "question": "⚡ Кто изобрёл лампочку?",
        "options": ["Эдисон", "Ньютон", "Эйнштейн"],
        "answer_index": 0
    },
    {
        "question": "🧬 Сколько хромосом у человека?",
        "options": ["46", "44", "48"],
        "answer_index": 0
    }
]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [
            InlineKeyboardButton("📌 Информация", callback_data='info'),
            InlineKeyboardButton("🧠 Викторина", callback_data='quiz'),
            InlineKeyboardButton("🛠 Поддержка", callback_data='support'),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Привет! Что ты хочешь сделать?", reply_markup=reply_markup)

async def go_back(query):
    keyboard = [
        [
            InlineKeyboardButton("📌 Информация", callback_data='info'),
            InlineKeyboardButton("🧠 Викторина", callback_data='quiz'),
            InlineKeyboardButton("🛠 Поддержка", callback_data='support'),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text("Ты вернулся в главное меню:", reply_markup=reply_markup)

async def send_question(query, context):
    index = context.user_data.get("quiz_index", 0)
    if index >= len(questions):
        score = context.user_data.get("score", 0)
        await query.edit_message_text("🎉 Викторина окончена! Молодец.")
await query.edit_message_text(f"Ты набрал {score} из {len(questions)} баллов.")
        return

    q = questions[index]
    keyboard = [
        [InlineKeyboardButton(f"A. {q['options'][0]}", callback_data='0')],
        [InlineKeyboardButton(f"B. {q['options'][1]}", callback_data='1')],
        [InlineKeyboardButton(f"C. {q['options'][2]}", callback_data='2')],
        [InlineKeyboardButton("🔙 Назад", callback_data='back')],
    ]
    await query.edit_message_text(q['question'], reply_markup=InlineKeyboardMarkup(keyboard))

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == 'info':
        keyboard = [[InlineKeyboardButton("🔙 Назад", callback_data='back')]]
        await query.edit_message_text("Приветствую! Я бот Ergo. Пока я могу предложить небольшую викторину.", reply_markup=InlineKeyboardMarkup(keyboard))

    elif data == 'support':
        keyboard = [[InlineKeyboardButton("🔙 Назад", callback_data='back')]]
        await query.edit_message_text("Если у вас есть замечания или вопросы, пишите: @kutukanas", reply_markup=InlineKeyboardMarkup(keyboard))

    elif data == 'back':
        await go_back(query)

    elif data == 'quiz':
        context.user_data["quiz_index"] = 0
        context.user_data["score"] = 0
        await send_question(query, context)

    elif data in ['0', '1', '2']:
        index = context.user_data.get("quiz_index", 0)
        question = questions[index]
        correct = int(data) == question['answer_index']
        if correct:
            context.user_data["score"] = context.user_data.get("score", 0) + 1
        text = "✅ Верно!" if correct else f"❌ Неверно. Правильный ответ: {question['options'][question['answer_index']]}"
        context.user_data["quiz_index"] += 1
        keyboard = [[InlineKeyboardButton("▶️ Далее", callback_data='next')]]
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard))

    elif data == 'next':
        await send_question(query, context)

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.run_polling()
