

"""
Why don't I have a root class for all product types

the class should have the following methods

mark product type


but...

we have companies and products belonging to a type





detect product type
    detect specification type
    detect specification
    detect company
    detect product

I can also detect the others in parallel
E.g., I may detect specification type for 2 product types, but then I may find
one product type only, so I use the specification types for the company



We work with functions first, they are easier to iterate from, we can refactor
into classes later.



I can have meta details
line 1 to 5 - is this product
Line 1 to 5 - is this company
Line 1 to 5 - is this product type

Line 6 to 7 - is this product type











This has to be done on the global level - across all product types, companies, etc

run product type by itself
run product by itself
run company by itself
run specification type by itself

run product type again with inputs from other 3
run product again with inputs from other 3
run company again with inputs from other 3
run specification type with inputs from other 3

why don't I repeat the process, until the data is stabalized?


get_prices


"""




"""
What can we optimize around



company
product type
I need company-product-type to optimize either above selection; I need to call the database; I cannot store this local

product
Need product-product-type to optimize; for this to work, I need to call the database; I cannot store this local
Need product-company to optimize; for this to work, I need to call the database; I cannot store this local

product specification type

having user also helps - because if the user only deals with a certain set of products, then we need can infer that


unit of measure
unit-of-measure to product-type

location
location - productspecificationtype

incoterm availability


How do I want the data to be processed before we run this function into it?


tokenized into lines
- I can mark from which lines to which lines, we're talking about product type
- Marked for decimal, domain




"""

def get_product_types(lines, marked_lines):
    """What should the output be line?

    lines coming in
    [
        'hello world',
        'hello world',
        'hello world',
    ]
    We could have marked lines, we could have unmarked lines


    It should be passable to the other functions


    For a line - what's the product type?
    The assumption is that we won't have 2 lines talking about different product types. If so, we'd detect the first type and miss the second

    Corresponds to lines
    refers to programmatic keys
    [
        ['product_type_a', 'product_type_b'],
        ['product_type_a', 'product_type_c'],
        ['product_type_d'],
        ['product_type_e'],
        [],
        [],
    ]


    """
    pass