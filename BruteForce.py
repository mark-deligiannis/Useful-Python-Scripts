# A password generator. Arguments:
# -- charset:       The character set. Must be either string "abc" or list ["common ","word "]
# -- max_length:    The maximum length of the generated password
# -- initial:       The index of the starting password (e.g. for "abc": 1 -> "a", 2 -> "b" and 4 -> "aa")
# -- step:          The stride (e.g. 1 -> a,b,c,aa...   2 -> a,c,ab,... )
# -- yield_empty:   If true an empty string will be generated first.
# Note that "initial" and "step" can be used for a multithreaded implementation

def bruteforce(charset : str|list[str],max_length : int,initial : int =1,step : int =1,yield_empty : bool =True) -> str:
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


# For testing purposes
# Example usage: .\BruteForce.py abc 4 1 2 F
import sys
for i,x in enumerate(bruteforce(sys.argv[1],int(sys.argv[2]),int(sys.argv[3]),int(sys.argv[4]),sys.argv[5][0]=='T')):
    end = '\n' if i%10==9 else '\t'
    print(x, end=end)