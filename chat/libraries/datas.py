"""Data Keys

Data keys are prefixed with the context - intent, message - in which they
are captured, and postfixed by its type. I.e.,

<Intent Key>__<Message Key>__<Data Name>__<Data Type>

E.g.,

NEW_SUPPLY__SUPPLY__GET_PRODUCT__PRODUCT_TYPE__STRING
"""

UNKNOWN = 'UNKNOWN' # Unknown data

# New Supply, Get Product
NEW_SUPPLY__SUPPLY__GET_PRODUCT__PRODUCT_TYPE__STRING = 'NEW_SUPPLY__SUPPLY__GET_PRODUCT__PRODUCT_TYPE__STRING' # Product type string

# New Supply, Get Availability
NEW_SUPPLY__SUPPLY__GET_AVAILABILITY__AVAILABILITY__CHOICE = 'NEW_SUPPLY__SUPPLY__GET_AVAILABILITY__AVAILABILITY__CHOICE' # Availability choice
## Options for choice
NEW_SUPPLY__SUPPLY__GET_AVAILABILITY__AVAILABILITY__READY_OTG = 'NEW_SUPPLY__SUPPLY__GET_AVAILABILITY__AVAILABILITY__READY_OTG' # Choose ready/OTG
NEW_SUPPLY__SUPPLY__GET_AVAILABILITY__AVAILABILITY__PRE_ORDER = 'NEW_SUPPLY__SUPPLY__GET_AVAILABILITY__AVAILABILITY__PRE_ORDER' # Choose pre-order

# New Supply, Get Country/State
NEW_SUPPLY__SUPPLY__GET_COUNTRY_STATE__COUNTRY_STATE__STRING = 'NEW_SUPPLY__SUPPLY__GET_COUNTRY_STATE__COUNTRY_STATE__STRING' # Country/State string

# New Supply, Get Packing
NEW_SUPPLY__SUPPLY__GET_PACKING__PACKING__STRING = 'NEW_SUPPLY__SUPPLY__GET_PACKING__PACKING__STRING' # Packing string

# New Supply, Get Quantity, Ready/OTG, Known Packing
NEW_SUPPLY__SUPPLY__GET_QUANTITY_READY_OTG_KNOWN_PACKING__QUANTITY__STRING = 'NEW_SUPPLY__SUPPLY__GET_QUANTITY_READY_OTG_KNOWN_PACKING__QUANTITY__STRING' # Quantity string

# New Supply, Get Quantity, Ready/OTG, Unknown Packing
NEW_SUPPLY__SUPPLY__GET_QUANTITY_READY_OTG_UNKNOWN_PACKING__QUANTITY__STRING = 'NEW_SUPPLY__SUPPLY__GET_QUANTITY_READY_OTG_UNKNOWN_PACKING__QUANTITY__STRING' # Quantity string

# New Supply, Get Quantity, Pre-Order
NEW_SUPPLY__SUPPLY__GET_QUANTITY_PREORDER__QUANTITY__STRING = 'NEW_SUPPLY__SUPPLY__GET_QUANTITY_PREORDER__QUANTITY__STRING' # Quantity string

# New Supply, Get Price, Ready/OTG, Known Packing
NEW_SUPPLY__SUPPLY__GET_PRICE_READY_OTG_KNOWN_PACKING__PRICE__STRING = 'NEW_SUPPLY__SUPPLY__GET_PRICE_READY_OTG_KNOWN_PACKING__PRICE__STRING' # Price string

# New Supply, Get Price, Ready/OTG, Unknown Packing
NEW_SUPPLY__SUPPLY__GET_PRICE_READY_OTG_UNKNOWN_PACKING__PRICE__STRING = 'NEW_SUPPLY__SUPPLY__GET_PRICE_READY_OTG_UNKNOWN_PACKING__PRICE__STRING' # Price string

# New Supply, Get Price, Pre-Order
NEW_SUPPLY__SUPPLY__GET_PRICE_PREORDER__PRICE__STRING = 'NEW_SUPPLY__SUPPLY__GET_PRICE_PREORDER__PRICE__STRING' # Price string

# New Supply, Get Deposit
NEW_SUPPLY__SUPPLY__GET_DEPOSIT__DEPOSIT__NUMBER = 'NEW_SUPPLY__SUPPLY__GET_DEPOSIT__DEPOSIT__NUMBER' # Deposit percentage number

# New Supply, Get Accept LC
NEW_SUPPLY__SUPPLY__GET_ACCEPT_LC__ACCEPT_LC__CHOICE = 'NEW_SUPPLY__SUPPLY__GET_ACCEPT_LC__ACCEPT_LC__CHOICE' # Accept LC choice
## Options for choice
NEW_SUPPLY__SUPPLY__GET_ACCEPT_LC__ACCEPT_LC__YES = 'NEW_SUPPLY__SUPPLY__GET_ACCEPT_LC__ACCEPT_LC__YES' # Accept LC
NEW_SUPPLY__SUPPLY__GET_ACCEPT_LC__ACCEPT_LC__NO = 'NEW_SUPPLY__SUPPLY__GET_ACCEPT_LC__ACCEPT_LC__NO' # Do not accept LC

# New Demand, Get Product
NEW_DEMAND__DEMAND__GET_PRODUCT__PRODUCT_TYPE__STRING = 'NEW_DEMAND__DEMAND__GET_PRODUCT__PRODUCT_TYPE__STRING' # Product type string

# New Demand, Get Country/State
NEW_DEMAND__DEMAND__GET_COUNTRY_STATE__COUNTRY_STATE__STRING = 'NEW_DEMAND__DEMAND__GET_COUNTRY_STATE__COUNTRY_STATE__STRING' # Country state string

