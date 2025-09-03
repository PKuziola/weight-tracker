import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler


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

# Define conversation states
CHOOSE_DATE, ENTER_WEIGHT = range(2)

async def start_update(update: Update, context: ContextTypes.DEFAULT_TYPE):    
    await update.message.reply_text(
        "Please choose a date (format: YYYY-MM-DD):"
    )
    return CHOOSE_DATE

async def date_received(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:  
    date_text = update.message.text
    
    try:
        # Validate date format #TODO: Implement validation

        context.user_data['selected_date'] = date_text
        
        await update.message.reply_text(
            f"Date {date_text} selected.\nNow please enter your weight (in kg):"
        )
        return ENTER_WEIGHT
        
    except ValueError:
        await update.message.reply_text(
            "Invalid date format. Please use YYYY-MM-DD format:"
        )
        return CHOOSE_DATE

async def weight_received(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    try:
        weight = float(update.message.text) #TODO: Validate weight format
        date = context.user_data['selected_date']   

        #await process_weight_data(date, weight, update.effective_user.id) #TODO: Implement this function
        
        await update.message.reply_text(
            f"✅ Done! Weight {weight}kg recorded for {date}."
        )
        
        # Clear user data
        context.user_data.clear()
        return ConversationHandler.END
        
    except ValueError:
        await update.message.reply_text(
            "Please enter a valid number for weight:"
        )
        return ENTER_WEIGHT

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancel the conversation"""
    await update.message.reply_text("Operation cancelled.")
    context.user_data.clear()
    return ConversationHandler.END

conv_handler = ConversationHandler(
    entry_points=[CommandHandler('update', start_update)],
    states={
        CHOOSE_DATE: [MessageHandler(filters.TEXT & ~filters.COMMAND, date_received)],
        ENTER_WEIGHT: [MessageHandler(filters.TEXT & ~filters.COMMAND, weight_received)],
    },
    fallbacks=[CommandHandler('cancel', cancel)],
)

if __name__ == '__main__':
    
    print("🤖 Weight Tracker Bot is starting...")

    token = os.getenv("TOKEN")
    allowed_username = os.getenv("TELEGRAM_USER_ID")
    app = Application.builder().token(token).build()

    #Commands
    app.add_handler(CommandHandler("start", start_command))

    #Handlers
    app.add_handler(conv_handler)

    print('Polling...')
    app.run_polling(poll_interval=5)