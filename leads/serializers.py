from everybase import settings
from files import serializers as fiserializers

class WriteOnlyPresignedURLSerializer(
    fiserializers.WriteOnlyPresignedURLSerializer):

    def s3_object_key_prefix(self):
        return f'{settings.LEADS_FILES_S3_PATH}/'

    def update_file(self, file):
        return file