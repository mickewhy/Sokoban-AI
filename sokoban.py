import copy
import time


class Color:
    # https://gist.github.com/fnky/458719343aabd01cfb17a3a4f7296797
    LIGHT_GRAY = "\033[97m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    GRAY = "\033[90m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


class Node:
    def __init__(self, state, parent, action):
        self.state = state
        self.parent = parent
        self.action = action


class StackFrontier:
    def __init__(self):
        self.frontier = []

    def add(self, node):
        self.frontier.append(node)

    def contains_state(self, state):
        return any(node.state == state for node in self.frontier)

    def empty(self):
        return len(self.frontier) == 0

    def remove(self):
        if self.empty():
            raise Exception(Color.RED + "Empty frontier" + Color.ENDC)
        else:
            node = self.frontier[-1]
            self.frontier = self.frontier[:-1]
            return node


class QueueFrontier(StackFrontier):

    def remove(self):
        if self.empty():
            raise Exception(Color.RED + "Empty frontier" + Color.ENDC)
        else:
            node = self.frontier[0]
            self.frontier = self.frontier[1:]
            return node


class SokobanAI:

    def __init__(self, start):

        # Determine start
        self.start = start

        # Determine height and width of puzzle
        self.height = len(self.start)
        self.width = len(self.start[0])

        self.solution = None

    def neighbors(self, state):
        # 👷 = WORKER
        # 📦 = BOX
        # ❌ = SPOT
        # 👷❌ = WORKER IN SPOT
        # 📦❌ = BOX IN SPOT
        # ⬛ = WALL
        #   = EMPTY

        result = []
        for i in range(self.height):
            for j in range(self.width):
                # If current position is worker or worker spot
                if state[i][j] == "👷" or state[i][j] == "👷❌":
                    # If worker is standing on spot, leaves behind spot. Otherwise leaves empty space.
                    leaveBehind = " " if state[i][j] == "👷" else "❌"
                    newState = copy.deepcopy(state)
                    # UP
                    if state[i - 1][j] == " ":
                        newState[i - 1][j] = "👷"
                        newState[i][j] = leaveBehind
                        result.append(("up", newState))
                    elif state[i - 1][j] == "📦" and 0 <= i - 2:
                        if state[i - 2][j] == " ":
                            newState[i - 2][j] = "📦"
                            newState[i - 1][j] = "👷"
                            newState[i][j] = leaveBehind
                            result.append(("up", newState))
                        elif state[i - 2][j] == "❌":
                            newState[i - 2][j] = "📦❌"
                            newState[i - 1][j] = "👷"
                            newState[i][j] = leaveBehind
                            result.append(("up", newState))
                    elif state[i - 1][j] == "❌":
                        newState[i - 1][j] = "👷❌"
                        newState[i][j] = leaveBehind
                        result.append(("up", newState))
                    elif state[i - 1][j] == "📦❌" and 0 <= i - 2:
                        if state[i - 2][j] == " ":
                            newState[i - 2][j] = "📦"
                            newState[i - 1][j] = "👷❌"
                            newState[i][j] = leaveBehind
                            result.append(("up", newState))
                        elif state[i - 2][j] == "❌":
                            newState[i - 2][j] = "📦❌"
                            newState[i - 1][j] = "👷❌"
                            newState[i][j] = leaveBehind
                            result.append(("up", newState))

                    newState = copy.deepcopy(state)
                    # DOWN
                    if state[i + 1][j] == " ":
                        newState[i + 1][j] = "👷"
                        newState[i][j] = leaveBehind
                        result.append(("down", newState))
                    elif state[i + 1][j] == "📦" and i + 2 < len(state):
                        if state[i + 2][j] == " ":
                            newState[i + 2][j] = "📦"
                            newState[i + 1][j] = "👷"
                            newState[i][j] = leaveBehind
                            result.append(("down", newState))
                        elif state[i + 2][j] == "❌":
                            newState[i + 2][j] = "📦❌"
                            newState[i + 1][j] = "👷"
                            newState[i][j] = leaveBehind
                            result.append(("down", newState))
                    elif state[i + 1][j] == "❌":
                        newState[i + 1][j] = "👷❌"
                        newState[i][j] = leaveBehind
                        result.append(("down", newState))
                    elif state[i + 1][j] == "📦❌" and i + 2 < len(state):
                        if state[i + 2][j] == " ":
                            newState[i + 2][j] = "📦"
                            newState[i + 1][j] = "👷❌"
                            newState[i][j] = leaveBehind
                            result.append(("down", newState))
                        elif state[i + 2][j] == "❌":
                            newState[i + 2][j] = "📦❌"
                            newState[i + 1][j] = "👷❌"
                            newState[i][j] = leaveBehind
                            result.append(("down", newState))

                    newState = copy.deepcopy(state)
                    # LEFT
                    if state[i][j - 1] == " ":
                        newState[i][j - 1] = "👷"
                        newState[i][j] = leaveBehind
                        result.append(("left", newState))
                    elif state[i][j - 1] == "📦" and 0 <= j - 2:
                        if state[i][j - 2] == " ":
                            newState[i][j - 2] = "📦"
                            newState[i][j - 1] = "👷"
                            newState[i][j] = leaveBehind
                            result.append(("left", newState))
                        elif state[i][j - 2] == "❌":
                            newState[i][j - 2] = "📦❌"
                            newState[i][j - 1] = "👷"
                            newState[i][j] = leaveBehind
                            result.append(("left", newState))
                    elif state[i][j - 1] == "❌":
                        newState[i][j - 1] = "👷❌"
                        newState[i][j] = leaveBehind
                        result.append(("left", newState))
                    elif state[i][j - 1] == "📦❌" and 0 <= j - 2:
                        if state[i][j - 2] == " ":
                            newState[i][j - 2] = "📦"
                            newState[i][j - 1] = "👷❌"
                            newState[i][j] = leaveBehind
                            result.append(("left", newState))
                        elif state[i][j - 2] == "❌":
                            newState[i][j - 2] = "📦❌"
                            newState[i][j - 1] = "👷❌"
                            newState[i][j] = leaveBehind
                            result.append(("left", newState))

                    newState = copy.deepcopy(state)
                    # RIGHT
                    if state[i][j + 1] == " ":
                        newState[i][j + 1] = "👷"
                        newState[i][j] = leaveBehind
                        result.append(("right", newState))
                    elif state[i][j + 1] == "📦" and j + 2 < len(state[i]):
                        if state[i][j + 2] == " ":
                            newState[i][j + 2] = "📦"
                            newState[i][j + 1] = "👷"
                            newState[i][j] = leaveBehind
                            result.append(("right", newState))
                        elif state[i][j + 2] == "❌":
                            newState[i][j + 2] = "📦❌"
                            newState[i][j + 1] = "👷"
                            newState[i][j] = leaveBehind
                            result.append(("right", newState))
                    elif state[i][j + 1] == "❌":
                        newState[i][j + 1] = "👷❌"
                        newState[i][j] = leaveBehind
                        result.append(("right", newState))
                    elif state[i][j + 1] == "📦❌" and j + 2 < len(state[i]):
                        if state[i][j + 2] == " ":
                            newState[i][j + 2] = "📦"
                            newState[i][j + 1] = "👷❌"
                            newState[i][j] = leaveBehind
                            result.append(("right", newState))
                        elif state[i][j + 2] == "❌":
                            newState[i][j + 2] = "📦❌"
                            newState[i][j + 1] = "👷❌"
                            newState[i][j] = leaveBehind
                            result.append(("right", newState))
        # Comment the line below to hide AI search text from terminal
        print(f"Result: {result}")
        return result

    def solve(self):
        """Finds a solution to the puzzle, if one exists."""

        # Keep track of number of states explored
        self.num_explored = 0

        # Initialize frontier to just the starting position
        start = Node(state=self.start, parent=None, action=None)
        frontier = QueueFrontier()
        frontier.add(start)

        # Initialize an empty explored set
        self.explored = []

        # Keep looping until solution found
        while True:

            # If nothing left in frontier, then no path
            if frontier.empty():
                raise Exception(Color.RED + "No solution possible" + Color.ENDC)

            # Choose a node from the frontier
            node = frontier.remove()
            self.num_explored += 1

            spotCount = 0
            for list in node.state:
                for element in list:
                    if element == "❌" or element == "👷❌":
                        spotCount += 1
            # If node is the goal, then we have a solution
            if spotCount == 0:
                actions = []
                cells = []
                while node.parent is not None:
                    actions.append(node.action)
                    cells.append(node.state)
                    node = node.parent
                actions.reverse()
                cells.reverse()
                self.solution = (actions, cells)
                return

            # Mark node as explored
            self.explored.append(node.state)

            # Add neighbors to frontier
            for action, state in self.neighbors(node.state):
                if not frontier.contains_state(state) and state not in self.explored:
                    child = Node(state=state, parent=node, action=action)
                    frontier.add(child)


# Terminal display
def placeEmoji(grid, x, y, emoji):
    if (grid[x][y]) != " " and emoji != " ":
        raise Exception(Color.RED + "Occupied space" + Color.ENDC)
    else:
        grid[x][y] = emoji


def printGrid(grid):
    line = "  "
    for j in range(int(columns)):
        line += "  " + chr(ord("A") + j)
    print(line)
    line = "   ┌"
    for j in range(int(columns) - 1):
        line += "──┬"
    line += "──┐"
    print(line)
    dividerLine = "   │"
    for j in range(int(columns)):
        dividerLine += "──│"
    for i in range(int(rows)):
        line = str(i + 1) + "  │"
        for j in range(int(columns)):
            if grid[i][j] == " ":
                line += "  │"
            else:
                if "👷" in grid[i][j]:
                    line += "👷│"
                elif "📦" in grid[i][j]:
                    line += "📦│"
                else:
                    line += grid[i][j] + "│"
        print(line)
        if i < int(rows) - 1:
            print(dividerLine)
    line = "   └"
    for j in range(int(columns) - 1):
        line += "──┴"
    line += "──┘"
    print(line)


rows = input("How many rows are in your puzzle?\n")
columns = input("How many columns are in your puzzle?\n")
puzzleGrid = [[" " for _ in range(int(columns))] for _ in range(int(rows))]

printGrid(puzzleGrid)
stillSetup = True
while stillSetup:
    emojiNum = int(
        input(
            f"What do you want to place?\n    {Color.BOLD}{Color.GREEN}1{Color.ENDC}. {Color.YELLOW}Worker\n    {Color.BOLD}{Color.GREEN}2{Color.ENDC}. {Color.LIGHT_GRAY}Box\n    {Color.BOLD}{Color.GREEN}3{Color.ENDC}. {Color.RED}Spot\n    {Color.BOLD}{Color.GREEN}4{Color.ENDC}. {Color.YELLOW}Worker in a Spot\n    {Color.BOLD}{Color.GREEN}5{Color.ENDC}. {Color.LIGHT_GRAY}Box in a Spot\n    {Color.BOLD}{Color.GREEN}6{Color.ENDC}. {Color.GRAY}Wall\n    {Color.BOLD}{Color.GREEN}7{Color.ENDC}. Empty Space{Color.ENDC}\n"
        )
    )
    if emojiNum > 10 or emojiNum < 1:
        raise Exception(Color.RED + "Index out of range" + Color.ENDC)
    emoji = ""
    match emojiNum:
        case 1:
            emoji = "👷"
        case 2:
            emoji = "📦"
        case 3:
            emoji = "❌"
        case 4:
            emoji = "👷❌"
        case 5:
            emoji = "📦❌"
        case 6:
            emoji = "⬛"
        case 7:
            emoji = " "
    printGrid(puzzleGrid)
    coord = input(
        f"Where would you like to place this block? ({Color.UNDERLINE}{Color.GREEN}e.g. a1{Color.ENDC})\n"
    ).lower()
    line = ""
    for j in range(int(columns)):
        line += chr(ord("A") + j)
    if not (coord[:1].lower() in line.lower()) or int(coord[1:]) < 1:
        raise Exception(Color.RED + "Index out of range" + Color.ENDC)
    placeEmoji(puzzleGrid, int(coord[1:]) - 1, ord(coord[:1]) - 97, emoji)

    printGrid(puzzleGrid)
    startSearch = input(
        f"Start search? {Color.UNDERLINE}{Color.GREEN}y{Color.ENDC}/{Color.RED}n{Color.ENDC}\n"
    ).lower()
    if startSearch != "y" and startSearch != "n":
        raise Exception(Color.RED + "Option unavailable" + Color.ENDC)
    if startSearch == "y":
        stillSetup = False

newGrid = [
    ["⬛" for _ in range(len(puzzleGrid[0]) + 2)] for _ in range(len(puzzleGrid) + 2)
]
for i in range(len(puzzleGrid)):
    for j in range(len(puzzleGrid[0])):
        newGrid[i + 1][j + 1] = puzzleGrid[i][j]

p = SokobanAI(newGrid)
timerStart = time.time()
p.solve()
timerEnd = time.time()
print(
    f"\n{Color.BOLD}{Color.UNDERLINE}{Color.GREEN}States explored{Color.ENDC}: {p.num_explored}\n"
)
print(
    f"{Color.BOLD}{Color.UNDERLINE}{Color.GREEN}Ideal move count{Color.ENDC}: {len(p.solution[0])}\n"
)
print(
    f"{Color.BOLD}{Color.UNDERLINE}{Color.GREEN}Solution{Color.ENDC}: {p.solution[0]}\n"
)
print(
    f"{Color.BOLD}{Color.UNDERLINE}{Color.GREEN}Solution found in{Color.ENDC}: {int((timerEnd-timerStart)/60)}m {int((timerEnd-timerStart)%60)}s\n"
)


displayMoves = input(
    f"Display moves in terminal? {Color.UNDERLINE}{Color.GREEN}y{Color.ENDC}/{Color.RED}n{Color.ENDC}\n"
).lower()
if displayMoves != "y" and displayMoves != "n":
    raise Exception(Color.RED + "Option unavailable" + Color.ENDC)
if displayMoves == "y":
    displayMoves = True
i = 0
while displayMoves and i < len(p.solution[1]):
    tempGrid = [
        [" " for _ in range(len(p.solution[1][0][0]) - 2)]
        for _ in range(len(p.solution[1][0]) - 2)
    ]
    for x in range(len(tempGrid)):
        for y in range(len(tempGrid[0])):
            tempGrid[x][y] = p.solution[1][i][x + 1][y + 1]
    print(f"Move {i+1}:")
    printGrid(tempGrid)
    if i + 1 == len(p.solution[0]):
        print(f"{Color.BOLD}{Color.GREEN}Solution reached{Color.ENDC}")
        displayMoves = False
    else:
        keepGoing = input(
            f"Press any key to keep going, or {Color.UNDERLINE}{Color.GREEN}q{Color.ENDC} to quit\n"
        ).lower()
        if keepGoing == "q":
            displayMoves = False
    i += 1