# New Demand, Get Quantity, Known Product
NEW_DEMAND__DEMAND__GET_QUANTITY_KNOWN_PRODUCT_TYPE__QUANTITY__NUMBER = 'NEW_DEMAND__DEMAND__GET_QUANTITY_KNOWN_PRODUCT_TYPE__QUANTITY__NUMBER' # Quantity number

# New Demand, Get Quantity, Unknown Product
NEW_DEMAND__DEMAND__GET_QUANTITY_UNKNOWN_PRODUCT_TYPE__QUANTITY__STRING = 'NEW_DEMAND__DEMAND__GET_QUANTITY_UNKNOWN_PRODUCT_TYPE__QUANTITY__STRING' # Quantity string

# Choices for model fields
# Note: remember to makemigrations when updating this list
choices = [
    (UNKNOWN, UNKNOWN),
    (NEW_SUPPLY__SUPPLY__GET_PRODUCT__PRODUCT_TYPE__STRING, NEW_SUPPLY__SUPPLY__GET_PRODUCT__PRODUCT_TYPE__STRING),
    (NEW_SUPPLY__SUPPLY__GET_AVAILABILITY__AVAILABILITY__CHOICE, NEW_SUPPLY__SUPPLY__GET_AVAILABILITY__AVAILABILITY__CHOICE),
    (NEW_SUPPLY__SUPPLY__GET_AVAILABILITY__AVAILABILITY__READY_OTG, NEW_SUPPLY__SUPPLY__GET_AVAILABILITY__AVAILABILITY__READY_OTG),
    (NEW_SUPPLY__SUPPLY__GET_AVAILABILITY__AVAILABILITY__PRE_ORDER, NEW_SUPPLY__SUPPLY__GET_AVAILABILITY__AVAILABILITY__PRE_ORDER),
    (NEW_SUPPLY__SUPPLY__GET_COUNTRY_STATE__COUNTRY_STATE__STRING, NEW_SUPPLY__SUPPLY__GET_COUNTRY_STATE__COUNTRY_STATE__STRING),
    (NEW_SUPPLY__SUPPLY__GET_PACKING__PACKING__STRING, NEW_SUPPLY__SUPPLY__GET_PACKING__PACKING__STRING),
    (NEW_SUPPLY__SUPPLY__GET_QUANTITY_READY_OTG_KNOWN_PACKING__QUANTITY__STRING, NEW_SUPPLY__SUPPLY__GET_QUANTITY_READY_OTG_KNOWN_PACKING__QUANTITY__STRING),
    (NEW_SUPPLY__SUPPLY__GET_QUANTITY_READY_OTG_UNKNOWN_PACKING__QUANTITY__STRING, NEW_SUPPLY__SUPPLY__GET_QUANTITY_READY_OTG_UNKNOWN_PACKING__QUANTITY__STRING),
    (NEW_SUPPLY__SUPPLY__GET_QUANTITY_PREORDER__QUANTITY__STRING, NEW_SUPPLY__SUPPLY__GET_QUANTITY_PREORDER__QUANTITY__STRING),
    (NEW_SUPPLY__SUPPLY__GET_PRICE_READY_OTG_KNOWN_PACKING__PRICE__STRING, NEW_SUPPLY__SUPPLY__GET_PRICE_READY_OTG_KNOWN_PACKING__PRICE__STRING),
    (NEW_SUPPLY__SUPPLY__GET_PRICE_READY_OTG_UNKNOWN_PACKING__PRICE__STRING, NEW_SUPPLY__SUPPLY__GET_PRICE_READY_OTG_UNKNOWN_PACKING__PRICE__STRING),
    (NEW_SUPPLY__SUPPLY__GET_PRICE_PREORDER__PRICE__STRING, NEW_SUPPLY__SUPPLY__GET_PRICE_PREORDER__PRICE__STRING),
    (NEW_SUPPLY__SUPPLY__GET_DEPOSIT__DEPOSIT__NUMBER, NEW_SUPPLY__SUPPLY__GET_DEPOSIT__DEPOSIT__NUMBER),
    (NEW_SUPPLY__SUPPLY__GET_ACCEPT_LC__ACCEPT_LC__CHOICE, NEW_SUPPLY__SUPPLY__GET_ACCEPT_LC__ACCEPT_LC__CHOICE),
    (NEW_SUPPLY__SUPPLY__GET_ACCEPT_LC__ACCEPT_LC__YES, NEW_SUPPLY__SUPPLY__GET_ACCEPT_LC__ACCEPT_LC__YES),
    (NEW_SUPPLY__SUPPLY__GET_ACCEPT_LC__ACCEPT_LC__NO, NEW_SUPPLY__SUPPLY__GET_ACCEPT_LC__ACCEPT_LC__NO),
    (NEW_DEMAND__DEMAND__GET_PRODUCT__PRODUCT_TYPE__STRING, NEW_DEMAND__DEMAND__GET_PRODUCT__PRODUCT_TYPE__STRING),
    (NEW_DEMAND__DEMAND__GET_COUNTRY_STATE__COUNTRY_STATE__STRING, NEW_DEMAND__DEMAND__GET_COUNTRY_STATE__COUNTRY_STATE__STRING),
    (NEW_DEMAND__DEMAND__GET_QUANTITY_KNOWN_PRODUCT_TYPE__QUANTITY__NUMBER, NEW_DEMAND__DEMAND__GET_QUANTITY_KNOWN_PRODUCT_TYPE__QUANTITY__NUMBER),
    (NEW_DEMAND__DEMAND__GET_QUANTITY_UNKNOWN_PRODUCT_TYPE__QUANTITY__STRING, NEW_DEMAND__DEMAND__GET_QUANTITY_UNKNOWN_PRODUCT_TYPE__QUANTITY__STRING)
]