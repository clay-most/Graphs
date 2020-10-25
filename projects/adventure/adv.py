from room import Room
from player import Player
from world import World

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
room_graph = literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []

# directions and opposites "bread_crumbs" for back-tracking
directions = {"n": "s", "e": "w", "s": "n", "w": "e"}

##first pass 1004 moves
# bread_crumbs = []
# visited = {}
# while len(visited) < len(room_graph)-1:
#     if player.current_room.id not in visited:
#         visited[player.current_room.id]=player.current_room.get_exits()
#         if len(bread_crumbs)>0:
#             #removing exits we just came from so we don't visit them again
#             step_back = bread_crumbs[-1]
#             visited[player.current_room.id].remove(step_back)
       
#     while len(visited[player.current_room.id]) < 1:
#         prev = bread_crumbs.pop()
#         traversal_path.append(prev)
#         player.travel(prev)
#     current = visited[player.current_room.id].pop(0)
#     traversal_path.append(current)
#     bread_crumbs.append(directions[current])
#     player.travel(current)

##recursive 1000 moves
def recurse(current_room, visited = set()):
    bread_crumbs=[]
    for direction in player.current_room.get_exits():
        player.travel(direction)
        if player.current_room in visited:
            player.travel(directions[direction])
        else:
            visited.add(player.current_room)
            bread_crumbs.append(direction)
            bread_crumbs = bread_crumbs + \
                recurse(player.current_room, visited)
            player.travel(directions[direction])
            bread_crumbs.append(directions[direction])
    return bread_crumbs
traversal_path = recurse(player.current_room)



# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(
        f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
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
