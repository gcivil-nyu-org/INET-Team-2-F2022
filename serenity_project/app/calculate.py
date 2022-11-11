from django.shortcuts import render, redirect
from sklearn import preprocessing
import numpy as np
from models import ScoreTable
import pandas as pd

# queryset = ScoreTable.objects.all()
#print(queryset)
A = np.array([[1,2,3,4],[5,6,7,8]])
print(A[:,2])