from everybase import settings
from files import serializers as fiserializers

class WriteOnlyPresignedURLSerializer(
    fiserializers.WriteOnlyPresignedURLSerializer):

    def s3_object_key_prefix(self):
        return f'{settings.LEADS_FILES_S3_PATH}/'

    def update_file(self, file):
        file.unlinked_lead_lifespan = settings.LEADS_UNLINKED_FILE_LIFESPAN
        return file