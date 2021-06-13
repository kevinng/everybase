"""Expected response body text to assert against.

We do not use the same rendering technique to produce expected response body
text, because then - if the rendering technique breaks, the test cases will not
be able to catch them.
"""

MENU__MENU = \
"""Hi Kevin Ng, Everybase can help you find buyers and sellers.

*Reply*:
1. Find buyers
2. Find sellers
3. Learn more about our service"""

DO_NOT_UNDERSTAND_OPTION = \
"""Sorry I do not understand.

Please enter a valid option."""

DISCUSS_W_SELLER__STILL_INTERESTED__CONFIRM = \
"""Are you still interested in nitrile gloves?

*Reply*:
1. Yes
2. No"""

DISCUSS_W_SELLER__DISCUSS__CONFIRM_DETAILS = \
"""*Your demand*:

Nitrile Gloves
Israel
12000 Boxes
200 pieces in 1 box
Target USD 15.15 per box

*Are your demand details correct?*
1. Yes
2. No"""

DISCUSS_W_SELLER__DISCUSS__ALREADY_CONNECTED__OTG = \
"""This seller is already connected with you.

*Seller's contacts*:

Test Seller
+234562345678901

Click this link to WhatsApp seller:
https://wa.me/234562345678901

*Supply details*:

Nitrile Gloves
Israel
OTG/Ready Stock
12000 Boxes
200 pieces in 1 box
USD 15.15 per box"""

DISCUSS_W_SELLER__DISCUSS__ALREADY_CONNECTED__PRE_ORDER_DURATION = \
"""This seller is already connected with you.

*Seller's contacts*:

Test Seller
+234562345678901

Click this link to WhatsApp seller:
https://wa.me/234562345678901

*Supply details*:

Nitrile Gloves
Israel
Pre-Order, 5 Days
Do not accept LC
40% Deposit
12000 Boxes
200 pieces in 1 box
USD 15.15 per box"""

DISCUSS_W_SELLER__DISCUSS__ALREADY_CONNECTED__PRE_ORDER_DEADLINE = \
"""This seller is already connected with you.

*Seller's contacts*:

Test Seller
+234562345678901

Click this link to WhatsApp seller:
https://wa.me/234562345678901

*Supply details*:

Nitrile Gloves
Israel
Pre-Order, by 5th February 2021
Do not accept LC
40% Deposit
12000 Boxes
200 pieces in 1 box
USD 15.15 per box"""

DISCUSS_W_SELLER__STILL_INTERESTED__THANK_YOU = \
"""OK.

Let us know if we may help you find buyers or sellers for other products.

*Reply*:
1. Find buyers
2. Find sellers
3. Learn more about our service"""

DEMAND__GET_PRODUCT = \
"""What do you want to buy?

Enter 1 item only.

E.g., nitrile gloves"""

SUPPLY__GET_PRODUCT = \
"""What do you sell?

Enter 1 item only.

E.g., nitrile gloves."""

EXPLAIN_SERVICE = \
"""Everybase helps you find sellers and buyers.

We charge a small connection fee.

When you select the option to connect with a seller/buyer we referred to you, you'd be sent a payment link.

On making payment, you'd receive the contact for the seller/buyer.

*Reply*:
1. Find buyers
2. Find sellers
3. Speak with an Everybase human agent"""

DISCUSS_W_SELLER__DISCUSS__ASK = \
"""Please enter any questions you have for the seller.

Reply 'none' if you have no questions."""

DISCUSS_W_SELLER__DEMAND__GET_COUNTRY_STATE = \
"""What is the destination country/state?"""

DISCUSS_W_SELLER__DISCUSS__THANK_YOU = \
"""Thanks. We'll keep you updated.

*Reply*:
1. Find buyers
2. Find sellers
3. Learn more about our service"""

NEW_SUPPLY__SUPPLY__GET_PRODUCT = \
"""What do you sell?

Enter 1 item only.

E.g., nitrile gloves."""

NEW_DEMAND__DEMAND__GET_PRODUCT = \
"""What do you want to buy?

Enter 1 item only.

E.g., nitrile gloves"""

EXPLAIN_SERVICE__EXPLAIN_SERVICE = \
"""Everybase helps you find sellers and buyers.

We charge a small connection fee.

When you select the option to connect with a seller/buyer we referred to you, you'd be sent a payment link.

On making payment, you'd receive the contact for the seller/buyer.

*Reply*:
1. Find buyers
2. Find sellers
3. Speak with an Everybase human agent"""

NEW_SUPPLY__SUPPLY__GET_AVAILABILITY = \
"""Availability?

1. Ready-Stock / On-the-Ground (OTG)
2. Pre-order"""

NEW_DEMAND__DEMAND__GET_COUNTRY_STATE = \
"""What is the destination country/state?"""