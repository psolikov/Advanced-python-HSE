def fibonacci_n(n):
    if n <= 0:
        print(f"Bad")
        return
    if n == 1:
        return 0
    elif n == 2:
        return 1
    else:
        return fibonacci_n(n - 1) + fibonacci_n(n - 2)


def fibonacci_sequence(n):
    
    seq = []
    for i in range(1, n + 1):
        seq.append(fibonacci_n(i))
    return seq


def print_ast(fun):
    pass


if __name__ == '__main__':
    print(fibonacci_sequence(10))
