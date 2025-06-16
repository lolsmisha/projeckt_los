def quick_sort(arr, key=None):
    if len(arr) <= 1:
        return arr

    pivot_index = len(arr) // 2
    pivot = arr[pivot_index] if key is None else key(arr[pivot_index])

    left = []
    right = []

    for i, item in enumerate(arr):
        if i == pivot_index:
            continue

        current = item if key is None else key(item)
        if current < pivot:
            left.append(item)
        else:
            right.append(item)

    return quick_sort(left, key) + [arr[pivot_index]] + quick_sort(right, key)