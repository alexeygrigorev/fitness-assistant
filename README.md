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


## Technologies

* [Minsearch](https://github.com/alexeygrigorev/minsearch) - for full-text search
* OpenAI as an LLM
* Flask as the API interface (see [Background](#background) for more information on Flask)



## Installing the dependencies

We use `pipenv` for managing dependencies and Python 3.12.

Make sure you have pipenv installed:

```bash
pip install pipenv
```

Installing the dependencies:

```bash
pipenv install --dev
```

## Running the application

Running the Flask application:

```bash
pipenv run python app.py
```

Testing it:

```bash
URL=http://localhost:5000

QUESTION="Is the Lat Pulldown considered a strength training activity, and if so, why?"

DATA='{
    "question": "'${QUESTION}'"
}'

curl -X POST \
  -H "Content-Type: application/json" \
  -d "${DATA}" \
  ${URL}/question
```

You will see sonething like the following in the response:

```json
{
  "answer": "Yes, the Lat Pulldown is considered a strength training activity. This classification is due to it targeting specific muscle groups, specifically the Latissimus Dorsi and Biceps, which are essential for building upper body strength. The exercise utilizes a machine, allowing for controlled resistance during the pulling action, which is a hallmark of strength training.",
  "conversation_id": "4e1cef04-bfd9-4a2c-9cdd-2771d8f70e4d",
  "question": "Is the Lat Pulldown considered a strength training activity, and if so, why?"
}
```

Sending feedback:

```bash
ID="4e1cef04-bfd9-4a2c-9cdd-2771d8f70e4d"

FEEDBACK_DATA='{
    "conversation_id": "'${ID}'",
    "feedback": 1
}'

curl -X POST \
  -H "Content-Type: application/json" \
  -d "${FEEDBACK_DATA}" \
  ${URL}/feedback
```

After sending it, you'll receive the acknowledgement:


```json
{
  "message": "Feedback received for conversation 4e1cef04-bfd9-4a2c-9cdd-2771d8f70e4d: 1"
}
```

Alternatively, you can use [test.py](test.py) for testing it:

```bash
pipenv run python test.py
```


## Code

The code for the application is in the
[`fitness_assistant`](fitness_assistant/) folder:

- [`app.py`](fitness_assistant/app.py)
- [`ingest.py`](fitness_assistant/ingest.py)
- [`minsearch.py`](fitness_assistant/minsearch.py)
- [`rag.py`](fitness_assistant/rag.py)


### Interface

We use Flask for serving the application as API.

Refer to ["Running the Application" section](#running-the-application) for more detail.


### Ingestion

The ingestion script is in [`ingest.py`](fitness_assistant/ingest.py).

Because we use an in-memory database minsearch as our
knowledge base, we run the ingestion script on the startup
of the application.

It's run inside [`rag.py`](fitness_assistant/rag.py) when we import it



## Experiments

For experiments, we use Jupyter notebooks. They are in the [`notebooks`](notebooks/) folder

To start jupyter, run:

```bash
cd notebooks
pipenv run jupyter notebook
```

We have the following notebooks:

* [`rag-test.ipynb`](notebooks/rag-test.ipynb): the RAG flow and evaluating the system
* [`evaluation-data-generation.ipynb`](notebooks/evaluation-data-generation.ipynb): generating the ground truth dataset for retrieval evaluation


### Retrieval evaluation

The basic approach - using `minsearch` without any boosting - gave the following metrics:

* hit_rate: 94%
* MRR: 82%

The improved vesion (with tuned boosting):

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

### RAG flow evaluation

We used the LLM-as-a-Judge metric to evaluate the quality
of our RAG flow

For gpt-4o-mini, in a sample with 200 records, we had:

* 167 (83%) `RELEVANT`
* 30 (15%) `PARTLY_RELEVANT`
* 3 (1.5%) `NON_RELEVANT`

We also tested gpt-4o:

* 168 (84%) `RELEVANT`
* 30 (15%) `PARTLY_RELEVANT`
* 2 (1%) `NON_RELEVANT`

The difference is far from significant, so we went with gpt-4o-mini.


## Monitoring


## Background

Here we provide background on some tech not used in the course
and links for futher reading.

### Flask

We use Flask for creating the API interface for our application.
It's a web application framework for Python: we can easily create
and endpoint for asking questions and use web clients (like
`curl` or `requests`) for communicating with it.

In our case, we can send the question to `http://localhost:5000/question`.

For more information, visit the [official Flask documentation](https://flask.palletsprojects.com/).