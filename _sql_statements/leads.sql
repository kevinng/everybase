select count(*) from leads_chemicalbooksupplier where coy_email != '' and coy_email != '-';

select * from leads_fibre2fashionlead limit 10;

select distinct cat, subcat from leads_fibre2fashionlead order by cat, subcat;

select * from leads_fibre2fashionlead where
	cat = 'Dyes & Chemicals' or
	cat = 'Fibre & FeedStock' or
    cat = 'Machinery';

select distinct cat from leads_fibre2fashionlead order by cat;

select * from leads_fibre2fashionlead where
	cat = 'Dyes & Chemical';

select count(*) from leads_fibre2fashionlead where
	cat = 'Dyes & Chemical';


-- Unique Zero Bounce statuses
select distinct zb_status from leads_zerobounceresult

-- We want to work with valid, catch-all
"abuse"
"valid"
"spamtrap"
"do_not_mail"
"invalid"
"catch-all"
"unknown"

-- Only deal with an unknown status result if MX is found
select * from leads_zerobounceresult where
    zb_status = 'unknown' and
    zb_mx_found = 'True'

select * from leads_zerobounceresult where zb_did_you_mean != ''

-- 62 entries
select count(*) from leads_zerobounceresult where zb_did_you_mean != ''

-- 438 entries
select count(*) from leads_zerobounceresult where
    zb_status = 'unknown'

-- 387 entries
select count(*) from leads_zerobounceresult where
    zb_status = 'unknown' and
    zb_mx_found = 'True'

-- 5511 entries
select count(*) from leads_zerobounceresult where
    zb_status = 'catch-all'

-- 5473 entries
select count(*) from leads_zerobounceresult where
    zb_status = 'catch-all' and
    zb_mx_found = 'True'

-- Sadiq buys mostly textile goods
select * from leads_fibre2fashionlead where
    coy_email = 'sadiq@sameerafashions.com'

"Home Textiles"	"Bath linen"	"Bath linen : Jacquard Fabric (100% Cotton), Woven, Quick-Dry Buyer"
"Home Textiles"	"Bed Sheets"	"Bed Sheets : 100% Cotton, 65% Polyester / 35% Cotton, Woven, quick dry,shrink-resistant Buyer"
"Home Textiles"	"Towels"	"Towels : Jacquard Fabric (100% Cotton), Woven, Quick-Dry & Soft Buyer"
