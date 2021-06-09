These fixtures MUST be loaded to set up the database.

Created: 27 May 2021, 2:40 PM
Updated: 27 May 2021, 2:40 PM

# Fixtures

common__country.json
    Country dump with primary keys for production only

common__country_stagingdevelopment.json
    Country dump with primary keys for staging and development. Subset
    of common__country_with_pk.json, so code that works on this will work on
    the larger dataset.

# Notes

- ImportJob, SystemTimestamp data only exists in production