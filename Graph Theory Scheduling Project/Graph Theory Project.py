import numpy as np

def read_constraint_table(file_nb):
    """Reads the constraint table from a file and stores it in memory."""
    tasks = {}
    file_path = "Test constraint tables-20250318/table " + file_nb + ".txt"
    try:
        with open(file_path, 'r') as file:
            for line in file:
                values = list(map(int, line.split()))
                task, duration, *predecessors = values
                tasks[task] = {'duration': duration,
                               'predecessors': predecessors}
    except FileNotFoundError:
        print(f"Table {file_nb} not found.")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None
    return tasks


def build_value_matrix(tasks):
    """Builds the value matrix representation of the graph."""
    num_tasks = len(tasks)
    size = num_tasks + 2  # Adding fictitious tasks 0 and N+1
    matrix = np.full((size, size), '*', dtype=object)
    has_no_successors = list(range(1, num_tasks + 1))

    # Initialize start (0) and end (N+1) tasks
    for task, data in tasks.items():
        if not data['predecessors']:
            matrix[0][task] = 0  # Start task with 0 duration
        for pred in data['predecessors']:
            if pred in has_no_successors:
                has_no_successors.remove(pred)
            matrix[pred][task] = tasks[pred]['duration']
    for elt in has_no_successors:
        matrix[elt][size-1] = tasks[elt]['duration']

    return matrix


def display_matrix(matrix):
    """Displays the value matrix in a readable format."""
    disp_matrix = np.array(matrix.copy())
    vertices = [str(i) for i in range(len(disp_matrix))]
    vertices[0], vertices[-1] = 'α', 'ω' # Delete this line to display α as 0 & ω as N+1
    disp_matrix = np.insert(disp_matrix, 0, vertices, axis=1)
    vertices = np.insert(vertices, 0, '')
    disp_matrix = np.insert(disp_matrix, 0, vertices, axis=0)
    print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in disp_matrix]))


def has_negatives(matrix):
    """Determines whether a graph as edges with negative weights based on its value matrix."""
    try:
        result = False
        for i in range(len(matrix)):
            for j in range(len(matrix[i])):
                if matrix[i][j] != '*' and matrix[i][j] < 0:
                    result = True
                    break
        return result
    except TypeError:
        print("Error: Bad table formating. Later operations can malfunction.")
        return True


def is_cyclic(matrix):
    """Determines whether a graph is cyclic based on its adjacency matrix."""
    not_deleted = [i for i in range(len(matrix))]
    print("\nDetecting cycles with the elimination method...")
    while True:
        sources_and_sinks = []
        for i in not_deleted:
            if get_degree(0, matrix, not_deleted, i) == 0 or get_degree(1, matrix, not_deleted, i) == 0:
                sources_and_sinks.append(i)
        if 0 not in sources_and_sinks:
            print(f"Sources and sinks: {(', '.join(map(str, sources_and_sinks))).strip() if sources_and_sinks else 'none'}.", end=' ')
        else:
            print(f"Sources and sinks: α, ω.", end=' ')

        for elt in sources_and_sinks:
            not_deleted.remove(elt)
        if not sources_and_sinks:
            print("We stop here.")
            break
        print("We delete them and go on.")
    if not_deleted:
        print("There are still some vertices, so there is at least on cycle.")
        return True
    print("There are no vertices left, so there is no cycle.")
    return False


def get_degree(in_out, matrix, not_deleted, vertex):
    """Calculates the in (in_out = 0) or out (in_out = 1) degree of a vertex."""
    degree = 0
    if in_out:
        for i in not_deleted:
            if matrix[i][vertex] != '*':
                degree += 1
    else:
        for i in not_deleted:
            if matrix[vertex][i] != '*':
                degree += 1
    return degree


def ranks_matrix(tasks):
    """Returns the rank of the vertices of a given group of tasks."""
    ranks = {}
    visiting = set()  # Track nodes being visited (to detect cycles)
    path = []  # Keep track of path
    alpha = 'α'
    ranks[alpha] = 0

    print("\nStarting rank computation...")

    def dfs(task):
        """Recursively traverse the graph to calculate the rank of a given vertex."""

        if task in ranks:
            return ranks[task]

        visiting.add(task)
        path.append(task)
        predecessors = tasks[task]['predecessors'] if tasks[task]['predecessors'] else [alpha]
        print(f"Task {task} has predecessors: {','.join([str(e) for e in predecessors])}",end=' ')

        max_rank = max(dfs(pred) for pred in predecessors) #recursive call
        ranks[task] = max_rank + 1
        print(f"thus we assign rank {ranks[task]} to task {task}")
        visiting.remove(task)
        path.pop()
        return ranks[task]

    for task in tasks:
        dfs(task)

    max_value = max(ranks.values())
    ranks['ω'] = max_value + 1
    print(f"Assigned rank {ranks['ω']} to terminal node ω\n")

    sorted_by_ranks = {}
    for key in sorted(ranks, key=ranks.get):
        sorted_by_ranks[key] = ranks[key]

    return sorted_by_ranks


def add_omega_tasks(tasks):
    has_no_successors = list(range(1, len(tasks) + 1))
    for elt in tasks.keys():
        for pred in tasks[elt]['predecessors']:
            if pred in has_no_successors:
                has_no_successors.remove(pred)
    tasks['ω'] = {'duration': 0,
                   'predecessors': has_no_successors}
    return tasks


def display_ranks(ranks):
    """Displays vertices' ranks in a readable format."""
    N = len(ranks)
    classed_vertices = []
    for i in range(N):
        classed_vertices.append([v for v, r in ranks.items() if r == i])
    print('Rank:', end='\t ')
    tmp_str = ''
    for i in range(len(classed_vertices)):
        tmp_str += f'{i}\t'*len(classed_vertices[i])
    print(tmp_str[:-1])
    print('Vertex:', end='\t ')
    print(('\t'.join(['\t'.join([str(vertex) for vertex in vertices]) for vertices in classed_vertices])).strip())


