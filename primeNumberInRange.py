# 10-50 prime numbers
import math
def isPrime(number):
	for i in range(2,int(math.sqrt(number))+1):
		if(number%i==0):
			return 0
	return 1

def primeNumberInRange(lower,higher):
	for i in range(lower,higher+1):
		if(isPrime(i)):	
			print(i,end=" ")

lower=10
higher=50
primeNumberInRange(lower,higher)


select * from Employee
where Salry>=50000

# select name from Student
# where name="Kavishankar" and substr(0,4)

# Employee number 1 
1 a 
1 a
1 a

1 a

select TOP 2 from Employee
where name='a' and id=1

