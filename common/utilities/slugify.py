import random
from nltk.corpus import stopwords
from nltk import pos_tag, word_tokenize
from django.utils.text import slugify as django_slugify
from common.models import Country
from common.utilities.is_censored import _shareable_forbidden_words

def slugify(
        phrase,
        append_key,
        buy_country=None,
        sell_country=None,
        is_selling=None,
        country=None,
        is_buy_agent=None,
        is_sell_agent=None,
        is_logistics_agent=None
    ):
    """Generates and returns URL/SEO-friendly slug for phrase ending with
    append_key.
    
    buy_country, sell_country, is_selling provides model-specific
    variation for Lead model.

    country, is_buy_agent, is_sell_agent, is_logistics_agent provides
    model-specific variation for User model. User model phrase should be a
    concatenation of all details we want to use - e.g., goods/services, and
    other agent related details.
    """
    # Tokenize
    tokens = word_tokenize(phrase)

    # Use words > 3 characters long
    tokens = [t for t in tokens if len(t) > 3]

    # Use alpha words only
    tokens = [t for t in tokens if t.isalpha()]

    # Remove stop words
    tokens = [t for t in tokens if not t in stopwords.words()]

    # Remove custom lowercased stop words
    custom_stop_words = _shareable_forbidden_words + [
        'available',
        'business',
        'businesses',
        'choice',
        'choices',
        'contact',
        'countries',
        'country',
        'detail',
        'details',
        'domestic',
        'export',
        'exporter',
        'exporters',
        'future',
        'icpo',
        'idea',
        'ideas'
        'import',
        'importer',
        'importers',
        'kind',
        'of'
        'only',
        'oversea',
        'overseas',
        'payment',
        'payments',
        'person',
        'persons',
        'please',
        'product',
        'products',
        'profit',
        'profits',
        'quality',
        'quantity',
        'rate',
        'rates',
        'reject',
        'rejection',
        'relationship',
        'relationships',
        'sblc',
        'varieties',
        'variety',
        'website',
        'websites',
    ]
    tokens = [t for t in tokens if not t.lower() in custom_stop_words]

    # Lowercase
    tokens = [t.lower() for t in tokens]

    # Deduplicate
    tokens = list(dict.fromkeys(tokens))

    # Shuffle
    random.shuffle(tokens)

    # Remove country names
    countries = [c.name.lower() for c in Country.objects.all()]
    tokens = [t for t in tokens if not t in countries]

    # Tag
    tags = pos_tag(tokens)

    # CC	coordinating conjunction
    # CD	cardinal digit
    # DT	determiner
    # EX	existential there
    # FW	foreign word
    # IN	preposition/subordinating conjunction
    # JJ	This NLTK POS Tag is an adjective (large)
    # JJR	adjective, comparative (larger)
    # JJS	adjective, superlative (largest)
    # LS	list market
    # MD	modal (could, will)
    # NN	noun, singular (cat, tree)
    # NNS	noun plural (desks)
    # NNP	proper noun, singular (sarah)
    # NNPS	proper noun, plural (indians or americans)
    # PDT	predeterminer (all, both, half)
    # POS	possessive ending (parent\ ‘s)
    # PRP	personal pronoun (hers, herself, him, himself)
    # PRP$	possessive pronoun (her, his, mine, my, our )
    # RB	adverb (occasionally, swiftly)
    # RBR	adverb, comparative (greater)
    # RBS	adverb, superlative (biggest)
    # RP	particle (about)
    # TO	infinite marker (to)
    # UH	interjection (goodbye)
    # VB	verb (ask)
    # VBG	verb gerund (judging)
    # VBD	verb past tense (pleaded)
    # VBN	verb past participle (reunified)
    # VBP	verb, present tense not 3rd person singular (wrap)
    # VBZ	verb, present tense with 3rd person singular (bases)
    # WDT	wh-determiner (that, what)
    # WP	wh- pronoun (who)
    # WRB	wh- adverb (how)
    labels = ['NNP', 'NNPS', 'NN', 'NNS', 'VB', 'VBP']
    tags = [t for t in tags if t[1] in labels]

    # Remove tags
    tokens = [t[0] for t in tags]

    # We want a URL length of < 80 characters. 'everybase.co/leads' is 19
    # characters long. This leaves us with 71 characters to work with.
    # We ignore append key length because we don't expect the key to contribute
    # much to SEO.
    slug = tokens[0] if len(tokens) > 0 else ''
    append_key = str(append_key)
    for t in tokens[1:]:
        if len(slug) < 71:
            slug += ' ' + t
        else:
            break
    
    if len(slug) > 0:
        slug += ' '
        
    slug += append_key

    # Add model-specific variations
    if sell_country is not None \
        and buy_country is not None \
        and is_selling is not None:
        # Add Lead model-specific variations
        prefix = sell_country if is_selling else buy_country
        prefix += ' ' + buy_country if is_selling else ' ' + sell_country
        slug = prefix + ' ' + slug
    elif is_buy_agent is not None \
        and is_sell_agent is not None \
        and is_logistics_agent is not None:
        # Add User model-specific variations

        # Country may be none if we're not able to ascertain the user's
        # country from his phone number.
        prefix = country + ' ' if country is not None else ''

        prefix += 'buy' if is_buy_agent else 'sell'
        if is_logistics_agent:
            prefix += ' ' + 'logistics'
        slug = prefix + ' ' + slug

    slug = django_slugify(slug)

    sep = ', '
    return slug, sep.join(tokens)