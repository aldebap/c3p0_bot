#!	/usr/bin/python3

################################################################################
#	test_c3p0_bot.py  -  Jan-28-2021 by aldebap
#
#	Unit tests for the Telegram c3po_bot
################################################################################

import unittest

from telegram.ext import CommandHandler
from telegram.utils.request import Request
from telegram.ext import Updater

from ptbtest import MessageGenerator
from ptbtest import Mockbot

import c3p0_bot

#   Unit tests class

class test_c3p0_bot( unittest.TestCase ):

    #   c3po_bot functions tests

    #   test help - 01. handle help command
    def test_help(self):
        #   create all required mock objects
        self.testBot = Mockbot()
        self.testBot.request = Request()
        self.testBot.defaults = {}
        self.testMsgGenerator = MessageGenerator(self.testBot)
        self.testUpdater = Updater(bot=self.testBot)

        #   add a handler for c3po help command
        self.testUpdater.dispatcher.add_handler(CommandHandler("help", help))
        self.testUpdater.start_polling()

        #   create a help message and send it to testBot
        helpMsg = self.testMsgGenerator.get_message(text="/help")
        self.testBot.insertUpdate( helpMsg )

        #   make sure only one message was sent to the testBot, and that is the expected one
        self.assertEqual(len(self.testBot.sent_messages), 1)
        #self.assertEqual(len(self.testBot._updates), 1)
        sentMsg = self.testBot.sent_messages[0]
        #sentMsg = self.testBot._updates[0]
        self.assertEqual(sentMsg['method'], "sendMessage")
        self.assertEqual(sentMsg['text'], "Help!")

        #   stop the testBot
        self.testUpdater.stop()

#	entry point

if __name__ == '__main__':
    unittest.main()
