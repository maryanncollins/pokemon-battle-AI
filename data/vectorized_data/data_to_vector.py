import pandas as pd
import numpy as np


name_code = pd.read_csv('pokemon_code.csv')
name_code.set_index('Name', inplace=True)
ncd = len(name_code)   # number of coded pokemon
boost_to_code = {'atk':0,'def':1,'spa':2,'spd':3,'spe':4,'accuracy':5,'evasion':6}
weather_to_code = {'RainDance':0,'SunnyDay':1,'Snow':2,'Sandstorm':3}
field_to_code = {'Grassy Terrain':0,'Electric Terrain':1,'Psychic Terrain':2,'Misty Terrain':3}


def get_value(row,name,non_output):
    if pd.isna(row[name]):
        return non_output
    else:
        return row[name]



def get_vector_by_name(name):

    try:
        code = name_code.loc[name, 'Code']
    except KeyError:
        return [1/ncd]*ncd
    vec = [0]*ncd
    vec[code] = 1
    return vec




def get_weight(row):                #e^-(hp_dif^2) prevents learning from falling number
    rank, turn, total_turn = row['rank'], row['turn'], row['total_turn']
    hp_dif = (row['p1a_hp'] + row['p1b_hp'] + row['p1c_hp'] + row['p1d_hp'] - row['p2a_hp'] - row['p2b_hp'] - row['p2c_hp'] - row['p2d_hp'])/200
    weight = (1 + (rank-1000)/400)*(turn+1)/(total_turn+1)*(1+0.2*np.log(total_turn+1))*np.exp(-(hp_dif)**2)
    if row['p1_alive'] != row['p2_alive']:
        weight *= 0.2                                                                       
    return weight

def vectorize(row):
    win=row['win']
    pokemon_dict = {}
    player_dict = {}
    for p in ['p1a','p1b','p1c','p1d','p2a','p2b','p2c','p2d']:     
        name_v = get_vector_by_name(row[p +'_form'])
        stat_v = [int(row[p +'_hp'])]
        boost_v = [0]*7
        status_v = [0,0,0]
        status_other_v = [0,0,0,0]

        status = get_value(row, p+'_status','')
        if status:
            if status == 'fnt':
                name_v = [0]*ncd
                stat_v = [0]
            elif status == 'brn':
                status_v = [1,1,0]
            elif status == 'psn':
                status_v = [2,0,0]
            elif status == 'frz':
                status_v = [0,0,4]
            elif status == 'par':
                status_v = [0,0,0.75]
            elif status.startswith('tox'):
                status_v = [int(status[4:]),0,0.75]
            elif status.startswith('slp'):
                status_v = [0,0,int(status[4:])]

        if p in ['p1a','p1b','p2a','p2b']:
            status_other = get_value(row, p+'_status_other','')
            if status_other:
                status_other = status_other.split(',')
                for s in status_other:
                    sn = s.split(':')[0]
                    st = s.split(':')[1]
                    if sn == 'Taunt':
                        status_other_v[0] += int(st)
                    if sn == 'Encore':
                        status_other_v[1] += int(st)
                    if sn == 'perish':
                        status_other_v[2] += int(st)
                    if sn == 'confusion':
                        status_v[2] += 0.3
                        status_v[0] += 1
                    if sn == 'Leech Seed':
                        status_v[0] += 1.6
                    if sn == 'Salt Cure':
                        status_v[0] += 2                                    #fix later
                    if sn == 'Substitute':
                        status_other_v[3] = 1
            item =  get_value(row, p+'_item','')
            if item.startswith('Choice'):
                status_other_v[1] == 15
            if item in ['Leftovers','Black Sludge']:
                status_v[0] -= 1
            if item == 'Assault Vest':
                status_other_v[0] == 15
            boost = get_value(row, p+'_stat_boost','')
            if boost:
                boost = boost.split(',')
                for b in boost:
                    bn = b.split(':')[0]
                    bt = int(b.split(':')[1])
                    boost_v[boost_to_code[bn]] = bt
        if p in ['p1a','p1b','p2a','p2b']:
            pokemon_dict[p] = name_v + stat_v + status_v + boost_v + status_other_v         #65
        else:
            pokemon_dict[p] = name_v + stat_v + status_v                              #54

    for p in ['p1','p2']:
        side_v = [0,0,0]                                                                    
        side = get_value(row,p+'_side','')
        if side:
            side = side.split(',')
            for s in side:
                sn = s.split(':')[0]
                st = int(s.split(':')[1])
                if sn == 'Reflect':
                    side_v[1] = st
                elif sn == 'Light Screen':
                    side_v[2] = st
                elif sn == 'Aurora Veil':
                    side_v[1] = st
                    side_v[2] = st
                elif sn == 'Tailwind':
                    side_v[0] = st
        player_dict[p] = side_v


    weather_v = [0,0,0,0]
    field_v = [0,0,0,0]
    condition_v = [0,0]

    weather = get_value(row,'weather','')
    if weather:
        wn = weather.split(':')[0]
        wt = int(weather.split(':')[1])
        weather_v[weather_to_code[wn]] = wt
    field = get_value(row,'field','')
    if field:
        fn = field.split(':')[0]
        ft = int(field.split(':')[1])
        field_v[field_to_code[fn]] = ft
    condition = get_value(row,'condition','')
    if condition:
        condition = condition.split(',')
        for c in condition:
            cn = c.split(':')[0]
            ct = int(c.split(':')[1])
            if cn == 'Trick Room':
                condition_v[0] = ct
            elif cn == 'Gravity':
                condition_v[1] = ct




    result = {}
    result['weather'] = weather_v
    result['field'] = field_v
    result['condition'] = condition_v
    for p in ['p1','p2']:
        result[p] = player_dict[p]
    for p in ['p1a','p1b','p1c','p1d','p2a','p2b','p2c','p2d']:
        result[p] = pokemon_dict[p]
    result['output'] = (win + 1)/2
    result['weight'] = get_weight(row)




    return result



for datafile in ['test02.csv','train02.csv']:
    data = pd.read_csv(datafile)
    #data_f = data[(data['rank'] > 1200) & ((data['total_turn'] - data['turn']) < 4)]
    data_f = data
    vectorized_data = pd.DataFrame(data_f.apply(vectorize, axis=1).tolist())
    vectorized_data.to_csv('vectorized_'+datafile,index=False)
