# Generated by Django 4.2.2 on 2023-09-29 08:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0006_title_description_alter_title_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='GptPrompt',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('prompt', models.TextField()),
            ],
            options={
                'verbose_name': 'GPT Prompt',
                'verbose_name_plural': 'GPT Prompts',
            },
        ),
        migrations.AddField(
            model_name='title',
            name='gpt_prompt',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='title_prompts', to='post.gptprompt'),
        ),
    ]
