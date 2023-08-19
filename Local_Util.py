def bruteforce(charset : str|list[str],max_length : int,initial : int =1,step : int =1,yield_empty : bool =True) -> str:
    '''
    ## A password generator

    Parameters
    ----------
    charset : str|list[str]
        The character set. Pass string for classic brute-force attack and list for dictionary attack.
    max_length : int
        The maximum length of the generated password.
    initial : int
        The index of the starting password (e.g. for "abc": 1 -> "a", 2 -> "b" and 4 -> "aa").
    step : int
        The stride (e.g. 1 -> a,b,c,d...   2 -> a,c,e,... ).
    yield_empty : bool
        If true an empty string will be generated first.
    
    Note that "initial" and "step" can be used for a multithreaded implementation
    '''
    # Check the validity of input
    if not (type(charset) in [str,list] and type(max_length)==int and type(initial)==int and type(step)==int): return
    carset_length = len(charset)
    if not (carset_length > 0 and step > 0 and max_length > 0 and initial > 0): return

    # Empty string
    if yield_empty: yield ""

    # Convert {initial} to base_{len(charset)}...
    state = []
    while True:
        # ...sort of   ( o.< )
        initial -= 1
        state.append(initial % carset_length)
        initial //= carset_length
        if initial == 0: break
    state_len = len(state)

    # Brute force loop
    while state_len <= max_length:
        # Build the string from scratch using the state
        string = ""
        for i in range(state_len-1,-1,-1):
            string += charset[state[i]]
        yield string

        # Update state variable
        carry_in = step
        for i in range(state_len):
            temp = state[i] + carry_in
            carry_in = temp // carset_length
            state[i] = temp % carset_length
            if carry_in == 0: break
        else:
            while (True):
                carry_in -= 1
                state.append(carry_in % carset_length)
                state_len += 1
                carry_in //= carset_length
                if carry_in == 0: break

def progressbar(progress : int|float, total : int|float, width : int=50, fill_char : str ="█") -> None:
    '''
    ## A simple progress bar

    Parameters
    ----------
    progress : int|float
        The amount of progress achieved. MUST be positive or zero.
    total : int|float
        The amount of total progress. MUST be positive.
    width : int
        The width of the progress bar. More specifically, the number of characters between the brackets of the progress bar.
    fill_char: str
        The character used to fill the progress bar.
    '''
    progress = min(progress, total)
    part = progress/total
    n_fill = int(part*width)
    print(f"\r["+ n_fill*fill_char + (width-n_fill)*" " + f"] {part*100:5.2f}%", end="")