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

DO_NOT_UNDERSTAND_NUMBER = \
"""Sorry I do not understand.

Please enter a number."""

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

NEW_SUPPLY__SUPPLY__GET_COUNTRY_STATE_READY_OTG = \
"""Which country/state is your goods in?"""

NEW_SUPPLY__SUPPLY__GET_COUNTRY_STATE_PRE_ORDER = \
"""Which country/state is your goods from?"""

NEW_SUPPLY__SUPPLY__GET_PACKING = \
"""Please describe packing.

E.g., 100 pieces in 1 box."""

NEW_SUPPLY__SUPPLY__CONFIRM_PACKING = \
"""Is this packing correct?

200 pieces in 1 box

*Reply*:
1. Yes
2. No"""

NEW_SUPPLY__SUPPLY__GET_QUANTITY_READY_OTG_KNOWN_PACKING = \
"""How many cartons can you supply ready-stock/OTG?"""

NEW_SUPPLY__SUPPLY__GET_QUANTITY_READY_OTG_UNKNOWN_PACKING = \
"""How much quantity can you supply ready-stock/OTG?

E.g., 300 boxes"""

NEW_SUPPLY__SUPPLY__GET_QUANTITY_PRE_ORDER = \
"""*Pre-order*: how much *quantity* and in what *timeframe* can you supply?

E.g., 10000 boxes a month"""

NEW_SUPPLY__SUPPLY__GET_PRICE_READY_OTG_KNOWN_PACKING = \
"""Ready-stock/OTG price per carton?

E.g., USD 20"""

NEW_SUPPLY__SUPPLY__GET_PRICE_READY_OTG_UNKNOWN_PACKING = \
"""Ready-stock/OTG price?

E.g., USD 20 per box"""

NEW_SUPPLY__SUPPLY__THANK_YOU = \
"""Thank you.

We'll contact our buyers and get back to you.

*Reply*:
1. Find buyers
2. Find sellers
3. Learn more about our service"""

NEW_SUPPLY__SUPPLY__GET_PRICE_PRE_ORDER = \
"""Ex-works (EXW) price per box?

E.g., USD 20 per box"""

NEW_SUPPLY__SUPPLY__GET_DEPOSIT = \
"""What % deposit do you require?

Reply '0' if no deposit required."""

NEW_SUPPLY__SUPPLY__GET_ACCEPT_LC = \
"""Do you accept LC?

*Reply*:
1. Yes
2. No"""

NEW_DEMAND__DEMAND__GET_QUANTITY_KNOWN_PRODUCT_TYPE = \
"""200 jams in 1 jar

How many jars do you need?"""

NEW_DEMAND__DEMAND__GET_QUANTITY_UNKNOWN_PRODUCT_TYPE = \
"""How much quantity do you need?"""

NEW_DEMAND__DEMAND__GET_PRICE_KNOWN_PRODUCT_TYPE = \
"""Target price per jar?

E.g., USD 20

Reply 'none' if no target price."""

NEW_DEMAND__DEMAND__THANK_YOU = \
"""Thank you.

We'll contact our sellers and get back to you.

*Reply*:
1. Find buyers
2. Find sellers
3. Learn more about our service"""

NEW_DEMAND__DEMAND__GET_PRICE_UNKNOWN_PRODUCT_TYPE = \
"""Target price?

E.g., USD 20 per box

Reply 'none' if no target price."""

REGISTER__REGISTER__GET_NAME = \
"""Thanks for contacting Everybase.

May we know your name?"""

DISCUSS_W_BUYER__SUPPLY__GET_AVAILABILITY = \
"""Availability?

1. Ready-Stock / On-the-Ground (OTG)
2. Pre-order"""

DISCUSS_W_BUYER__SUPPLY__GET_COUNTRY_STATE_READY_OTG = \
"""Which country/state is your goods in?"""

DISCUSS_W_BUYER__SUPPLY__GET_COUNTRY_STATE_PRE_ORDER = \
"""Which country/state is your goods from?"""

DISCUSS_W_BUYER__SUPPLY__CONFIRM_PACKING = \
"""Is this packing correct?

200 pieces in 1 box

*Reply*:
1. Yes
2. No"""

DISCUSS_W_BUYER__SUPPLY__GET_PACKING = \
"""Please describe packing.

E.g., 100 pieces in 1 box."""

DISCUSS_W_BUYER__SUPPLY__GET_QUANTITY_READY_OTG_KNOWN_PACKING = \
"""How many cartons can you supply ready-stock/OTG?"""

DISCUSS_W_BUYER__SUPPLY__GET_QUANTITY_READY_OTG_UNKNOWN_PACKING = \
"""How much quantity can you supply ready-stock/OTG?

E.g., 300 boxes"""

DISCUSS_W_BUYER__SUPPLY__GET_QUANTITY_PRE_ORDER = \
"""*Pre-order*: how much *quantity* and in what *timeframe* can you supply?

E.g., 10000 boxes a month"""

DISCUSS_W_BUYER__SUPPLY__THANK_YOU = \
"""Thank you.

We'll contact our buyers and get back to you.

*Reply*:
1. Find buyers
2. Find sellers
3. Learn more about our service"""

DISCUSS_W_BUYER__SUPPLY__GET_PRICE_READY_OTG_KNOWN_PACKING = \
"""Ready-stock/OTG price per carton?

E.g., USD 20"""

DISCUSS_W_BUYER__SUPPLY__GET_PRICE_READY_OTG_UNKNOWN_PACKING = \
"""Ready-stock/OTG price?

E.g., USD 20 per box"""

DISCUSS_W_BUYER__SUPPLY__GET_PRICE_PRE_ORDER = \
"""Ex-works (EXW) price per box?

E.g., USD 20 per box"""

DISCUSS_W_BUYER__SUPPLY__GET_DEPOSIT = \
"""What % deposit do you require?

Reply '0' if no deposit required."""

DISCUSS_W_BUYER__SUPPLY__GET_ACCEPT_LC = \
"""Do you accept LC?

*Reply*:
1. Yes
2. No"""

DISCUSS_W_SELLER__DEMAND__GET_QUANTITY_KNOWN_PRODUCT_TYPE = \
"""200 jams in 1 jar

How many jars do you need?"""

DISCUSS_W_SELLER__DEMAND__GET_QUANTITY_UNKNOWN_PRODUCT_TYPE = \
"""How much quantity do you need?"""