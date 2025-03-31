# Grapy-Theory-Scheduling

## Overview
This project implements a scheduling system that processes constraint tables to construct directed graphs, verify their validity, and compute scheduling metrics such as earliest and latest dates, float times, and critical paths. The program reads a constraint table from a `.txt` file, processes it into a graph, and executes scheduling computations while ensuring correctness and usability.

## Features
1. **Reading and Displaying the Constraint Table:**
   - Reads constraint tables from `.txt` files.
   - Stores them in memory for further processing.
   - Displays the table contents on the screen.

2. **Graph Construction and Validation:**
   - Constructs a directed graph from the constraint table.
   - Represents the graph in a matrix form (value matrix).
   - Checks for the presence of cycles (circuit detection).
   - Ensures there are no negative-weight edges.

3. **Scheduling Computation:**
   - Computes the **topological order** of the graph (rank determination).
   - Computes the **earliest start times** and **latest start times** of tasks.
   - Calculates **float times** for each task.
   - Identifies **critical paths** in the project schedule.

4. **User Interaction and Looping:**
   - Allows users to test multiple constraint tables in a single execution.
   - Provides structured execution traces for better debugging and validation.

## Input Format
The constraint table is read from a `.txt` file, where:
- Each line represents a task with:
  - Task ID
  - Duration
  - Predecessor task IDs (if any)
- Example constraint table:
  ```
  1 9
  2 2
  3 3 2
  4 5 1
  5 2 1 4
  6 2 5
  7 2 4
  8 4 4 5
  9 5 4
  10 1 2 3
  11 2 1 5 6 7 8
  ```
- The table must include the fictitious tasks:
  - `0` (Start)
  - `N+1` (End), where `N` is the number of tasks.

## Execution Flow
The program follows this sequence:
1. Prompt user to choose a constraint table.
2. Read and store the table in memory.
3. Construct the scheduling graph and display it as a value matrix.
4. Check for cycle presence and negative edges.
5. If valid:
   - Compute task ranks.
   - Calculate earliest and latest start dates.
   - Compute float times.
   - Identify and display critical paths.
6. Repeat for another constraint table if requested by the user.

## Output Example
**Graph Representation:**
```
Value Matrix
   0  1  2  3  4  5  6
0  *  0  0  *  *  *  *
1  *  *  *  1  1  *  *
2  *  *  *  *  2  2  *
3  *  *  *  *  *  *  3
4  *  *  *  *  *  4  *
5  *  *  *  *  *  *  5
6  *  *  *  *  *  *  *
```

**Cycle Detection and Scheduling Validation:**
```
Entry points: 0
Eliminating entry points
Remaining vertices: 1 2 3 4 5 6
Entry points:  1 2
Eliminating entry points
Remaining vertices: 3 4 5 6
Entry points:  3 4
Eliminating entry points
Remaining vertices: 5 6
Entry points:  5
Eliminating entry points
Remaining vertices: 6
Entry points:  6
Eliminating entry points
Remaining vertices: None
-> There is no cycle
-> This is a valid scheduling graph
```

## Project Requirements
- The program should be implemented in **Python** (or C/C++/Java, based on team choice).
- The source code should be modular and well-documented.
- The program should handle multiple constraint tables without restarting.
- The execution traces should be clearly displayed.
- All output should be user-friendly and structured.

## Deployment and Testing
- Test files will be provided on **March 21**.
- The project submission deadline is **March 30** (before 00:00 on March 31).
- Teams must upload the following on Moodle:
  - **Source code** (well-commented, no compiled/execution files).
  - **All test `.txt` files** used for validation.
  - **Presentation slides** (ppt/pdf, can be provided during defense).
  - **Execution traces** as a `.txt` file.

## Evaluation Criteria
To score at least 10/20, the program must correctly implement:
1. Constraint table reading and in-memory storage.
2. Graph representation in matrix form.
3. Cycle detection and negative edge validation.
4. Rank computation for all vertices.

For higher scores:
5. Correct computation of earliest/latest start times.
6. Float calculation and critical path detection.
7. Well-structured execution traces.

## Team and Contribution
- Each team consists of **4-5 members**.
- Every team member must understand and be able to explain the code.
- The teacher can ask any team member questions during the **15-minute defense**.

## Notes
- The program should allow smooth transitions between different constraint tables.
- A backup system (extra laptop) is recommended for the defense.
- The project **must be rigorously tested** on various constraint tables before submission.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

