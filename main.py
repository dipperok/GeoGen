import numpy as np
import matplotlib.pyplot as plt
import random
import math
import csv

class layer_models:
    def __init__(self, N = 1, NY=60, NX=120, layerCount = None, layerThickness=[], layerValues=[],
                  scatterMaxValue=5, scatterPeriod=5, smoothness=False, Y=None, L=None, shiftForce=None,
                  side = None, shiftType = None, shiftCount = 1, multiprocess=False, scatterAmount = [], sole=None, withoutShift=False):
        """
        Function that generate N models
        ===
        - N - number of models
        - NY - number of rows
        - NX - number of columns
        - layerCount - number of layers (default = 3-6)
        - layerThickness - size of every layer (list)
        - layerValues - value in every layer (list)
        - scatterMaxValue - maximum scatter value (default = 5)
        - scatterPeriod - scatter period (default = 5)
        - smoothness - smooth scatter
        - scatterAmount - height of scatter (only in smooth mode)
        - sole - outsole layer (2d or 1d array)
        - ----
        - withoutShift - will generate model without shift
        - Y - column number of center geological fault (default = +-20% from center)
        - L - angle of geological fault
        - shiftForce - force of the geological fault (default = 4-12)
        - side - fault side (0 = left ; 1 - right)
        - shiftType - recession or shift (0 = down ; 1 = up)
        - shiftCount - shift count
        - ----
        - multiprocess - enables multiprocess
        """
        self.N = N
        self.NY = NY
        self.NX = NX
        self.layerCount = layerCount
        self.layerThickness = layerThickness
        self.layerValues = layerValues
        self.scatterMaxValue = scatterMaxValue
        self.scatterPeriod = scatterPeriod
        self.sole = sole
        self.smoothness = smoothness
        self.multiprocess = multiprocess

        self.Y = Y
        self.L = L
        self.shiftForce = shiftForce
        self.side = side
        self.shiftType = shiftType
        self.scatterAmount = scatterAmount
        self.shiftCount = shiftCount
        self.withoutShift = withoutShift

        self.LSave = []
        self.YstartSave = []
        self.layerValuesSave = []
        self.models = self.__gen_models()


    def generate_base(self):
        """
        Function that generates layer model
        ===
        - layerCount - number of layers
        - NY - number of rows
        - NX - number of columns
        - layerThickness - size of every layer (list)
        - layerValues - value in every layer (list)
        - scatterMaxValue - maximum scatter value (default = 5)
        - scatterPeriod - scatter period (default = 5)
        - smoothness - smooth scatter
        - scatterAmount - height of scatter (only in smooth mode)
        """
        if (len(self.layerThickness) < self.layerCount):
            val = round(np.random.uniform(self.NY/9, self.NY/6))
            self.layerThickness = [val]
            tempsum = val
            for i in range(self.layerCount - 1):
                temp2 = self.NY - self.layerThickness[0]
                temp = round(np.random.uniform(temp2/10, abs((temp2/2.5) * (temp2 - tempsum)/temp2) + temp2/10))
                self.layerThickness.append(temp)
                tempsum +=temp
                if (tempsum > self.NY - self.NY/5):
                    break
            while True:
                if (self.layerCount != len(self.layerThickness)):
                    index = np.argmax(self.layerThickness)
                    val = round(self.layerThickness[index]/2)
                    self.layerThickness[index] = val
                    self.layerThickness.append(val)
                else: break

        if (len(self.layerValues) < self.layerCount):
            layerValues = []
            temp = 1
            for i in range(self.layerCount):
                temp += random.randint(10, 30)
                layerValues.append(temp)

        currentLayer = 0
        scatter = 0

        self.upperValue = layerValues[0]
        self.downValue = layerValues[len(layerValues)-1]
        self.layerValuesSave.append(layerValues)

        model = np.empty(shape=(self.NY,self.NX))

        if (self.smoothness):
            if not scatterAmount:
                scatterAmount = []
                for i in range(random.randint(2,3)):
                    scatterAmount.append(random.randint(self.NY/10, self.NY/5) * (1 if random.random() < 0.5 else -1))
            model.fill(layerValues[0])

            temp = 0

            for o in range(len(self.layerThickness) - 1):
                temp += self.layerThickness[o]

                arrY = [temp]
                for i in range(len(scatterAmount)):
                    arrY.append(temp + scatterAmount[i])

                for i in range(self.NY):
                    for j in range(self.NX):
                        temp1 = j/self.NX
                        y = self.bezier_curves(temp1, arrY)
                        if (i > y):
                            model[i][j] = layerValues[o + 1]
        else:
            if self.sole:
                prevSole = []
                for o in self.sole:
                    prevSole.append(random.randint(o[0], o[1]))

                for i in range(self.NX):
                    if (type(self.sole[0]) is not list):
                        tempSole = self.sole
                    else:
                        tempSole = []
                        for o in range(len(self.sole)):
                            tempSole.append(random.randint(np.clip(prevSole[o] - 9, self.sole[o][0], self.sole[o][1]), 
                                                           np.clip(prevSole[o] + 9, self.sole[o][0], self.sole[o][1])))

                    counter = 0
                    currentValue = 0
                    for j in range(self.NY):
                        if (counter >= tempSole[currentValue]):
                            currentValue += 1
                            # counter = 0
                        model[j][i] = layerValues[currentValue]
                        counter +=1
                    prevSole = tempSole
            else:
                tempThickness = self.layerThickness[:]
                print(tempThickness)

                if (self.scatterMaxValue is not list):
                    self.scatterMaxValue = np.full(shape=self.layerCount,  fill_value = self.scatterMaxValue)

                for i in range(self.NY):
                    tempThickness[currentLayer] -= 1
                    if (tempThickness[currentLayer] == 0 and len(layerValues) - 1 > currentLayer):
                        currentLayer +=1
                    for j in range(self.NX):
                        if (j%self.scatterPeriod == 0):
                            scatter = random.randint(0,self.scatterMaxValue[currentLayer])
                        for u in range(scatter):
                            if i-u >= self.NY:
                                continue
                            model[i-u][j] = layerValues[currentLayer]
                        if scatter == 0:
                            model[i][j] = layerValues[currentLayer]
            
        return model


    def bezier_curves(self, temp, arr):
            y = 0
            temp2 = 1
            for num in range(len(arr)):
                if (num%(len(arr)-1) == 0):
                    temp2 = 1
                else:
                    temp2 = len(arr)-1
                y += ((1-temp)**(num)) * (temp ** (len(arr) - 1 - num)) * arr[len(arr) - 1 - num] * temp2
            return y
    

    def gen_slice(self, model, L=None, side = random.randint(0,1), Y=None, shiftForce = 15, iterationCount=0):
        """
        Function that generate geological fault
        ===
        - model - your model
        - Y - column number of center geological fault (default = +-20% from center)
        - L - angle of geological fault
        - shiftForce - force of the geological fault
        - side - fault side (0 = left ; 1 - right)
        - shiftType - recession or shift (0 = down ; 1 = up)
        """
        columns = len(model[0])
        rows = len(model)

        shiftType = self.shiftType
        L = self.L

        if shiftType == None:
            shiftType = random.randint(0,1)
        if Y == None:
            Y = np.random.uniform((columns/2) - (columns/100)*20, (columns/2) + (columns/100)*20)   

        if (self.shiftCount > 1):
            if ((side == 0 and shiftType== 1) or (side == 1 and shiftType == 0)):
                Ystart = np.random.uniform(Y - (Y/100) * 35, Y)
            else: 
                Ystart = np.random.uniform(Y, (Y/100) * 35 + Y)
        else:
            if ((side == 0 and shiftType== 1) or (side == 1 and shiftType == 0)):
                Ystart = np.random.uniform(0, Y)
            else: 
                Ystart = np.random.uniform(Y, self.NX)

        if (Ystart > self.NX):
            Ystart = self.NX
        elif (Ystart < 0):
            Ystart = 0

        if L == None:
            L = math.degrees(math.tan((Y-Ystart) / (self.NY/2)))

        temp = math.tan(math.radians(90-L))

        if (self.shiftCount>1):
            if (iterationCount%self.shiftCount == 0):
                self.LSave.append([L])
                self.YstartSave.append([Ystart])
            else:
                self.LSave[len(self.LSave)-1].append(L)
                self.YstartSave[len(self.YstartSave)-1].append(Ystart)
        else:
            self.LSave.append(L)
            self.YstartSave.append(Ystart)
            
        for i in (range(columns) if shiftType else reversed(range(columns))):
            de2 = temp * (i - Ystart)
            for j in (range(rows) if shiftType else reversed(range(rows))):
                if ((side and ((de2 >= j and L>=0) or (de2<=j and L<0))) or (not side and ((de2 >= j and L<=0) or (de2<=j and L>0)))):
                    if (shiftType):
                        if (j + shiftForce < rows):
                            model[j][i] = model[j + shiftForce][i]
                        else:
                            model[j][i] = self.downValue
                    else: 
                        if (j - shiftForce > -1):
                            model[j][i] = model[j - shiftForce][i]
                        else:
                            model[j][i] = self.upperValue
        return model


    def __params_validation(self, layerCount, layerThickness, layerValues):
        result = [False, []]

        if ((len(layerThickness) > 3 and layerCount == None) or (layerCount and len(layerThickness) > layerCount)):
            result[1].append('layerThickness count is greater than layerCount')
            result[0] = True

        if ((len(layerValues) > 3 and layerCount == None) or (layerCount and len(layerValues) > layerCount)):
            result[1].append('layerValues count is greater than layerCount')
            result[0] = True

        if ((len(layerThickness) < 3 and layerCount == None) or (layerCount and len(layerThickness) < layerCount)):
            result[1].append('layerThickness count is less than layerCount so it will generated')

        if ((len(layerValues) < 3 and layerCount == None) or (layerCount and len(layerValues) < layerCount)):
            result[1].append('layerValues count is less than layerCount so it will generated')

        return result


    def __gen_models(self):
        models = []
        
        validation = self.__params_validation(self.layerCount, self.layerThickness, self.layerValues)

        if (validation[0]):
            raise ValueError(validation[1][0])

        if (validation[1]):
            for val in validation[1]:
                print(val)

        if not self.multiprocess:
            for o in range(self.N):
                model = self.generate_base()
                if not self.withoutShift:
                    for i in range(self.shiftCount):
                        sideTemp = self.side
                        YTemp = self.Y
                        shiftForceTemp = self.shiftForce
                        if (type(self.shiftForce) == list):
                            shiftForceTemp = random.randint(self.shiftForce[0],self.shiftForce[1])
                        if self.shiftCount > 1:
                            if (i%self.shiftCount == 0):
                                YTemp = np.random.uniform((self.NX/100)*10, (self.NX/100)*40)
                            else:
                                YTemp = np.random.uniform(self.NX - (self.NX/100)*40, self.NX - (self.NX/100)*10)
                            sideTemp = self.side[i%self.shiftCount]
                        model = self.gen_slice(model, side=sideTemp, Y=YTemp, shiftForce=shiftForceTemp, iterationCount=i)
                models.append(model)
        else:
            import multiprocessing
            models = multiprocessing.Manager().list()
            cores = multiprocessing.cpu_count()

            if (cores > self.N):
                print('The number of models is less than the number of cores. It is better not to use multiprocessing')

            processes = []
            calc = self.N // cores
            diff = self.N % cores

            for i in range(cores):
                processes[i].start()

            for p in processes:
                p.join()
        return models


    def multi_sequential(self, index, models, calc, NY, NX, layerCount, layerThickness, layerValues,
                          scatterMaxValue, scatterPeriod, smoothness, Y, L, side, shiftType, shiftForce):
        print(f"Запускаем поток № {index}")
        isDefault = [shiftForce if type(shiftForce)==list else 1 if type(shiftForce)==int else 0,
                     True if layerCount else False,
                     True if L else False] 
        
        for i in range(calc):
            layerCount = layerCount if isDefault[1] else random.randint(3,6)
            L = L if isDefault[2] else random.randint(-45, 45)
            shiftForce = random.randint(isDefault[0][0], isDefault[0][1]) if type(isDefault[0])==list else shiftForce if isDefault[0] == 1 else random.randint(6,12)

            model = self.generate_base(layerCount, NY, NX, layerThickness, layerValues, scatterMaxValue, scatterPeriod, smoothness)
            model = self.gen_slice(model, Y, L, shiftForce, side = side if side is None else random.randint(0,1), shiftType = shiftType if shiftType is None else random.randint(0,1))
            models.append(model)
        print(f"{calc} циклов вычислений закончены. Процессор № {index}")


    def show(self, limit=9, cmap='viridis'):
        """
        Function that show models or a single model
        ===
        - limit - models limit
        - cmap - Colormap
        """
        if (len(self.models) > limit):
            self.models = self.models[:limit]

        if len(self.models) == 1:
            figure, axis = plt.subplots(1, 1)

            axis.imshow(self.models[0], cmap)

            plt.show()
            return
        elif len(self.models) == 2:
            figure, axis = plt.subplots(1, 2)
            axis[0].imshow(self.models[0], cmap)
            axis[1].imshow(self.models[1], cmap)

            plt.show()
            return
        
        up =  math.ceil(len(self.models)**0.5)
        low =  round(len(self.models)**0.5)

        figure, axis = plt.subplots(low, up)
        
        for i in range(len(self.models)):
            axis[i//up, i%up].imshow(self.models[i], cmap)

        plt.show()

        
    def save(self, name='data.csv', skipLast = False, step=2, prefix=''):
        # model = np.array(self.models)
        # model = model.reshape(model.shape[0], -1)
        # np.savetxt('data.csv', model, delimiter=',', fmt='%.1f')
        y = 0.02
        f = open(name, 'a', newline='')
        writer = csv.writer(f)
        for o in range(len(self.models)):
            modelsThiknes = []
            for i in range(len(self.models[0][0])):
                if i%step:
                    continue
                counter = 0
                layercounter = 0
                thikness = []
                for j in range(len(self.models[0])):
                    if (self.models[o][j][i] != self.layerValuesSave[o][layercounter]):
                        if (self.layerValuesSave[o].index(self.models[o][j][i]) >= layercounter):
                            thikness.append(round(counter, 2))
                            layercounter += 1
                    counter += y
                if (not skipLast):
                    thikness.append(round(counter, 2))
                modelsThiknes.append(thikness)
            modelsThiknes = np.transpose(modelsThiknes)

            if (not self.LSave):
                writer.writerow([*modelsThiknes[0], *modelsThiknes[1], *modelsThiknes[2], prefix, 'nan', 'nan', 'nan', 'nan'])
            elif (self.shiftCount == 2):
                writer.writerow([*modelsThiknes[0], *modelsThiknes[1], *modelsThiknes[2], prefix, self.LSave[o][0], self.YstartSave[o][0], self.LSave[o][1], self.YstartSave[o][1]])
            else:
                writer.writerow([*modelsThiknes[0], *modelsThiknes[1], *modelsThiknes[2], prefix, self.LSave[o], self.YstartSave[o], 'nan', 'nan'])
        f.close()
        return