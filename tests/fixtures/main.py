import os
import utils
import config

# Global variables (The agent should rename these!)
x = 25
y = "User_Admin"
a = [1, 2, 3]

def process(d):
    # This function uses the imported 'utils' library
    res = utils.calculate_metric(d, x)
    return res

def main():
    print("Starting process for: " + y)
    b = process(a)
    print("Result: " + str(b))

if __name__ == "__main__":
    main()