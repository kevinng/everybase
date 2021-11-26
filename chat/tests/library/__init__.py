"""Chat Testing Library

This module contains library code to support the automated testing of chatbots.

Sub-modules are defined in their respective files and then imported here.

We import sub-modules in this folder so we may import them without referencing
them directly. E.g.,

Instead of:
from chat.tests.lib.chat_test import ChatTest
from chat.tests.lib.get_target_message_body import get_target_message_body

We can do:
from chat.tests.lib import ChatTest, get_target_message_body
"""

from .chat_test import ChatTest
from .get_target_message_body import get_target_message_body