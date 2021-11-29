# Generated by Django 3.0.14 on 2021-11-29 14:31

import core.models
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0015_missing_roles'),
        ('insuree_batch', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='InsureeBatchMutation',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('insuree_batch', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='mutations', to='insuree_batch.InsureeBatch')),
                ('mutation', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='insuree_batches', to='core.MutationLog')),
            ],
            options={
                'db_table': 'insuree_batch_InsureeBatchMutation',
                'managed': True,
            },
            bases=(models.Model, core.models.ObjectMutation),
        ),
    ]