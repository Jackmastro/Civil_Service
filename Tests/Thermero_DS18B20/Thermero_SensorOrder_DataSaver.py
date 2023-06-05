import numpy as np

orderedSensorList = [  # address after 28- and physical counter
    ["00000e743370", 12],
    ["00000e74b77f", 3],
    ["00000e74378f", 18],
    ["00000e74c185", 7],
    ["00000e72abdd", 11],
    ["00000e74c839", 1],
    ["00000e737902", 5],
    ["00000e74c6ef", 4],
    ["00000e72d1a9", 9],
    ["00000e73f4ec", 2],
    ["00000e72dbe9", 15],
    ["00000e745a03", 16],
    ["00000e74667f", 6],
    ["00000e72e2b9", 10],  # unknown
    ["00000e737785", 19],
    ["00000e73f830", 14],
    ["00000e728757", 8],
    ["00000e744177", 20],
    ["00000e73e6af", 13],  # unknown
    ["00000e73ef44", 17]  # unknown
]

# Reduce the value of the second column by one using a list comprehension
orderedSensorList = [[address, value-1] for address, value in orderedSensorList]

# Print the updated second column
second_elements = [sublist[1] for sublist in orderedSensorList]
print(sorted(second_elements))

readDataList = np.random.rand(20, 1)

# Populate orderedDataList using advanced indexing
orderedDataList = np.zeros((20, 1))
orderedDataList[[sublist[1] for sublist in orderedSensorList]] = readDataList

print(orderedSensorList)
print(readDataList)
print(orderedDataList)