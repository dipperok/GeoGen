# GeoGen
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
- 
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

Function that generate geological fault
===
- model - your model
- Y - column number of center geological fault (default = +-20% from center)
- L - angle of geological fault
- shiftForce - force of the geological fault
- side - fault side (0 = left ; 1 - right)
- shiftType - recession or shift (0 = down ; 1 = up)

Function that show models or a single model
===
- limit - models limit
- cmap - Colormap