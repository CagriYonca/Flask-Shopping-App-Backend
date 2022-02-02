from tribeshop.models import Yak, Tribe
import json


def calculate_stocks(T, yak):
    milk = 0
    wool = 0
    days = int(yak.get('age') * 100)
    age_last_shaved = 0
    last_age = float(days + T) / 100
    for i in range(days, days + T):
        milk += 50 - (i * 0.03)
        if i >= 100:
            if i - days == 0:
                wool += 1
                age_last_shaved = i / 100
            else:
                if (i - days) % (8 + i * 0.01) == 0:
                    wool += 1
                    age_last_shaved = i / 100
    return milk, wool, last_age, age_last_shaved

def bury_died_yaks(yaks):
    for i in range(len(yaks)):
        if yaks[i].get('age') >= 10:
            del yaks[i]
    return yaks

def produce_for_t_days(t):
    total_milk = 0
    total_wool = 0
    yaks = bury_died_yaks(json.loads(Yak.objects().to_json()))
    for yak in yaks:
        result = calculate_stocks(t, yak)
        total_milk += result[0]
        total_wool += result[1]
    print('In Stock:\n\t{} liters of milk\n\t{} skins of wool'.format(total_milk, total_wool))
    print('Herd:')
    for yak in yaks:
        print('\t{} {} years old'.format(yak.get('name'), float(yak.get('age') * 100 + t) / 100))
    return total_milk, total_wool, yaks

def get_tribe_info(t):
    herd = []
    yaks = bury_died_yaks(json.loads(Yak.objects().to_json()))
    for yak in yaks:
        _, _, age, age_last_shaved =  calculate_stocks(t, yak)
        herd.append({
            'name': yak.get('name'), 
            'age': age, 
            'age-last-shaved': age_last_shaved
        })
    return herd

def check_stock_info(t, data):
    ordered_milk = data['order'].get('milk')
    ordered_wool = data['order'].get('skins')
    response = {}
    tribe = json.loads(Tribe.objects.first().to_json())
    if tribe.get('total_milk') is None or tribe.get('total_wool') is None:
        total_milk, total_wool, _ = produce_for_t_days(t)
    else:
        total_milk = tribe.get('total_milk')
        total_wool = tribe.get('total_wool')
    if ordered_milk <= total_milk and ordered_milk is not None:
        response['milk'] = ordered_milk
    if ordered_wool <= total_wool and ordered_wool is not None:
        response['skins'] = ordered_wool
    return response
