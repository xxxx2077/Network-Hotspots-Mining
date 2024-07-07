# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class Class(models.Model):
    class_id = models.AutoField(primary_key=True)
    class_title = models.CharField(max_length=100, blank=True, null=True)
    key_points = models.CharField(db_column='Key_points', max_length=100, blank=True,
                                  null=True)  # Field name made lowercase.
    summary = models.CharField(max_length=1000, blank=True, null=True)
    hot_value = models.BigIntegerField(blank=True, null=True)
    hot_value_perday = models.BigIntegerField(blank=True, null=True)
    is_relation = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'class'


class Comments(models.Model):
    id = models.IntegerField(primary_key=True)
    pid = models.IntegerField(db_comment='所属帖子id')
    content = models.CharField(max_length=400, blank=True, null=True)
    time = models.DateTimeField(blank=True, null=True)
    nickname = models.CharField(max_length=45, blank=True, null=True)
    rid = models.IntegerField(blank=True, null=True, db_comment='回复评论id')
    likenum = models.IntegerField(db_column='likeNum', blank=True, null=True)  # Field name made lowercase.
    sentiment = models.FloatField(blank=True, null=True, db_comment='情感分析得分')

    class Meta:
        managed = False
        db_table = 'comments'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Picture(models.Model):
    id = models.CharField(primary_key=True, max_length=25)
    pid = models.IntegerField()
    imgurl = models.CharField(db_column='imgURL', max_length=100, blank=True, null=True)  # Field name made lowercase.
    ocr = models.CharField(max_length=3000, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'picture'


class PopRecord(models.Model):
    pid = models.IntegerField(db_comment='帖子id')
    hotval = models.FloatField(db_column='hotVal', blank=True, null=True)  # Field name made lowercase.
    hotval_rate = models.FloatField(db_column='hotVal_rate', blank=True, null=True,
                                    db_comment='热度变化')  # Field name made lowercase.
    viewnum = models.IntegerField(db_column='viewNum', blank=True, null=True,
                                  db_comment='浏览次数')  # Field name made lowercase.
    likenum = models.IntegerField(db_column='likeNum', blank=True, null=True,
                                  db_comment='点赞数')  # Field name made lowercase.
    comnum = models.IntegerField(db_column='comNum', blank=True, null=True,
                                 db_comment='评论数')  # Field name made lowercase.
    c_likenum = models.IntegerField(db_column='c_likeNum', blank=True, null=True,
                                    db_comment='评论点赞总数')  # Field name made lowercase.
    top = models.IntegerField(blank=True, null=True)
    recordtime = models.DateTimeField(db_column='recordTime', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'pop_record'


class Post(models.Model):
    id = models.IntegerField(primary_key=True, db_comment='PostID')
    title = models.CharField(max_length=100, blank=True, null=True)
    content = models.CharField(max_length=2000, blank=True, null=True, db_comment='内容')
    nickname = models.CharField(max_length=45, blank=True, null=True)
    cate_name = models.CharField(max_length=5, blank=True, null=True)
    time = models.DateTimeField(blank=True, null=True)
    imgnum = models.IntegerField(db_column='imgNum', blank=True, null=True)  # Field name made lowercase.
    monitoring = models.IntegerField(blank=True, null=True, db_comment='监听标记')
    is_summaried = models.IntegerField()
    class_id = models.IntegerField(blank=True, null=True, db_comment='所属聚类ID')
    sentiment_negative = models.FloatField(blank=True, null=True, db_comment='帖子讨论情感倾向负面得分')
    correlation = models.FloatField(blank=True, null=True, db_comment='帖子内容与校方的相关程度')

    class Meta:
        managed = False
        db_table = 'post'


class Summary(models.Model):
    id = models.IntegerField(blank=True, null=True)
    summary_id = models.AutoField(primary_key=True)
    date = models.CharField(max_length=50, blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    participants = models.CharField(max_length=100, blank=True, null=True)
    key_points = models.CharField(db_column='Key_points', max_length=100, blank=True,
                                  null=True)  # Field name made lowercase.
    summary = models.CharField(max_length=1000, blank=True, null=True)
    consequences = models.CharField(max_length=1000, blank=True, null=True)
    comments = models.CharField(max_length=1000, blank=True, null=True)
    is_abnormal = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'summary'


class Users(models.Model):
    username = models.CharField(max_length=50)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'users'


class Relation(models.Model):
    id = models.IntegerField(primary_key=True)
    post1 = models.IntegerField(blank=True, null=True)
    post_relation = models.CharField(max_length=255)
    post2 = models.IntegerField(blank=True, null=True)
    class_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'relation'
