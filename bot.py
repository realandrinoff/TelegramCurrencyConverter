import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, ConversationHandler, MessageHandler, filters
from rate import convert
import decimal



# This part is responsible for logging so we wouldnt skip code errors
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# fsfsdf
while True:
    AMOUNT, CURRENCY1, CURRENCY2, EXCHANGE, ERROR = range(5)
    async def amount(update: Update, context: ContextTypes.DEFAULT_TYPE):

            amount1 = update.message.text
            print(amount1)
            context.user_data["amount"] = decimal(amount1)
            try:
                await update.message.reply_text('Now write the currency (e.g. usd, gel, eur)')
                return CURRENCY1
            except ValueError: 
                await update.message.reply_text("Error, write just the amount.") 
                await amount(update, context)
                


    async def currency1(update: Update, context: ContextTypes.DEFAULT_TYPE):
        currency_1 = update.message.text
        context.user_data["currency1"] = currency_1
        currency_1 = currency_1.strip().upper()
        print(currency_1)
        currency_1 = str(currency_1)
        try:
            if len(currency_1) == 3:
                await update.message.reply_text ('Write the currency you want ' + context.user_data["amount"] + context.user_data['currency1'] + ' in')
                return CURRENCY2
            else:
                await update.message.reply_text("Error, write just the currency! (It has to be 3 letters long) (e.g USD, GEL)") 
        except Exception:
            await update.message.reply_text("Error, try again through /exchange")
            await exchange(update, context)
        
        
    async def currency2(update: Update, context: ContextTypes.DEFAULT_TYPE):
        currency_2 = update.message.text
        currency_2 = currency_2.strip().upper()
        print(currency_2)
        context.user_data["currency2"] = currency_2
        currency_2 = str(currency_2)
        try:
            if len(currency_2) == 3:
                    finalresult = convert(context.user_data["amount"], context.user_data["currency1"], context.user_data["currency2"])
                    finalresult = str(finalresult)
                    await update.message.reply_text('Your rate for ' +context.user_data["amount"]+context.user_data["currency1"] + ' = '+ finalresult+ context.user_data["currency1"]+ '.\n\n\n\nThank you for using my service! \nType anything to proceed!\n\nCredits: @andrinoff')
                    return EXCHANGE
            else:
                await update.message.reply_text("Error, write just the currency! (It has to be 3 letters long) (e.g USD, GEL)") 
        except Exception:
            await update.message.reply_text("Error, try again through /exchange")
            await exchange(update, context)

        
    async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text ('An error encounted, reported \n You will start over')
        context.user_data['amount'] = None
        context.user_data['currency1']  = None
        context.user_data['currency2']  = None
        return EXCHANGE
    async def exchange(update: Update, context: ContextTypes.DEFAULT_TYPE):
        amount1 = None
        currency_1 = None
        currency_2 = None
        await update.message.reply_text('Write AMOUNT (e.g. 20)')

                
        return AMOUNT


    if __name__ == '__main__':
        application = ApplicationBuilder().token('7307380567:AAHrnAsxUxwlg7cXWGjFvwlBS_NmoyirJ4I').build()        
        exchange_handler = ConversationHandler(
            entry_points= [CommandHandler('exchange', exchange)],
                                        states = {
                                            AMOUNT: [
                                                MessageHandler(filters.TEXT, amount),
                                                
                                            ],
                                            CURRENCY1: [
                                                MessageHandler(filters.TEXT, currency1),
                                                
                                            ],
                                            CURRENCY2: [
                                                MessageHandler(filters.TEXT, currency2),
                                               
                                            ],
                                            EXCHANGE: [
                                                 MessageHandler(filters.TEXT, exchange)
                                            ],
                                            ERROR: [
                                                 MessageHandler(filters.TEXT, error)
                                            ]
                                        },
                                        fallbacks= [CommandHandler("exchange", exchange)],
        )
        application.add_handler(exchange_handler)
        application.run_polling()
