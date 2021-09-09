from django.db import transaction
from relationships.models import Lead, ProductType, Recommendation
from chat.libraries.constants import messages
from chat.libraries.classes.chat_test import ChatTest
from chat.libraries.utility_funcs.render_message import render_message
from chat.tasks.send_recommend_product_type import send_recommend_product_type

class Test(ChatTest):
    fixtures = [
        'setup/20210527__relationships__producttype.json',
        'setup/20210527__relationships__phonenumber',
        'setup/20210527__relationships__phonenumbertype',
        'setup/20210527__relationships__user'
    ]

    def test_run(self):
        with transaction.atomic():
            # Set up models
            p = ProductType.objects.get(pk=1) # Nitrile Gloves
            l = Lead.objects.create(
                owner=self.user,
                product_type=p,
                display_text='Example lead details',
                is_buying=True
            )
            r = Recommendation.objects.create(
                lead=l,
                recommendee=self.user
            )
            
            # Run task
            msg = send_recommend_product_type(r.id, True)

            # Assert
            r.refresh_from_db()
            self.assertIsNotNone(r.recommend_product_type_sent)
            self.assertEqual(
                msg.body,
                render_message(
                    messages.RECOMMEND__PRODUCT_TYPE, {
                        'is_buying': True,
                        'product_type': 'Nitrile Gloves'
                    }
                )
            )