import telebot
import sqlite3

connection = sqlite3.connect( "survey.db" )
cursor = connection.cursor()

questions = []
types = []
answers = []

with connection :
    cursor.execute( "SELECT * FROM survey" )
    rows = cursor.fetchall()

    for row in rows :
        questions.append( row[1] )
        types.append( row[2] )

print( questions )

bot = telebot.TeleBot( "1452807594:AAE9pnSEejG4Ur0MbjmHv1xrvNZCAcIAlYo" )

@bot.message_handler( content_types = [ 'text' ] )

def survey( message ) :
    for question in questions :
        bot.send_message( message.chat.id, question )
        answers.append( message.text )
        print( answers )

    bot.stop_polling()

bot.polling()
