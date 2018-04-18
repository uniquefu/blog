#Author:Jeff Lee

numbers ={'first':1,'second':2}

n_dict =dict(zip(numbers.values(),numbers.keys()))
#n_dict =dict([v,k] for k,v in numbers.items() )


#for k,v in numbers.items():
#    n_dict[v]=k

print(n_dict)


