# OS Project: Virtual Memory Management
# Group Members: [Enter Your Names Here]

def display(frames):
    # Function to print the current status of memory frames
    print("Frames: ", end="")
    for i in frames:
        if i == -1:
            print("- ", end="")
        else:
            print(f"{i} ", end="")
    print() # Print new line

# 1. FIFO Algorithm
def fifo(n, pages):
    print("\n--- Running FIFO ---")
    
    memory = [-1] * n  # Initialize empty memory (-1 indicates empty slot)
    pointer = 0        # Pointer to track which frame to replace next
    faults = 0
    hits = 0
    
    for x in pages:
        print(f"Page {x} arrives: ", end="")
        
        if x in memory:
            print("HIT! (Page already exists)")
            hits += 1
        else:
            print("MISS! (Loading page into memory)")
            faults += 1
            memory[pointer] = x
            pointer = pointer + 1
            
            # If pointer exceeds frame size, reset it to 0 (Circular manner)
            if pointer == n:
                pointer = 0
                
        display(memory) # Show memory status after every step

    return faults, hits

# 2. LRU Algorithm
def lru(n, pages):
    print("\n--- Running LRU ---")
    
    memory = [] # Using a list to maintain the order of usage
    faults = 0
    hits = 0
    
    for x in pages:
        print(f"Page {x} arrives: ", end="")
        
        if x in memory:
            print("HIT!")
            hits += 1
            memory.remove(x) # Remove from current position
            memory.append(x) # Add to the end (Mark as most recently used)
        else:
            print("MISS!")
            faults += 1
            if len(memory) == n:
                memory.pop(0) # Remove the first element (Least Recently Used)
            memory.append(x)
            
        # Creating a temporary view to display empty slots as '-'
        temp_view = list(memory)
        while len(temp_view) < n:
            temp_view.append(-1)
        display(temp_view)

    return faults, hits

# 3. Optimal Algorithm
def optimal(n, pages):
    print("\n--- Running Optimal ---")
    
    memory = []
    faults = 0
    hits = 0
    
    # Loop using index (i) to check future pages
    for i in range(len(pages)):
        x = pages[i]
        print(f"Page {x} arrives: ", end="")
        
        if x in memory:
            print("HIT!")
            hits += 1
        else:
            print("MISS!")
            faults += 1
            
            if len(memory) < n:
                memory.append(x)
            else:
                # Logic to decide which page to remove
                # We check which page in memory will not be used for the longest time
                farthest = -1
                target = -1
                
                for page_in_mem in memory:
                    # Check when this page appears next in the future list
                    found = False
                    for j in range(i + 1, len(pages)):
                        if pages[j] == page_in_mem:
                            if j > farthest:
                                farthest = j
                                target = page_in_mem
                            found = True
                            break
                    
                    # If page is not found in future, it is the best candidate to remove
                    if found == False:
                        target = page_in_mem
                        break
                
                # If target is still -1 (e.g., initially full), remove the first one
                if target == -1:
                    target = memory[0]
                    
                # Perform replacement
                idx = memory.index(target)
                memory[idx] = x
                
        # Display logic
        temp_view = list(memory)
        while len(temp_view) < n:
            temp_view.append(-1)
        display(temp_view)

    return faults, hits

# --- MAIN PROGRAM ---
print("=== OS Virtual Memory Simulator ===")

# Taking inputs from the user
try:
    n = int(input("Enter number of Frames (e.g., 3): "))
    inp = input("Enter Pages (space separated, e.g., 1 2 3): ")
    # Converting input string into a list of numbers
    pages = []
    for num in inp.split():
        pages.append(int(num))
except:
    print("Invalid Input! Please enter numbers only.")
    exit()

while True:
    print("\nSelect Algorithm:")
    print("1. FIFO")
    print("2. LRU")
    print("3. Optimal")
    print("4. Compare All")
    print("5. Exit")
    
    choice = input("Enter your choice (1-5): ")
    
    total = len(pages)
    
    if choice == '1':
        f, h = fifo(n, pages)
        print(f"\nResult: Total Faults: {f}, Total Hits: {h}")
        print(f"Hit Ratio: {round((h/total)*100, 2)}%")
        
    elif choice == '2':
        f, h = lru(n, pages)
        print(f"\nResult: Total Faults: {f}, Total Hits: {h}")
        print(f"Hit Ratio: {round((h/total)*100, 2)}%")
        
    elif choice == '3':
        f, h = optimal(n, pages)
        print(f"\nResult: Total Faults: {f}, Total Hits: {h}")
        print(f"Hit Ratio: {round((h/total)*100, 2)}%")
        
    elif choice == '4':
        # Run all three to compare performance
        f1, h1 = fifo(n, pages)
        f2, h2 = lru(n, pages)
        f3, h3 = optimal(n, pages)
        
        print("\n=== Final Comparison ===")
        print(f"FIFO    -> Faults: {f1}, Hits: {h1}")
        print(f"LRU     -> Faults: {f2}, Hits: {h2}")
        print(f"Optimal -> Faults: {f3}, Hits: {h3}")
        
    elif choice == '5':
        print("Exiting program...")
        break
    else:
        print("Invalid choice, please try again.")