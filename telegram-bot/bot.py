import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

load_dotenv()

#Commands
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):    
    user_id = update.effective_user.id
    if str(user_id) not in allowed_username:
        await update.message.reply_text("🚫 You are not authorized.")
        return    
    user_name = update.effective_user.first_name or "there"
    await update.message.reply_text(
        f"Hi {user_name}! Welcome to the Weight Tracker Bot!\n\n"
        "Commands:\n"
        "• /update - Add new weight entry\n"
        "• /view - View your progress\n"
        "• /help - Show all commands" 
    )

if __name__ == '__main__': 
    print("🤖 Weight Tracker Bot is starting...")
    token = os.getenv("TOKEN")
    allowed_username = os.getenv("TELEGRAM_USER_ID")
    app = Application.builder().token(token).build()

    #Commands
    app.add_handler(CommandHandler("start", start_command))

    print('Polling...')
    app.run_polling(poll_interval=5)