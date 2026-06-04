def sort_numbers(numbers):
	"""Return two lists: (evens, odds) from the input list of integers."""
	evens = []
	odds = []
	for n in numbers:
		if n % 2 == 0:
			evens.append(n)
		else:
			odds.append(n)
	return evens, odds
if __name__ == "__main__":
	nums = [12, 7, 5, 18, 0, -3, 44, 21, 33, 100, 57, 2]
	evens, odds = sort_numbers(nums)
	print("Input:", nums)
	print("Evens:", evens)
	print("Odds:", odds)
