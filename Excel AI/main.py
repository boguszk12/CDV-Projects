from prettytable import PrettyTable
from prettytable import ALL, FRAME



def count_row1(pattern, weights, hard_data):
    euler = 2.718281828459

    sumator = round(hard_data['xo'] * weights[0] + pattern[0] * weights[1] + pattern[1] * weights[2],2)

    euler_yssn = (euler**sumator) / (1 + euler**sumator)
    yssn = 1 if sumator > hard_data['step'] else 0
    return_table = [
        sumator, yssn, (pattern[2] - yssn)**2, sumator, round((pattern[2] - sumator)**2,2),
        round(euler_yssn,2), round((pattern[2] - euler_yssn)**2,2)
    ]

    return return_table

def count_row2(pattern, weights, hard_data):
    sumator = hard_data['xo'] * weights[0] + pattern[0] * weights[1] + pattern[1] * weights[2]
    error = pattern[2]-sumator
    dw0 = hard_data['xo'] * hard_data['eta'] * error
    dw1 = pattern[0] * hard_data['eta'] * error
    dw2 = pattern[1] * hard_data['eta'] * error
    return_table = [
        sumator,error,dw0,dw1,dw2
    ]

    return return_table


def generate_table1(pattern, weights, hard_data):
    names = ['Wzorzec', 'X1', 'X2', 'Y', 'Sumator', 'Yssn', 'Kw.róż', 'Yssn2', 'Kw.róż2','Yssn3', 'Kw.róż3']
    tab = PrettyTable() 
    tab.field_names = names
    wzr = 1
    for pattern in patterns:
        data = pattern
        row = count_row1(pattern, weights, hard_data)
        final = [wzr] + data + row
        tab.add_row(final)
        wzr+=1  
    tab._validate_field_names = lambda *a, **k: None
    return tab

def generate_table2(patterns, weights, hard_data):
    names = ['Iteracja','Epoka','Wzorzec', 'W0', 'W1', 'W2', 'Sumator', 'Błąd','dW0','dW1','dW2']
    tab = PrettyTable() 
    tab.field_names = names
    iteration = 1
    era = 1
    wzr = 1
    while era != 11:
        row = count_row2(patterns[wzr-1], weights, hard_data)
        final = [iteration] + [era] + [wzr] + weights + row
        new_weights = [weights[0]+row[2],weights[1]+row[3],weights[2]+row[4]]
        for x in range(0,len(final)):
            final[x] = round(final[x],2)
        tab.add_row(final)
        iteration+=1
        wzr+=1
        if wzr == 5:
            era+=1
            wzr=1
        weights = new_weights
    tab._validate_field_names = lambda *a, **k: None
    return tab,final


    

patterns = [[-0.2, 0.5, 0], [0.2, -0.5, 0], [0.8, -0.8, 1], [0.8, 0.8, 1]]

hard_data = {'xo': 1.0, 'step': 0.5}

weights = []

for t in range(0, 3):
  weights.append(float(input(f'Wprowadz wage {t}:\n- ')))
print('\nWagi zapisane!')


print('Tabela 1')

tab1 = generate_table1(patterns,weights,hard_data)
print(tab1)


eta = float(input('Wprowadz ETA:\n- '))
hard_data['eta'] = 0.3

weights2 = []

for t in range(0, 3):
  weights2.append(float(input(f'Wprowadz wage {t}:\n- ')))
print('\nWagi zapisane!')

tab2,final_row = generate_table2(patterns,weights2,hard_data)
print(tab2)

new_weights = final_row[3:]
final_weights = []

for nw in range(0,3):
    final_weights.append(str(round(new_weights[nw]+ new_weights[nw+5],2)))

print('| Wagi po ostatniej iteracji | '+' | '.join(final_weights))

input('')