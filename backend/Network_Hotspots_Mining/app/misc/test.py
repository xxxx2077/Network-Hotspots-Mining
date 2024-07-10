import json

def fuck():
    with open('./app/result/res_total.json', 'r', encoding='utf-8') as file:
        content_list = json.load(file)

    with open('./app/result/res_cluster2hot.json', 'r', encoding='utf-8') as file:
        cluster2hot_list = json.load(file)
    
    with open('./app/result/res_cluster2hot_perday.json', 'r', encoding='utf-8') as file:
        cluster2hot_perday_list = json.load(file)

    for item in content_list:
        # print(item)
        # print(content_list[item])
        print(cluster2hot_list[item])
        print(cluster2hot_perday_list[item])
        hot_value_total = 0.0
        hot_value_perday_total = 0.0
        for hot_value in (cluster2hot_list[item]):
            hot_value_total += float(hot_value)
        for hot_value_perday in (cluster2hot_perday_list[item]):
            hot_value_perday_total += float(hot_value_perday)
        print(hot_value_total)
        print(hot_value_perday_total)