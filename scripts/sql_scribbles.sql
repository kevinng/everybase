DELETE FROM relationships_email WHERE id > 1000;

DELETE FROM relationships_user where email_id > 1000;

DELETE FROM relationships_useripdevice
USING relationships_user
WHERE
relationships_useripdevice.user_id = relationships_user.id AND
relationships_user.email_id > 1000;

DELETE FROM relationships_accessedurl
USING relationships_user
WHERE
relationships_accessedurl.user_id = relationships_user.id AND
relationships_user.email_id > 1000;


DELETE FROM relationships_useripdevice_accessed_urls
USING relationships_accessedurl, relationships_user
WHERE
relationships_useripdevice_accessed_urls.accessedurl_id = relationships_accessedurl.id AND
relationships_accessedurl.user_id = relationships_user.id AND
relationships_user.email_id > 1000;