def compute_earliest_latest_dates(tasks,ranks):
    """Computes the earliest and latest dates for each task in the project."""
    tasks=add_omega_tasks(tasks)
    earliest_dates = {}
    latest_dates = {'α':0, **{key:0 for key in ranks.keys()}}

    # Compute earliest dates calendar
    for task in ranks.keys():
        if task=='α' or not tasks[task]['predecessors']:
            earliest_dates[task]=0
        else:
            earliest_dates[task] = max(     #If there are more than 1 predecessor
                earliest_dates[pred] + tasks[pred]['duration'] for pred in tasks[task]['predecessors'])

    # Compute latest dates calendar
    for task in reversed(list(earliest_dates.keys())):
        if task=='ω':
            latest_dates[task] = earliest_dates[task]
        elif task == 'α':
            successors = [t for t in tasks if not tasks[t]['predecessors']]
            latest_dates[task] = min(latest_dates[succ] for succ in successors)
        else:
            successors = [t for t in tasks if task in tasks[t]['predecessors']]
            latest_dates[task] = min(latest_dates[succ] - tasks[task]['duration'] for succ in successors)

    return earliest_dates, latest_dates


def display_dates(earliest_dates, latest_dates):
    print('Earl.:', end='\t ')
    print('\t'.join(map(str, earliest_dates.values())))
    print('Latest:', end='\t ')
    print('\t'.join(map(str, latest_dates.values())))


def total_floats(earliest, latest):
    return [latest[i] - earliest[i] for i in earliest.keys()]


def free_floats(tasks, earliest,ranks):
    free = []
    print("\nStarting computation of free floats...")
    for task in ranks.keys():
        if task=='α':
            successors = [t for t in tasks if not tasks[t]['predecessors']]
            free.append(min(earliest[s] - earliest[task] for s in successors))
            print(f"For task α, free float is equal to {free[0]}")
        elif task=='ω':
            free.append('X')
            print(f"Task ω has no free float value thus we enter X")
        else:
            successors = [t for t in tasks if task in tasks[t]['predecessors']]
            free.append(min(earliest[s]-(earliest[task]+tasks[task]['duration']) for s in successors))
            print(f"Task {task} free float : {min(earliest[s] for s in successors)} - ({earliest[task]} + "
                  f"{tasks[task]['duration']}) = {min(earliest[s]-(earliest[task]+tasks[task]['duration']) for s in successors)}")
    return free


def display_floats(total, free):
    print('Total f.:', end='')
    print('\t'.join([str(elt) for elt in total]))
    print('Free f.:', end=' ')
    print('\t'.join([str(elt) for elt in free]))


def compute_critical_paths(tasks, earliest, latest):
    """Computes the longest path duration and returns the path with predecessors."""
    critical_tasks = [t for t in tasks if latest[t] - earliest[t] == 0]
    critical_paths = []
    start_tasks = [t for t in critical_tasks if not tasks[t]['predecessors']]
    for start in start_tasks:
        explore_critical_path(start, tasks, critical_tasks, ['α',start], critical_paths)

    path_durations = {tuple(path): sum(tasks[t]["duration"] for t in path if t in tasks) for path in critical_paths}
    max_duration = max(path_durations.values())
    longest_critical_paths = [list(path) for path, duration in path_durations.items() if duration == max_duration]

    return longest_critical_paths


def explore_critical_path(task, tasks, critical_tasks, current_path, critical_paths):
    successors = [succ for succ in [t for t in tasks if task in tasks[t]['predecessors']] if succ in critical_tasks]

    if not successors:  #Store the path only if it's complete
        critical_paths.append(current_path[:])  #Copy the full path, not a partial one
        return

    for succ in successors:
        current_path.append(succ)  #Extend the current path (not create a new one)
        explore_critical_path(succ, tasks, critical_tasks, current_path, critical_paths)
        current_path.pop()


def display_critical_path(crit_path):
    print('Critical path•s :', end=" ")
    for path in crit_path:
        for edge in range(len(path)-1):
            print(f'{path[edge]} → ',end="")
        print(f'{path[len(path)-1]}', end='    ')
    print()



def main():
    """Main loop allowing the user to process multiple constraint tables without restarting."""
    print("\nWelcome to our Graph Theory Project!")
    while True:
        print("—" * 75)
        file_nb = input(
            "Enter the wanted constraint table's number (or type 'exit' to quit): ").strip()
        if file_nb.lower() == 'exit':
            print("\n\nExiting program...\nGoodbye!")
            break

        tasks = read_constraint_table(file_nb)
        print()
        if tasks:
            matrix = build_value_matrix(tasks)
            print("Table n°"+file_nb+":\n")
            display_matrix(matrix)

            if has_negatives(matrix):
                print("\nThis graph is not a scheduling graph (contains negative weights).\n")
            elif is_cyclic(matrix):
                print("\nThis graph is not a scheduling graph (contains cycles).\n")
            else:
                print("\nThis graph is a scheduling graph.\n")
                ranks = ranks_matrix(tasks)
                earliest, latest = compute_earliest_latest_dates(tasks, ranks)
                total = total_floats(earliest, latest)
                free = free_floats(tasks, earliest,ranks)

                print()
                display_ranks(ranks)
                display_dates(earliest, latest)
                display_floats(total, free)
                critical_path = compute_critical_paths(tasks, earliest, latest)
                display_critical_path(critical_path)


if __name__ == "__main__":
    print("Launching program...")
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nExiting program...\nGoodbye!")