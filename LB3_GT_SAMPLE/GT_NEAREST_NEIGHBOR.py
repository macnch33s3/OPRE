import math
import matplotlib.pyplot as plt


def calculate_distance(point1, point2):
    # calculate distance between two points
    x1, y1 = point1
    x2, y2 = point2
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def nearest_neighbor(points, start_point_idx):
    # nearest neighbor heuristic
    remaining_points = set(points)
    current_point = points[start_point_idx]
    tour = [current_point]
    remaining_points.remove(current_point)

    while remaining_points:
        nearest_point = min(remaining_points, key=lambda point: calculate_distance(current_point, point))
        tour.append(nearest_point)
        current_point = nearest_point
        remaining_points.remove(nearest_point)
    return tour


def visualize_tour(tour):
    # Separate x and y coordinates for plotting
    x_coords = [point[0] for point in tour]
    y_coords = [point[1] for point in tour]
    labels = [f"Step {i + 1}" for i in range(len(tour))]
    # Plot the tour, points, and start point
    plt.figure(figsize=(8, 6))
    plt.plot(x_coords + [x_coords[0]], y_coords + [y_coords[0]], color='red', marker='o', linestyle='-', label='Tour')
    plt.scatter(x_coords, y_coords, color='blue', s=200, label='Points')  # Increase size (s) of points
    plt.scatter(tour[0][0], tour[0][1], color='green', marker='s', s=200,
                label='Start Point')  # Increase size (s) of start point

    # Set the axis limits and integer tick labels
    plt.xticks(range(int(min(x_coords)), int(max(x_coords)) + 2))
    plt.yticks(range(int(min(y_coords)), int(max(y_coords)) + 2))

    # plot labels
    for label, x, y in zip(labels, x_coords, y_coords):
        plt.annotate(label, (x, y), textcoords="offset points", xytext=(0, 10), ha='center', weight='bold')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Nearest Neighbor TSP Tour')
    plt.legend(loc='lower right')
    plt.grid(True)
    plt.show()


# Example list of points [(x1, y1), (x2, y2), ...]
points = [(0, 0), (1, 3), (4, 6), (7, 2), (9, 5)]

# Specify the start point
start_point = 0

# Calculate the nearest neighbor tour
tour = nearest_neighbor(points, start_point)

# visualize tour
visualize_tour(tour)