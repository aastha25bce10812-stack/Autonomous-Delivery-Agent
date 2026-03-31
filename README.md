# Autonomous-Delivery-Agent

## What This Project Does
The **Autonomous Delivery Agent** is a Python-based project that simulates how a delivery agent can find the most efficient path to reach a destination in a changing environment.It:

- Creates a **10x10 grid-based delivery world**
- Adds **static obstacles** like blocked roads or walls
- Includes **moving obstacles** to simulate dynamic challenges
- Uses **BFS, UCS, and A\*** algorithms to find paths
- Allows the agent to **replan its route** if the path gets blocked
- Compares which algorithm performs better in different situations

This project helps demonstrate how **AI-based pathfinding** can be useful in solving real-world delivery and navigation problems.

---
## Setup Instructions

1. **Clone the repository**
https://github.com/aastha25bce10812-stack/Autonomous-Delivery-Agent.git

3. **Create a virtual environment**
[ python -m venv venv ]

Activate the virtual environment: Windows: [ venv\Scripts\activate ]

3.**Install required libraries**

If you are using only the basic simulation code, no external libraries are required because it uses Python built-in modules.

If you are using the extended/project version with plotting and analysis, install:

[ pip install pandas matplotlib seaborn numpy ]
4. **Run the Project**
 [ python main.py ]

## How to Use
1.Run the Python file in VS Code, Google Colab, or any Python-supported IDE.

2. The program will create a grid environment with:
 - Start point
 - Goal point
 - Static obstacles
 - Moving obstacles
 - 
3. The delivery agent will try to find the best path from start to goal.
   
4. The following algorithms will run one by one:
  - BFS
  - UCS
  - A*

5. If a moving obstacle blocks the planned route, the agent will automatically recalculate a new        path.
 
6. The grid and movement will be shown directly in the terminal/console.
 
7. At the end, you can compare which algorithm performs more efficiently.

## Sample Output
Running BFS
BFS planned path: [(0, 0), (0, 1), (0, 2), ...]

Current Grid:
A 0 0 0 0 0 0 0 0 0
0 0 0 1 0 0 0 0 0 0
0 0 0 1 0 0 M 0 0 0
...

BFS: Goal reached in 18 steps!
BFS: Time taken = 2.1345 seconds

The same process is repeated for:

 -  UCS
 -  A*

## Technologies Used

- Python 3.12

- Google Colab
  
- GitHub

  
## Future Enhancements

-  Add a GUI version using Tkinter or Pygame
  
- Add colored visualization for better path display
  
- Introduce weighted roads and traffic simulation
  
-  Add real-world map integration

- Expand to multiple delivery agents
  
-  Improve obstacle movement for more realistic simulations
