def assertEquals(received, expected):
    
    global correct
    global cases
    
    if received == expected:
        message = 'Correct!'
        correct += 1
    else:
        message = f'Expected {expected} but received {received}'
    
    cases.append((message, received, expected))

    
    return (message, received == expected)