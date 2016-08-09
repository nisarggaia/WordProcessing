dict1 = {'a':1, 'b':2,'c':3,'d':4}

user_sum = sum([v for v in dict1.itervalues()])
print user_sum
#dict1.update((k, v/user_sum) for (k, v) in dict1.iteritems())

for (k, v) in dict1.iteritems():
    print k
    print v