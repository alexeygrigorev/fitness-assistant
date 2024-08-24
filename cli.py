import json
import uuid
import argparse

import requests
import questionary

import pandas as pd


def get_random_question(file_path):
    df = pd.read_csv(file_path)
    return df.sample(n=1).iloc[0]["question"]


def ask_question(url, question):
    data = {"question": question}
    response = requests.post(url, json=data)
    return response.json()


def send_feedback(url, conversation_id, feedback):
    feedback_data = {"conversation_id": conversation_id, "feedback": feedback}
    response = requests.post(f"{url}/feedback", json=feedback_data)
    return response.status_code


def main():
    parser = argparse.ArgumentParser(
        description="Interactive CLI app for continuous question answering and feedback"
    )
    parser.add_argument(
        "--random", action="store_true", help="Use random questions from the CSV file"
    )
    args = parser.parse_args()

    base_url = "http://localhost:5000"
    csv_file = "./data/ground-truth-retrieval.csv"

    print("Welcome to the interactive question-answering app!")
    print("You can exit the program at any time when prompted.")

    while True:
        if args.random:
            question = get_random_question(csv_file)
            print(f"\nRandom question: {question}")
        else:
            question = questionary.text("Enter your question:").ask()

        response = ask_question(f"{base_url}/question", question)
        print("\nAnswer:", response.get("answer", "No answer provided"))

        conversation_id = response.get("conversation_id", str(uuid.uuid4()))

        feedback = questionary.select(
            "How would you rate this response?",
            choices=["+1 (Positive)", "-1 (Negative)", "Pass (Skip feedback)"],
        ).ask()

        if feedback != "Pass (Skip feedback)":
            feedback_value = 1 if feedback == "+1 (Positive)" else -1
            status = send_feedback(base_url, conversation_id, feedback_value)
            print(f"Feedback sent. Status code: {status}")
        else:
            print("Feedback skipped.")

        continue_prompt = questionary.confirm("Do you want to continue?").ask()
        if not continue_prompt:
            print("Thank you for using the app. Goodbye!")
            break


if __name__ == "__main__":
    main()
