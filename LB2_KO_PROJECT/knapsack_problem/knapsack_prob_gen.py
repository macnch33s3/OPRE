# Generator für Kapazitäts-Knapsack-Instanzen (CAP_KNAPSACK)
# Filename: PROG_KNAPSACK_PROB_GEN.py
# Dieses Skript generiert zufällige Problem-Instanzen für das Kapazitäts-Knapsack-Problem (CAP_KNAPSACK). 
# Dabei werden eine definierte Anzahl von Items mit zufälligem Gewicht und abgeleitetem Wert erzeugt und 
# in eine standardisierte .ks-Datei geschrieben. Die erzeugten Instanzen können für Experimente mit 
# Heuristiken oder exakten Lösungsverfahren verwendet werden.
#
# Funktionen:
# - create_knapsack_problem(): Erzeugt eine einzelne Knapsack-Instanz und schreibt diese in eine Datei.
# - main(): Generiert mehrere Instanzen mit vordefinierten Parametern zur Demonstration.
#
# Format der Ausgabedatei:
# - NAME, TYPE, COMMENT, NUM_ITEMS, KNAPSACK_CAPACITY
# - Auflistung der Items mit ID, Gewicht und Wert
# - Abschluss durch 'EOF'
#
# Hinweis: Dieser Code wird ohne Gewähr bereitgestellt. Für Fehler oder Folgeschäden wird keine Haftung übernommen. 
# Feedback, Anregungen oder Hinweise auf Verbesserungsmöglichkeiten sind jederzeit willkommen!
#
# Autor: Fabian Leuthold, Ostschweizer Fachhochschule, fabian.leuthold@ost.ch
# Version: 1.0
# Datum: 05.08.2025

import random
import math

def create_knapsack_problem(knapsack_capacity, num_items, value_range, test_name="test", write=False):
    """
    Generate a knapsack problem instance

    :param knapsack_capacity: knapsack capacity
    :param num_items: number of items
    :param value_range: tuple containing the range (a, b) for the item values
    :param test_name: the name of the instance
    :return: nothing, write the file
    """
    # Generiere zufällige Gewichte und Werte für die Items
    items = []
    max_weight = 0.6 * knapsack_capacity
    file_name = "./data/" + test_name + "_" + str(num_items) + ".ks"
    name = test_name + "_" + str(num_items)

    comment = f"Pack {num_items} items into a knapsack with max_cap={knapsack_capacity} (Leuthold)"

    for i in range(1, num_items + 1):
        weight = round(random.uniform(1.0, max_weight), 2)
        value = round(weight + max_weight / 10, 2)
        items.append((i, weight, value))

    problem_text = (
        f"NAME: {name}\n"
        f"TYPE: CAP_KNAPSACK\n"
        f"COMMENT: {comment}\n"
        f"NUM_ITEMS: {num_items}\n"
        f"KNAPSACK_CAPACITY: {knapsack_capacity}\n"
        f"ITEMS_ID_WEIGHT_VALUE\n"
    )

    for item in items:
        problem_text += f"{item[0]} {item[1]} {item[2]}\n"

    problem_text += "EOF\n"

    if write:
        with open(file_name, "w") as file:
            file.write(problem_text)
        print(f"Knapsack problem file '{file_name}' created successfully.")
        return None
    else:
        return problem_text


def main():
    create_knapsack_problem(knapsack_capacity=20, num_items=8, value_range=(0.29, 38.73), test_name="CAP_KS")
    create_knapsack_problem(knapsack_capacity=20, num_items=48, value_range=(0.29, 38.73), test_name="CAP_KS")
    create_knapsack_problem(knapsack_capacity=50, num_items=140, value_range=(2.78, 38.73), test_name="CAP_KS")
    create_knapsack_problem(knapsack_capacity=200, num_items=2844, value_range=(12.1, 50.00), test_name="CAP_KS")


if __name__ == "__main__":
    main()
