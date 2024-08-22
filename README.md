# Fitness Assistant

## Problem description

Staying consistent with fitness routines is challenging,
especially for beginners. Gyms can be intimidating, and
personal trainers aren't always available.

The Fitness Assistant provides a conversational AI that helps
users choose exercises and find alternatives, making fitness
more manageable.

## Dataset

The dataset used in this project contains information about various exercises, including:

- **Exercise Name:** The name of the exercise (e.g., Push-Ups, Squats).
- **Type of Activity:** The general category of the exercise (e.g., Strength, Mobility, Cardio).
- **Type of Equipment:** The equipment needed for the exercise (e.g., Bodyweight, Dumbbells, Kettlebell).
- **Body Part:** The part of the body primarily targeted by the exercise (e.g., Upper Body, Core, Lower Body).
- **Type:** The movement type (e.g., Push, Pull, Hold, Stretch).
- **Muscle Groups Activated:** The specific muscles that are engaged during the exercise (e.g., Pectorals, Triceps, Quadriceps).
- **Instructions:** Step-by-step guidance on how to perform the exercise correctly.

The dataset was generated using ChatGPT and contains 207 records. It serves as the foundation for the Fitness Assistant's exercise recommendations and instructional support.

## Project overview

The Fitness Assistant is a RAG application for assisting users
with their fitness routines.

The main use cases include:

1. Exercise Selection: recommend exercises based type of activity, targeted muscle groups, or available equipment
2. Exercise Replacement: replace an exercise with a suitable alternatives
3. Exercise Instructions: perform a specific exercise
4. Conversational Interaction: make it easy to get the information without sifting through manuals or websites


## Running it

We use `pipenv` for managing dependencies and Python 3.12.

Make sure you have pipenv installed:

```bash
pip install pipenv
```

Installing the dependencies:

```bash
pipenv install
```

Running Jupyter notebook for experiments:

```bash
cd notebooks
pipenv run jupyter notebook
```



## Ingestion


## Evaluation 

For the code for evaluating the system, you can check 
the [notebooks/rag-test.ipynb](notebooks/rag-test.ipynb)
notebook.

We generated the ground truth dataset using this notebook:
[notebooks/evaluation-data-generation.ipynb](notebooks/evaluation-data-generation.ipynb)

### Retrieval

The basic approach - using minsearch without any boosting - gave the following metrics:

* hit_rate: 94%
* MRR: 82%

The improved vesion (with better boosting):

* hit_rate: 94%
* MRR: 90%

The best boosting parameters:

```python
boost = {
    'exercise_name': 2.11,
    'type_of_activity': 1.46,
    'type_of_equipment': 0.65,
    'body_part': 2.65,
    'type': 1.31,
    'muscle_groups_activated': 2.54,
    'instructions': 0.74
}
```

### RAG flow


## Monitoring

