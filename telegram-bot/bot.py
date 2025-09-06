import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler
from datetime import datetime
from google.cloud import bigquery


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
        "• /delete - Delete weight entry\n"
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
        date = datetime.strptime(date_text, '%Y-%m-%d').date()
        context.user_data['selected_date'] = date

        await update.message.reply_text(
            f"Date {date} selected.\nNow please enter your weight (in kg):"
        )
        return ENTER_WEIGHT
        
    except ValueError:
        await update.message.reply_text(
            "Invalid date format. Please use YYYY-MM-DD format:"
        )
        return CHOOSE_DATE

async def weight_received(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    try:
        weight = float(update.message.text.replace(',', '.'))
        date = context.user_data['selected_date']

        try:
            await process_weight_data(date, weight)
            await update.message.reply_text(
                f"✅ Done! Weight {weight}kg recorded for {date}."
            )
            
            # Clear user data
            context.user_data.clear()
            return ConversationHandler.END
            
        except Exception as e:
            await update.message.reply_text(
                f"❌ Error uploading data: Something went wrong. Please try again later.\n"
                f"Error details: {str(e)}"
            )
            # Cancel conversation on error
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

async def process_weight_data(date, weight):
    """
    Process and store weight data for a given user
    
    Args:
        date: Date of the weight measurement
        weight: Weight in kg
        user_id: Telegram user ID
    """
    client = bigquery.Client.from_service_account_json('gcp_service_account_key.json')

    full_table_id = f"{dataset_id}.{table_id}"

    row = {
        "date": date.isoformat(),
        "weight": weight
    }

    try:
        errors = client.insert_rows_json(
            full_table_id, 
            [row]
        )
        if errors:
            print(f"Encountered errors while inserting row: {errors}")
            raise Exception("Failed to insert data into BigQuery")

    except Exception as e:
        print(f"Error inserting data into BigQuery: {str(e)}")
        raise

if __name__ == '__main__':
    
    print("🤖 Weight Tracker Bot is starting...")

    #get env variables
    token = os.getenv("TOKEN")
    allowed_username = os.getenv("TELEGRAM_USER_ID")
    dataset_id = os.getenv("DATASET_NAME")
    table_id = os.getenv("TABLE_NAME")


    app = Application.builder().token(token).build()

    #Commands
    app.add_handler(CommandHandler("start", start_command))

    #Handlers
    app.add_handler(conv_handler)

    print('Polling...')
    app.run_polling(poll_interval=5)