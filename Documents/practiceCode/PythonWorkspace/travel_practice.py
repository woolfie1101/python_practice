# import travel.thailand

# trip_to = travel.thailand.ThailandPackage()
# trip_to.detail()

# from travel.thailand import ThailandPackage

# trip_to = ThailandPackage()
# trip_to.detail()

# from travel import vietnam

# trip_to = vietnam.vietnamePackage()
# trip_to.detail()

from travel import *

# trip_to = vietnam.vietnamePackage()
trip_to = thailand.ThailandPackage()
trip_to.detail()


import inspect
import random
print(inspect.getfile(random))
print(inspect.getfile(thailand))