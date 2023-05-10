from prettytable import PrettyTable
from prettytable import ALL, FRAME

class Utils:
    

    def generateTable(rows,row_names):
        tab = PrettyTable() 

        tab.field_names = row_names

        for row in rows:
            tab.add_row(row)

        tab._validate_field_names = lambda *a, **k: None

        return tab
    
    def safeInput(prompt):
        confirmation = 0
        
        while confirmation == 0:
            try:
                response = input(prompt)
                value = float(response)
                confirmation = 1
            except:
                print('Podana wartość nie jest prawidłowa!\n')
        
        return value

class FirstTable:

    def __init__(self,patterns, weights, hard_data) -> None:
        self.pts = patterns
        self.ws = weights
        self.hd = hard_data


    def getRow(self,pattern):
        euler = 2.718281828459

        sumator = round(self.hd['xo'] * self.ws[0] + pattern[0] * self.ws[1] + pattern[1] * self.ws[2],2)

        euler_yssn = (euler**sumator) / (1 + euler**sumator)

        yssn = 1 if sumator > self.hd['step'] else 0

        return_row = [sumator, yssn, (pattern[2] - yssn)**2, sumator, round((pattern[2] - sumator)**2,2),round(euler_yssn,2), round((pattern[2] - euler_yssn)**2,2)]

        return return_row
    

    def calculate(self):
        wzr = 1
        rows = []
        for pattern in self.pts:

            row = self.getRow(pattern)

            rows.append([wzr] + pattern + row)

            wzr+=1  

        tab = Utils.generateTable(rows,['Wzorzec', 'X1', 'X2', 'Y', 'Sumator', 'Yssn', 'Kw.róż', 'Yssn2', 'Kw.róż2','Yssn3', 'Kw.róż3'])

        return tab

class SecondTable:

    def __init__(self,patterns, weights, hard_data) -> None:
        self.pts = patterns
        self.ws = weights
        self.hd = hard_data

    def getRow(self,pattern):
        eta_error = self.hd['eta'] * error

        sumator = self.hd['xo'] * self.ws[0] + pattern[0] * self.ws[1] + pattern[1] * self.ws[2]

        error = pattern[2]-sumator

        dw0 = self.hd['xo'] * eta_error
        dw1 = pattern[0] * eta_error
        dw2 = pattern[1] * eta_error

        return_row = [sumator,error,dw0,dw1,dw2]

        return return_row

    def calculate(self):
        iteration = 1
        era = 1
        wzr = 1
        rows = []
        while era != 11:
            row = self.getRow(self.pts[wzr-1], self.ws)

            final = [iteration] + [era] + [wzr] + self.ws + row

            self.ws = [self.ws[0]+row[2],self.ws[1]+row[3],self.ws[2]+row[4]]

            for x in range(0,len(final)):
                final[x] = round(final[x],2)

            rows.append(final)

            iteration+=1
            wzr+=1
            if wzr == 5:
                era+=1
                wzr=1

        tab = Utils.generateTable(rows,['Iteracja','Epoka','Wzorzec', 'W0', 'W1', 'W2', 'Sumator', 'Błąd','dW0','dW1','dW2'])

        return tab,final

patterns = [[-0.2, 0.5, 0], [0.2, -0.5, 0], [0.8, -0.8, 1], [0.8, 0.8, 1]]

hard_data = {'xo': 1.0, 'step': 0.5}

weights = []


for t in range(0, 3):
    weights.append(Utils.safeInput(f'Wprowadz wage {t}:\n- '))
print('\nWagi zapisane!')



print('Tabela 1')

ft = FirstTable(patterns,weights,hard_data)
tab1 = ft.calculate()
print(tab1)


eta = Utils.safeInput('Wprowadz ETA:\n- ')
hard_data['eta'] = eta

weights = []

for t in range(0, 3):
    weights.append(Utils.safeInput(f'Wprowadz wage {t}:\n- '))
print('\nWagi zapisane!')


st = SecondTable(patterns,weights,hard_data)
tab2,final_row = st.calculate()

print(tab2)

new_weights = final_row[3:]
final_weights = []

for nw in range(0,3):
    final_weights.append(str(round(new_weights[nw]+ new_weights[nw+5],2)))

print('| Wagi po ostatniej iteracji | '+' | '.join(final_weights))

input('')