from Website.website import McGraw

with McGraw() as bot:
    bot.quizletLogin("EMAIL HERE", "PASS HERE", timeout=2)
    bot.mcGrawLogin("EMAIL HERE", "PASS HERE", timeout=2)
    bot.startAssignment()
    bot.startQuestions(7)
    bot.closePopup(2)
    while True:
        try:
            bot.questionFind()
            bot.searchOnGoogle()
            bot.getAnswer2()
        finally:
            bot.switch_to.window(bot.connectTab)
