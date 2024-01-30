from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from functions import *

TOKEN: Final = #BOT_TOKEN TO BE GENERATED FROM TELEGRAM
BOT_USERNAME: Final = #BOT_NAME TO BE CREATED IN TELEGRAM

# Commands
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello there, I am SUTD's personal Leetcode Bot\nI provide all information that you need for the Leetcode Challenge")
    await update.message.reply_text("Please use the readily available commands to navigate this bot")

async def register_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    input = str(update.message.text)
    words = input.split()
    if len(words) == 1:
        await update.message.reply_text("Please include your Leetcode Username in this format\n/register <username>")
    else:
        await update.message.reply_text("Please wait a moment...")
        output = filter(words[1:])
        text = '\n'.join(output)
        await update.message.reply_text(text)
    
async def leaderboard_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    month = datetime.now().strftime("%m-%y")
    datefile = '01-' + month + '.txt'
    await update.message.reply_text("Please wait a moment, this will take awhile approx. 2mins...")
    output = scoreboard(datefile)
    await update.message.reply_text(output)
    
async def myscore_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    input = str(update.message.text)
    words = input.split()
    if len(words) == 1:
        await update.message.reply_text("Please include your Leetcode Username in this format\n/myscore <username>")
    else:
        await update.message.reply_text("Please wait a moment...")
        month = datetime.now().strftime("%m-%y")
        datefile = '01-' + month + '.txt'
        output = mytally(words[1], datefile)
        await update.message.reply_text(output)

async def update_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Please wait a moment, this will take awhile approx. 2mins...")
    output = referencescore()
    await update.message.reply_text(output)

async def final_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Please wait a moment, this will take awhile approx. 2mins...")
    output = finalscore()
    await update.message.reply_text(output)

# Responses
def handle_response(text: str) -> str:
    return "I am not designed to converse\nPlease use the readily available commands to navigate this bot"

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text

    print(f'User({update.message.chat.id}) in {message_type}: "{text}"')

    if message_type == 'group':
        if BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME, '').strip()
            response: str = handle_response(new_text)
        else:
            return
    else:
        response: str = handle_response(text)
    
    print('Bot: ', response)
    await update.message.reply_text(response)

# Error
async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} cause error {context.error}')


# Main operational code
if __name__ == '__main__':
    print('Starting Bot...')
    app = Application.builder().token(TOKEN).build()
    
    # Commands
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('register', register_command))
    app.add_handler(CommandHandler('leaderboard', leaderboard_command))
    app.add_handler(CommandHandler('myscore', myscore_command))
    app.add_handler(CommandHandler('_update', update_command))
    app.add_handler(CommandHandler('_final', final_command))

    # Messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    # Error
    app.add_error_handler(error)

    # Polls the bot
    print('Polling...')
    app.run_polling(poll_interval=3)