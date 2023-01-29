def prime(bound):
	prm = []
	for i in range(3, bound):
		for j in range(i):
			if i % d == 0:
				break
		if j == i-1:
			prm.append(i)
	return prm

if __name__ == "__main__":
	print(prime(10))
