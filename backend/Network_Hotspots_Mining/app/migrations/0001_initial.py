# Generated by Django 4.2.13 on 2024-06-13 08:49

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Class',
            fields=[
                ('class_id', models.AutoField(primary_key=True, serialize=False)),
                ('class_title', models.CharField(blank=True, max_length=100, null=True)),
                ('Key_points', models.CharField(blank=True, max_length=100, null=True)),
                ('summary', models.CharField(blank=True, max_length=1000, null=True)),
            ],
            options={
                'db_table': 'class',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('pid', models.IntegerField(db_comment='所属帖子id')),
                ('content', models.CharField(blank=True, max_length=200, null=True)),
                ('time', models.DateTimeField(blank=True, null=True)),
                ('nickname', models.CharField(blank=True, max_length=45, null=True)),
                ('rid', models.IntegerField(blank=True, db_comment='回复评论id', null=True)),
                ('likenum', models.IntegerField(blank=True, db_column='likeNum', null=True)),
            ],
            options={
                'db_table': 'comments',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Picture',
            fields=[
                ('id', models.CharField(max_length=25, primary_key=True, serialize=False)),
                ('pid', models.IntegerField()),
                ('imgurl', models.CharField(blank=True, db_column='imgURL', max_length=100, null=True)),
                ('ocr', models.CharField(blank=True, max_length=2000, null=True)),
            ],
            options={
                'db_table': 'picture',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='PopRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pid', models.IntegerField(db_comment='帖子id')),
                ('hotval', models.IntegerField(blank=True, db_column='hotVal', null=True)),
                ('hotval_rate', models.FloatField(blank=True, db_column='hotVal_rate', db_comment='热度变化', null=True)),
                ('viewnum', models.IntegerField(blank=True, db_column='viewNum', db_comment='浏览次数', null=True)),
                ('likenum', models.IntegerField(blank=True, db_column='likeNum', db_comment='点赞数', null=True)),
                ('comnum', models.IntegerField(blank=True, db_column='comNum', db_comment='评论数', null=True)),
                ('c_likenum', models.IntegerField(blank=True, db_column='c_likeNum', db_comment='评论点赞总数', null=True)),
                ('top', models.IntegerField(blank=True, null=True)),
                ('recordtime', models.DateTimeField(blank=True, db_column='recordTime', null=True)),
            ],
            options={
                'db_table': 'pop_record',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('title', models.CharField(blank=True, max_length=100, null=True)),
                ('content', models.CharField(blank=True, max_length=2000, null=True)),
                ('nickname', models.CharField(blank=True, max_length=45, null=True)),
                ('cate_name', models.CharField(blank=True, max_length=5, null=True)),
                ('time', models.DateTimeField(blank=True, null=True)),
                ('imgnum', models.IntegerField(blank=True, db_column='imgNum', null=True)),
                ('monitoring', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'post',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Summary',
            fields=[
                ('summary_id', models.AutoField(primary_key=True, serialize=False)),
                ('id', models.IntegerField(blank=True, null=True)),
                ('date', models.CharField(blank=True, max_length=50, null=True)),
                ('location', models.CharField(blank=True, max_length=100, null=True)),
                ('participants', models.CharField(blank=True, max_length=100, null=True)),
                ('Key_points', models.CharField(blank=True, max_length=100, null=True)),
                ('summary', models.CharField(blank=True, max_length=1000, null=True)),
                ('consequences', models.CharField(blank=True, max_length=1000, null=True)),
                ('is_abnormal', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'summary',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=50)),
                ('email', models.CharField(max_length=100)),
                ('password', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField()),
            ],
            options={
                'db_table': 'users',
                'managed': False,
            },
        ),
    ]
