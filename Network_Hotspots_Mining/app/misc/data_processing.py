from app.models import Summary
from app.util.util import querySet_to_list 

def preprocess_data():
    res = []
    querySet = Summary.objects.values('summary_id','summary').all()
    num = len(querySet)
    summary_id_list = querySet_to_list(querySet,'summary_id')
    summary_list = querySet_to_list(querySet,'summary')
    for i in range(num):
        print(type(summary_list[i]))
        print(summary_list[i])
        if str(summary_list[i]) == 'N/A'  or str(summary_list[i]) == '' or str(summary_list[i]) == '无' or summary_list[i] == 'NAN' or summary_list[i] is None:
            Summary.objects.filter(summary_id=summary_id_list[i]).update(is_abnormal=True)
            res.append({summary_id_list[i]:summary_list[i]})
    print('以下为异常summary')
    for var in res:
        print(var)
        