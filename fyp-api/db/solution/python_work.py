message ="Hello Python world!"
print(message)
name = "ada lovelace"
print(name.upper())
first_name = "ada"
last_name = "lovelace"
full_name = first_name +" "+ last_name
print(full_name)
bicycles = ['trek','cannondale','redline','specialized']
print(bicycles[-1])
message = "My first bicycles was a " + bicycles[0].title() + "."
print(message)
motorcycles = ['honda','yamaha','suzuki']
motorcycles.append('ducati')
print(motorcycles)
motorcycles.insert(0,'ducati')
print(motorcycles)
del motorcycles[0]
print(motorcycles)
popped_motorcycle = motorcycles.pop()
print(motorcycles)
print(popped_motorcycle)
motorcycles.remove('yamaha')
print(motorcycles)
cars=['bmw','audi','toyota','subaru']
cars.sort(reverse=True)
print(cars)
magicians = ['alice','david','carolina']
for magician in magicians:
	print(magician)
	print(magician.title() + ", that was a great trick")
print("Thank you, everyone. That was a great magic show!")