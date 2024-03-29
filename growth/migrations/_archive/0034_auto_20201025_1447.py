# Generated by Django 3.1.2 on 2020-10-25 06:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('growth', '0033_auto_20201023_2359'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='chemicalbookresultcompany',
            options={'verbose_name': 'ChemicalBookResult-Company relationship', 'verbose_name_plural': 'ChemicalBookResult-Company relationships'},
        ),
        migrations.AlterModelOptions(
            name='chemicalbookresultcompanytype',
            options={'verbose_name': 'ChemicalBookResult-Company type', 'verbose_name_plural': 'ChemicalBookResult-Company types'},
        ),
        migrations.AlterModelOptions(
            name='chemicalbookresultcountry',
            options={'verbose_name': 'ChemicalBookResult-Country relationship', 'verbose_name_plural': 'ChemicalBookResult-Country relationships'},
        ),
        migrations.AlterModelOptions(
            name='chemicalbookresultcountrytype',
            options={'verbose_name': 'ChemicalBookResult-Country type', 'verbose_name_plural': 'ChemicalBookResult-Country types'},
        ),
        migrations.AlterModelOptions(
            name='chemicalbookresultemail',
            options={'verbose_name': 'ChemicalBookResult-Email relationship', 'verbose_name_plural': 'ChemicalBookResult-Email relationships'},
        ),
        migrations.AlterModelOptions(
            name='chemicalbookresultlink',
            options={'verbose_name': 'ChemicalBookResult-Link relationship', 'verbose_name_plural': 'ChemicalBookResult-Link relationships'},
        ),
        migrations.AlterModelOptions(
            name='chemicalbookresultlinktype',
            options={'verbose_name': 'ChemicalBookResult-Link type', 'verbose_name_plural': 'ChemicalBookResult-Link types'},
        ),
        migrations.AlterModelOptions(
            name='chemicalbookresultphonenumber',
            options={'verbose_name': 'ChemicalBookResult-PhoneNumber relationship', 'verbose_name_plural': 'ChemicalBookResult-PhoneNumber relationships'},
        ),
        migrations.AlterModelOptions(
            name='chemicalbookresultphonenumbertype',
            options={'verbose_name': 'ChemicalBookResult-PhoneNumber type', 'verbose_name_plural': 'ChemicalBookResult-PhoneNumber types'},
        ),
        migrations.AlterModelOptions(
            name='lookchemresultaddress',
            options={'verbose_name': 'LookChemResult-Address relationship', 'verbose_name_plural': 'LookChemResult-Address relationships'},
        ),
        migrations.AlterModelOptions(
            name='lookchemresultaddresstype',
            options={'verbose_name': 'LookChemResult-Address type', 'verbose_name_plural': 'LookChemResult-Address types'},
        ),
        migrations.AlterModelOptions(
            name='lookchemresultcompany',
            options={'verbose_name': 'LookChemResult-Company relationship', 'verbose_name_plural': 'LookChemResult-Company relationships'},
        ),
        migrations.AlterModelOptions(
            name='lookchemresultcompanytype',
            options={'verbose_name': 'LookChemResult-Company type', 'verbose_name_plural': 'LookChemResult-Company types'},
        ),
        migrations.AlterModelOptions(
            name='lookchemresultemail',
            options={'verbose_name': 'LookChemResult-Email relationship', 'verbose_name_plural': 'LookChemResult-Email relationships'},
        ),
        migrations.AlterModelOptions(
            name='lookchemresultemailtype',
            options={'verbose_name': 'LookChemResult-Email type', 'verbose_name_plural': 'LookChemResult-Email types'},
        ),
        migrations.AlterModelOptions(
            name='lookchemresultlink',
            options={'verbose_name': 'LookChemResult-Link relationship', 'verbose_name_plural': 'LookChemResult-Link relationships'},
        ),
        migrations.AlterModelOptions(
            name='lookchemresultlinktype',
            options={'verbose_name': 'LookChemResult-Link type', 'verbose_name_plural': 'LookChemResult-Link types'},
        ),
        migrations.AlterModelOptions(
            name='lookchemresultperson',
            options={'verbose_name': 'LookChemResult-Person relationship', 'verbose_name_plural': 'LookChemResult-Person relationships'},
        ),
        migrations.AlterModelOptions(
            name='lookchemresultpersontype',
            options={'verbose_name': 'LookChemResult-Person type', 'verbose_name_plural': 'LookChemResult-Person types'},
        ),
        migrations.AlterModelOptions(
            name='lookchemresultphonenumber',
            options={'verbose_name': 'LookChemResult-PhoneNumber relationship', 'verbose_name_plural': 'LookChemResult-PhoneNumber relationships'},
        ),
        migrations.AlterModelOptions(
            name='lookchemresultphonenumbertype',
            options={'verbose_name': 'LookChemResult-PhoneNumber type', 'verbose_name_plural': 'LookChemResult-PhoneNumber types'},
        ),
        migrations.AlterModelOptions(
            name='worldofchemicalsresultaddress',
            options={'verbose_name': 'WorldOfChemicalsResult-Address relationship', 'verbose_name_plural': 'WorldOfChemicalsResult-Address relationships'},
        ),
        migrations.AlterModelOptions(
            name='worldofchemicalsresultaddresstype',
            options={'verbose_name': 'WorldOfChemicalsResult-Address type', 'verbose_name_plural': 'WorldOfChemicalsResult-Address types'},
        ),
        migrations.AlterModelOptions(
            name='worldofchemicalsresultcompany',
            options={'verbose_name': 'WorldOfChemicalsResult-Company relationship', 'verbose_name_plural': 'WorldOfChemicalsResult-Company relationships'},
        ),
        migrations.AlterModelOptions(
            name='worldofchemicalsresultcompanytype',
            options={'verbose_name': 'WorldOfChemicalsResult-Company type', 'verbose_name_plural': 'WorldOfChemicalsResult-Company types'},
        ),
        migrations.AlterModelOptions(
            name='worldofchemicalsresultemail',
            options={'verbose_name': 'WorldOfChemicalsResult-Email relationship', 'verbose_name_plural': 'WorldOfChemicalsResult-Email relationships'},
        ),
        migrations.AlterModelOptions(
            name='worldofchemicalsresultemailtype',
            options={'verbose_name': 'WorldOfChemicalsResult-Email type', 'verbose_name_plural': 'WorldOfChemicalsResult-Email types'},
        ),
        migrations.AlterModelOptions(
            name='worldofchemicalsresultlink',
            options={'verbose_name': 'WorldOfChemicalsResult-Link relationship', 'verbose_name_plural': 'WorldOfChemicalsResult-Link relationships'},
        ),
        migrations.AlterModelOptions(
            name='worldofchemicalsresultlinktype',
            options={'verbose_name': 'WorldOfChemicalsResult-Link type', 'verbose_name_plural': 'WorldOfChemicalsResult-Link types'},
        ),
        migrations.AlterModelOptions(
            name='worldofchemicalsresultphonenumber',
            options={'verbose_name': 'WorldOfChemicalsResult-PhoneNumber relationship', 'verbose_name_plural': 'WorldOfChemicalsResult-PhoneNumber relationships'},
        ),
        migrations.AlterModelOptions(
            name='worldofchemicalsresultphonenumbertype',
            options={'verbose_name': 'WorldOfChemicalsResult-PhoneNumber type', 'verbose_name_plural': 'WorldOfChemicalsResult-PhoneNumber types'},
        ),
    ]
