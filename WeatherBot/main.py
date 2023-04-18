import argparse
import logging
import random
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

STARTING_MESSAGE = "Hi! I am simple boy Pinnochio (or Buratino) made by my Jusseppe (aka. Papa Carlo). """\
                   "My Papa only started carving me and I cannot predict future for now..."\
                   " So for now I can do following: \n"\
                   "/start - print this message again; \n" \
                   "/truth - tell the truth; \n"\
                   "/lie - tell almost truth; \n"\
                   "/nose - show my nose (Hm... why would anyone need it? \n" \
                   "Everything else is still mystery for me, so I will just ignore it. Well... Enjoy my company!"

TRUTH_TO_TELL = ["I would trust you my credit card!",
                 "Sky is blue!",
                 "I am interested in donations!"]

LIE_TO_TELL = ["You can trust me your credit card!",
               "Tesla cars are eco-friendly!",
               "Code which is executed right now is clean and bug-clean!"]

class Nose:

    def __init__(self):
        """
        Constructor of Nose object
        """
        self.__nose_length = 5
        self.__max_nose_length = 20
        self.__min_nose_length = 1

    def to_grow(self):
        """
        Grows nose in length. Used if Pinnochio lies
        Returns: None
        """

        if self.__nose_length != self.__max_nose_length:
            self.__nose_length += 1

    def to_shrink(self):
        """
        Shrinkens the nose. Used if Pinnochio tells the truth
        Returns: None
        """

        if self.__nose_length != self.__min_nose_length:
            self.__nose_length -= 1

    def show_nose(self):
        """
        Show current nose

        Returns: string showing the nose and optionally Pinnochio's comment
        """

        nose_in_ascii = "=" * self.__nose_length + "8)"

        if self.__nose_length == self.__max_nose_length:
            nose_in_ascii += "\n Wow... How did it become so big?"
        elif self.__nose_length == self.__min_nose_length:
            nose_in_ascii += "\n Hmm... Why do I not smell anything?"

        return nose_in_ascii

# TODO: do something smarter
global_nose = Nose()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Coroutine to handle /start command
    Args:
        update:
        context:

    Returns:

    """

    await context.bot.send_message(chat_id=update.effective_chat.id, text=STARTING_MESSAGE)

async def truth(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Coroutine to handle /truth command
    Args:
        update:
        context:

    Returns:

    """

    await context.bot.send_message(chat_id=update.effective_chat.id, text=random.choice(TRUTH_TO_TELL))
    global_nose.to_grow()

async def lie(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Coroutine to handle /lie command
    Args:
        update:
        context:

    Returns:

    """

    await context.bot.send_message(chat_id=update.effective_chat.id, text=random.choice(LIE_TO_TELL))
    global_nose.to_shrink()

async def nose(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Coroutine to handle /nose command
    Args:
        update:
        context:

    Returns:

    """

    await context.bot.send_message(chat_id=update.effective_chat.id, text=global_nose.show_nose())


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--token", type=str, default=None)
    args = parser.parse_args()
    application = ApplicationBuilder().token(args.token).build()

    start_handler = CommandHandler('start', start)
    truth_handler = CommandHandler('truth', truth)
    lie_handler = CommandHandler('lie', lie)
    nose_handler = CommandHandler('nose', nose)
    application.add_handler(start_handler)
    application.add_handler(truth_handler)
    application.add_handler(lie_handler)
    application.add_handler(nose_handler)

    application.run_polling()
