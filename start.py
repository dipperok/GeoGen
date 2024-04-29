from main import layer_models


#models = layer_models(N = 1, smoothness=True, multiprocess=False, L=-40, side=0, shiftType=0, Y=750, NX=2000, NY=800, shiftForce=200, 
#                       layerCount=5, layerThickness=[120,83,83,83,1000], scatterAmount=[200,-50])
# models = layer_models(N=9, smoothness=True, shiftCount=2, side=[0,1], Y=[40,80], shiftType=0, L=[30,-30])
# models = layer_models(N=1, NY=60, NX=120, smoothness=True, side = 1, shiftType=0, shiftCount=2, L=10)
# models = layer_models(N=1, NX=300, smoothness=True, scatterMaxValue=10, shiftCount=7, L=[30, 40, -30, 0, -10, 5, -14], Y=[20,50,100,130,180,200,250], shiftForce=10)
# models = layer_models(N=5000, NX=15, NY=150, layerCount=4, scatterPeriod=1, sole = [[50, 74], [90, 99], [110, 114], [1000, 1000]], shiftForce=30, side=0, shiftType=0)
# models = layer_models(N=5000, NX=15, NY=150, layerCount=4, scatterPeriod=1, sole = [[50, 74], [90, 99], [110, 114], [1000, 1000]], shiftForce=15, shiftCount=2, side=[0, 1], shiftType=1, L=[5, -5], Y=[3,12], layerValues=[0, 20, 40,])
# models = layer_models(N=2, NX=150, NY=150, layerCount=4, side=0, shiftType=1)



models = layer_models(N=1, NX=150, NY=60, layerCount=4, scatterPeriod=5,scatterMaxValue=5, layerThickness=[10,10,10,10], withoutShift=True)
models.save(name='DataBasemmm.csv' ,skipLast = True, prefix='RL0', step=1)
models.show(limit=2)
#models = layer_models(N=500, NX=15, NY=300, layerCount=4, scatterPeriod=1, sole = [[50, 74], [90, 99], [110, 114], [1000, 1000]], shiftForce=[5,15], side=0, shiftType=0)
#models.save(name='DataBasemmm.csv' ,skipLast = True, prefix='L1', step=1)
#models = layer_models(N=500, NX=15, NY=300, layerCount=4, scatterPeriod=1, sole = [[50, 74], [90, 99], [110, 114], [1000, 1000]], shiftForce=[5,15], side=0, shiftType=1)
#models.save(name='DataBasemmm.csv' ,skipLast = True, prefix='L1v', step=1)
#models = layer_models(N=500, NX=15, NY=300, layerCount=4, scatterPeriod=1, sole = [[50, 74], [90, 99], [110, 114], [1000, 1000]], shiftForce=[5,15], side=1, shiftType=0)
#models.save(name='DataBasemmm.csv' ,skipLast = True, prefix='R1', step=1)
#models = layer_models(N=500, NX=15, NY=300, layerCount=4, scatterPeriod=1, sole = [[50, 74], [90, 99], [110, 114], [1000, 1000]], shiftForce=[5,15], side=1, shiftType=1)
#models.save(name='DataBasemmm.csv' ,skipLast = True, prefix='R1v', step=1)
# грабен
#models = layer_models(N=500, NX=15, NY=300, layerCount=4, scatterPeriod=1, sole = [[50, 74], [90, 99], [110, 114], [1000, 1000]], shiftForce=[5,15], shiftCount=2, side=[0, 1], shiftType=1)
#models.save(name='DataBasemmm.csv' ,skipLast = True, prefix='LR2', step=1)
# горст
#models = layer_models(N=500, NX=15, NY=300, layerCount=4, scatterPeriod=1, sole = [[50, 74], [90, 99], [110, 114], [1000, 1000]], shiftForce=[5,15], shiftCount=2, side=[0, 1], shiftType=0)
#models.save(name='DataBasemmm.csv' ,skipLast = True, prefix='LR2v', step=1)

    

models = layer_models(N=2, NX=200, NY=150, layerCount=5, scatterPeriod=1, sole = [[35, 89], [75, 114], [95, 129], [1000, 1000]], withoutShift=True)
models.save(name='DataBasemmm.csv' ,skipLast = True, prefix='RL0', step=1)
models.show(limit=2)


# Smooth               ; With multiprocess (16 cores)
# N=5000 ; 537.2 sec   ; 66.0 sec
# N=1000 ; 107.5 sec   ; 15.7 sec
# N=100 ; 10.5 sec     ; 4.1 sec

# No smooth            ; With multiprocess (16 cores)
# N=5000 ; 67.5 sec    ; 12.6 sec
# N=1000 ; 13.4 sec    ; 4.8 sec
# N=100 ; 1.3 sec      ; 3.1 sec






# import time

# start = time.time()

# models = layer_models(N = 1000, smoothness=True)

# end = time.time()
# print(end - start)



                    # num1 = (x1 - i) * (y2 - y1) - (x2 - x1) * (y1 - j)
                    # num2 = (x2 - i) * (y3 - y2) - (x3 - x2) * (y2 - j)
                    # num3 = (x3 - i) * (y1 - y3) - (x1 - x3) * (y3 - j)
                    # if ((num1 >= 0 and num2 >= 0 and num3 >= 0) or (num1 <= 0 and num2 <= 0 and num3 <= 0)):
                    #     # model[j][i] = 0
                    #     print(i, j, de2)
                    #     if (shiftType):
                    #         if (j + shiftForce < rows):
                    #             model[j][i] = model[j + shiftForce][i]
                    #         else:
                    #             model[j][i] = self.downValue
                    #     else: 
                    #         if (j - shiftForce > -1):
                    #             model[j][i] = model[j - shiftForce][i]
                    #         else:
                    #             model[j][i] = self.upperValue