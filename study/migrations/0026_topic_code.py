from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('study', '0025_fix_content_issues'),
    ]

    operations = [
        migrations.AddField(
            model_name='topic',
            name='code',
            field=models.CharField(
                blank=True,
                default='',
                help_text="Topic ordering code e.g. '001A'. Blank for user-created topics.",
                max_length=5,
            ),
        ),
    ]
