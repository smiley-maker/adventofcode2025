import time

def main():
    start_time = time.perf_counter()
    sum1 = 0
    sum2 = 0
    file = open("puzzle_two_input.txt","r")
    content = file.read().strip().split(",")
    for num_range in content:
        int_range = convert_range_to_int(num_range)
        sums = check_range(int_range)
        sum1 += sums[0]
        sum2 += sums[1]
    end_time = time.perf_counter()
    print(f"Part 1: {sum1}")
    print(f"Part 2: {sum2}")
    print(f"Time: {end_time-start_time}")

def convert_range_to_int(str_range:str) -> list:
    str_range = str_range.split("-")
    return [int(x) for x in str_range]

def check_range(int_range:list) -> list:
    range_sum1 = 0
    range_sum2 = 0
    for x in range(int_range[0],int_range[1]+1):
        str_x = str(x)
        l = len(str_x)
        
        #part 1
        if l % 2 == 0:  #if even
            low = x%(10**(l//2))
            high = low*(10**(l//2))
            if x == high + low:
                range_sum1 += x

        #part 2
        for i in range(l//2):
            if l % (i+1) == 0:
                sub_string = str_x[:i+1]
                repeats = False
                for j in range(i+1,l-i+1,i+1):
                    if sub_string != str_x[j:j+i+1]:
                        break
                    elif j == l-i-1:
                        repeats = True
            if repeats:
                range_sum2 += x
                break

        
    return [range_sum1,range_sum2]
        
    
main()

# t = [1188511880,1188511890]
# print(check_range(t))