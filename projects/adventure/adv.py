from room import Room
from player import Player
from world import World

import sys
sys.setrecursionlimit(5000)

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []

class Stack():
    def __init__(self):
        self.stack = []
    def push(self, value):
        self.stack.append(value)
    def pop(self):
        if self.size() > 0:
            return self.stack.pop()
        else:
            return None
    def size(self):
        return len(self.stack)

s = []
visited = {}

def traverse_map(prev_room, current_room):
    # print()
    # print(f"You are here: {player.current_room.id}")
    # print(f"You think you are here: {current_room}")
    # print(f"You think you came from: {prev_room}")
    # print(f"Possible rooms are: {player.current_room.get_exits()}")
    if current_room not in visited:
        exits = player.current_room.get_exits()
        visited[current_room] = {}
        for direction in exits:
            visited[current_room][direction] = "?"

    if len(traversal_path) > 0:
        from_direction = traversal_path[-1]
    else:
        from_direction = None

    if from_direction == 'n':
        visited[current_room]['s'] = prev_room
        visited[prev_room]["n"] = current_room
    elif from_direction == 'e':
        visited[current_room]['w'] = prev_room
        visited[prev_room]["e"] = current_room
    elif from_direction == 'w':
        visited[current_room]['e'] = prev_room
        visited[prev_room]["w"] = current_room
    elif from_direction == 's':
        visited[current_room]['n'] = prev_room
        visited[prev_room]["s"] = current_room

    # checks what possible exits there are, add to stack if unknown room
    for direction in visited[current_room]:
        if visited[current_room][direction] == "?":
            player.travel(direction)
            next_room = player.current_room.id
            # print(f"you are adding to stack: current_room {current_room}, next_room {next_room}, direction {direction}")
            if (current_room, next_room, direction) not in s:
                s.append((current_room, next_room, direction))
                
            if direction == "n":
                player.travel("s")
            elif direction == "e":
                player.travel("w")
            elif direction == "s":
                player.travel("n")
            elif direction == "w":
                player.travel("e")

    # print(f"this is the stack: {s}")
    if len(s) > 0:
        info_for_next_room = s.pop()
        current_room_info = info_for_next_room[0]
        next_room_info = info_for_next_room[1]
        direction_info = info_for_next_room[2]
        # print(f"popped off stack. current room: {current_room_info}, next room: {next_room_info}, direction: {direction_info}")
        if direction_info in visited[current_room] and visited[current_room][direction_info] == "?":
            traversal_path.append(direction_info)
            # print(f"You travelled {direction_info} because its available and is unknown")
            player.travel(direction_info)
            traverse_map(current_room_info, next_room_info)
        else:
            # print("unknown not available, gotta go back")
            last_direction = -1
            back_tracking = []
            # print(f"you are here: {current_room}, where you need to be {current_room_info}")
            while (current_room_info != player.current_room.id):
                # print("enter while loop to go back")
                if len(traversal_path) > 0:
                    from_direction = traversal_path[last_direction]
                else:
                    from_direction = None

                next_direction = ""
                if from_direction == 'n':
                    next_direction = "s"
                elif from_direction == 'e':
                    next_direction = "w"
                elif from_direction == 'w':
                    next_direction = "e"
                elif from_direction == 's':
                    next_direction = "n"

                back_tracking.append(next_direction)
                last_direction -= 1
                # print(f"You travel {next_direction} because all rooms are explored and you're at a dead end.")
                player.travel(next_direction)
                # print(f"you are now here: {player.current_room.id}")

            # print(f"current traversal path: {traversal_path}")
            # print(f"back_tracking is {back_tracking}")
            for direction in back_tracking:
                traversal_path.append(direction)
            # print(f"traversal path after adding baCktracking: {traversal_path}")
            # print(f"info: current_room_info {current_room_info}, next room info: {next_room_info}, actual current room {player.current_room.id}")
            player.travel(direction_info)
            traversal_path.append(direction_info)
            traverse_map(current_room_info, next_room_info)
            
            
        
traverse_map(None, player.current_room.id)
# print(f"Stack: {s}")
# print(f"visited: {visited}")
# print(f"traversal path {traversal_path}")
# print(f"current room {player.current_room.id}")

"""
enter a room
has the current room been visited? 
if not: check all possible exits. add the room to visited dictionary and add all possible exits as values. {'n': '?', 's': '?', 'w': '?', 'e': '?'}
check the dictionary for the current values of all the rooms
get the last item in traversal path. if opposite direction of the last item in traversal path in the current room is unknown, set it to previous room
add all unknown directions to the stack
pop item off stack, add that direction to traversal path, then travel that direction

"""

# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")
