# Initialize goal_state and cost
goal_state = {'A': 0, 'B': 0}
cost = 0

# Prompt user for vacuum starting location and status
vacuum_location = input("Enter vacuum's starting location (A or B): ").strip().upper()
status_A = int(input("Enter status of location A (Dirty=1, Clean=0): ").strip())
status_B = int(input("Enter status of location B (Dirty=1, Clean=0): ").strip())

# Initial state display
print("\nInitial State:")
print(f"Vacuum location: {vacuum_location}")
print(f"Location A status: {'Dirty' if status_A == 1 else 'Clean'}")
print(f"Location B status: {'Dirty' if status_B == 1 else 'Clean'}\n")

if vacuum_location == 'A':
    print("Vacuum at Location A")

    if status_A == 1:
        # Clean A
        goal_state['A'] = 0
        cost += 1
        print("Cleaned Location A")
        
        if status_B == 1:
            # Move to B
            cost += 1
            print("Moved to Location B")
            # Clean B
            goal_state['B'] = 0
            cost += 1
            print("Cleaned Location B")
        else:
            print("Location B is already clean")
    else:
        print("Location A is already clean")
        
        if status_B == 1:
            # Move to B
            cost += 1
            print("Moved to Location B")
            # Clean B
            goal_state['B'] = 0
            cost += 1
            print("Cleaned Location B")
        else:
            print("Location B is already clean")

else:  # Vacuum at B
    print("Vacuum at Location B")

    if status_B == 1:
        # Clean B
        goal_state['B'] = 0
        cost += 1
        print("Cleaned Location B")
        
        if status_A == 1:
            # Move to A
            cost += 1
            print("Moved to Location A")
            # Clean A
            goal_state['A'] = 0
            cost += 1
            print("Cleaned Location A")
        else:
            print("Location A is already clean")
    else:
        print("Location B is already clean")
        
        if status_A == 1:
            # Move to A
            cost += 1
            print("Moved to Location A")
            # Clean A
            goal_state['A'] = 0
            cost += 1
            print("Cleaned Location A")
        else:
            print("Location A is already clean")

print("\nFinal goal state:")
print(f"Location A: {'Clean' if goal_state['A'] == 0 else 'Dirty'}")
print(f"Location B: {'Clean' if goal_state['B'] == 0 else 'Dirty'}")
print(f"Total cost: {cost}")
