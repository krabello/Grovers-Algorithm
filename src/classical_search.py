def linear_search(arr, target):
    """Classical linear search implementation."""
    steps = 0
    for i in range(len(arr)):
        steps += 1
        if arr[i] == target:
            return i, steps
    return -1, steps