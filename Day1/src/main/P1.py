import os

N_GRADUATIONS = 100
DIAL_STARTING_POSITION = 50
DATA_FOLDER = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'data')

data = []
with open(os.path.join(DATA_FOLDER, 'input_p1.txt'), 'r') as file:
    data = file.readlines()
    data = [line.strip() for line in data]
    for line in data:
        if line[0] not in ('R', 'L'):
            raise ValueError("Input data must all start with 'R' and end with 'L', got {}".format(line))
        
print(data[:10])

diffs = [(1 if line[0] == 'R' else -1) * int(line[1:]) for line in data]

print(diffs[:10])

cumulative_summation = []
current_sum = DIAL_STARTING_POSITION
for diff in diffs:
    current_sum += diff
    cumulative_summation.append(current_sum)
print(cumulative_summation[:10])

n_divisible_by_n_graduations = sum(1 for x in cumulative_summation if x % N_GRADUATIONS == 0)
print("Number of zeros in cumulative summation:", n_divisible_by_n_graduations)
assert(n_divisible_by_n_graduations == 1097, "Expected 1097, got {}".format(n_divisible_by_n_graduations))

def n_sweep_zero(starting_point, diff, n_graduations):
    if diff == 0:
        return 0
    end_point = starting_point + diff
    low = min(starting_point, end_point)
    high = max(starting_point, end_point)
    first_multiple = ((low + n_graduations - 1) // n_graduations) * n_graduations
    if first_multiple > high:
        return 0
    last_multiple = (high // n_graduations) * n_graduations
    return ((last_multiple - first_multiple) // n_graduations) + 1
total_pass_zero = sum(n_sweep_zero(starting_point, diff, N_GRADUATIONS) for starting_point, diff in zip([DIAL_STARTING_POSITION] + cumulative_summation[:-1], diffs))
print("Total passes over zero:", total_pass_zero)
print(8198 + 1097)

if __name__ == "__main__":
    print("Day 1, Part 1")
    print("Number of instructions:", len(data))