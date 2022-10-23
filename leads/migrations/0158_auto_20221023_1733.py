# Generated by Django 3.1.2 on 2022-10-23 09:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('leads', '0157_auto_20220811_2240'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='applicationmessage',
            name='application',
        ),
        migrations.RemoveField(
            model_name='applicationmessage',
            name='author',
        ),
        migrations.RemoveField(
            model_name='applicationquerylog',
            name='user',
        ),
        migrations.RemoveField(
            model_name='contact',
            name='country',
        ),
        migrations.RemoveField(
            model_name='contact',
            name='email',
        ),
        migrations.RemoveField(
            model_name='contact',
            name='lead',
        ),
        migrations.RemoveField(
            model_name='contact',
            name='phone_number',
        ),
        migrations.RemoveField(
            model_name='contactaction',
            name='contact',
        ),
        migrations.RemoveField(
            model_name='contactnote',
            name='contact',
        ),
        migrations.RemoveField(
            model_name='filterformpost',
            name='user',
        ),
        migrations.RemoveField(
            model_name='lead',
            name='author',
        ),
        migrations.RemoveField(
            model_name='lead',
            name='buy_country',
        ),
        migrations.RemoveField(
            model_name='lead',
            name='category',
        ),
        migrations.RemoveField(
            model_name='lead',
            name='country',
        ),
        migrations.RemoveField(
            model_name='lead',
            name='currency',
        ),
        migrations.RemoveField(
            model_name='lead',
            name='sell_country',
        ),
        migrations.RemoveField(
            model_name='leadcomment',
            name='commentor',
        ),
        migrations.RemoveField(
            model_name='leadcomment',
            name='lead',
        ),
        migrations.RemoveField(
            model_name='leadcomment',
            name='reply_to',
        ),
        migrations.AlterUniqueTogether(
            name='leaddetailview',
            unique_together=None,
        ),
        migrations.RemoveField(
            model_name='leaddetailview',
            name='lead',
        ),
        migrations.RemoveField(
            model_name='leaddetailview',
            name='viewer',
        ),
        migrations.AlterUniqueTogether(
            name='leadflag',
            unique_together=None,
        ),
        migrations.RemoveField(
            model_name='leadflag',
            name='lead',
        ),
        migrations.RemoveField(
            model_name='leadflag',
            name='user',
        ),
        migrations.RemoveField(
            model_name='leadqueryaction',
            name='tracker',
        ),
        migrations.RemoveField(
            model_name='leadqueryaction',
            name='user',
        ),
        migrations.RemoveField(
            model_name='mentionedcountry',
            name='country',
        ),
        migrations.RemoveField(
            model_name='mentionedcountry',
            name='lead',
        ),
        migrations.RemoveField(
            model_name='mentionedincoterm',
            name='incoterm',
        ),
        migrations.RemoveField(
            model_name='mentionedincoterm',
            name='lead',
        ),
        migrations.RemoveField(
            model_name='mentionedpaymentterm',
            name='lead',
        ),
        migrations.RemoveField(
            model_name='mentionedpaymentterm',
            name='term',
        ),
        migrations.RemoveField(
            model_name='mentionedproduct',
            name='lead',
        ),
        migrations.RemoveField(
            model_name='mentionedproduct',
            name='product',
        ),
        migrations.AlterUniqueTogether(
            name='savedlead',
            unique_together=None,
        ),
        migrations.RemoveField(
            model_name='savedlead',
            name='lead',
        ),
        migrations.RemoveField(
            model_name='savedlead',
            name='saver',
        ),
        migrations.RemoveField(
            model_name='searchnotification',
            name='country',
        ),
        migrations.RemoveField(
            model_name='searchnotification',
            name='email',
        ),
        migrations.RemoveField(
            model_name='searchnotification',
            name='lead_query_action',
        ),
        migrations.RemoveField(
            model_name='searchnotification',
            name='phone_number',
        ),
        migrations.RemoveField(
            model_name='tracker',
            name='lead',
        ),
        migrations.RemoveField(
            model_name='tracker',
            name='user',
        ),
        migrations.RemoveField(
            model_name='whatsappclick',
            name='contactee',
        ),
        migrations.RemoveField(
            model_name='whatsappclick',
            name='contactor',
        ),
        migrations.AlterUniqueTogether(
            name='whatsappleadauthorclick',
            unique_together=None,
        ),
        migrations.RemoveField(
            model_name='whatsappleadauthorclick',
            name='contactor',
        ),
        migrations.RemoveField(
            model_name='whatsappleadauthorclick',
            name='lead',
        ),
        migrations.RemoveField(
            model_name='whatsappmessagebody',
            name='contactee',
        ),
        migrations.RemoveField(
            model_name='whatsappmessagebody',
            name='contactor',
        ),
        migrations.DeleteModel(
            name='Application',
        ),
        migrations.DeleteModel(
            name='ApplicationMessage',
        ),
        migrations.DeleteModel(
            name='ApplicationQueryLog',
        ),
        migrations.DeleteModel(
            name='Contact',
        ),
        migrations.DeleteModel(
            name='ContactAction',
        ),
        migrations.DeleteModel(
            name='ContactNote',
        ),
        migrations.DeleteModel(
            name='FilterFormPost',
        ),
        migrations.DeleteModel(
            name='Incoterm',
        ),
        migrations.DeleteModel(
            name='Lead',
        ),
        migrations.DeleteModel(
            name='LeadCategory',
        ),
        migrations.DeleteModel(
            name='LeadComment',
        ),
        migrations.DeleteModel(
            name='LeadDetailView',
        ),
        migrations.DeleteModel(
            name='LeadFlag',
        ),
        migrations.DeleteModel(
            name='LeadQueryAction',
        ),
        migrations.DeleteModel(
            name='MentionedCountry',
        ),
        migrations.DeleteModel(
            name='MentionedIncoterm',
        ),
        migrations.DeleteModel(
            name='MentionedPaymentTerm',
        ),
        migrations.DeleteModel(
            name='MentionedProduct',
        ),
        migrations.DeleteModel(
            name='PaymentTerm',
        ),
        migrations.DeleteModel(
            name='Product',
        ),
        migrations.DeleteModel(
            name='SavedLead',
        ),
        migrations.DeleteModel(
            name='SearchNotification',
        ),
        migrations.DeleteModel(
            name='Tracker',
        ),
        migrations.DeleteModel(
            name='WhatsAppClick',
        ),
        migrations.DeleteModel(
            name='WhatsAppLeadAuthorClick',
        ),
        migrations.DeleteModel(
            name='WhatsAppMessageBody',
        ),
    ]
