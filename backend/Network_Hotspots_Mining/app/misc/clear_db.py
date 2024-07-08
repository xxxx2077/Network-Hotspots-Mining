from app.models import Summary, Class, Relation


def clear_db_summary():
    Summary.objects.all().delete()
    print('table:summary has clear')


def clear_db_class():
    Class.objects.all().delete()
    print('table:class has clear')


def clear_db_relation():
    Relation.objects.all().delete()
    print('table:relation has clear')
