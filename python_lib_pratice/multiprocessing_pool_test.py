# from multiprocessing import Pool
from multiprocessing.dummy import Pool

pool = Pool(100)
f=lambda x:x+1
xl=range(100)
results = pool.map(f, xl)
print results
