# Course Scheduler

An optimized course scheduling system using linear programming to assign instructors to time slots while respecting constraints.

[![PuLP](https://img.shields.io/badge/PuLP-Linear_Programming-orange)](https://coin-or.github.io/pulp/)
## Features
+ **Constraint-based scheduling** with PuLP
+ **Input and output via JSON**
+ **Terminal UI**
+ **Printing as a table** with Tabulate
+ **Smart scheduling** with
  + Instructor availability constraints
  + Course and time preferences
  + Balancing over the week

## Installation
```bash
git clone https://github.com/Levon90210/course_scheduler.git
cd course_scheduler
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
pip install -r requirements.txt
```

## Usage
```bash
python main.py --input data/complex_input.json
```

## Input Format
Create a JSON file with this structure
```json
{
  "courses": [
    {
      "name": "Python",
      "times_per_week": 2,
      "preferred_time_slots": ["Monday 09:00-10:30"]
    }
  ],
  "instructors": [
    {
      "name": "Dr. Smith",
      "availability": ["Monday 09:00-10:30"],
      "preferred_courses": ["Python"],
      "max_hours": 8
    }
  ],
  "time_slots": [
    "Monday 9:00-10:30",
    "Tuesday 14:00-15:30"
  ]
}
```
\* Note that you can have any time slots but the start time shouldn't be earlier than `09:00`

## Project Structure
```
course_scheduler/
├── data/                # Sample input/output files
├── src/
│   ├── models/          # Data classes (Course, Instructor)
│   ├── utils/           # Helper functions
│   └── scheduler.py     # Core scheduling logic
├── main.py              # Entry point
└── requirements.txt     # Dependencies
```