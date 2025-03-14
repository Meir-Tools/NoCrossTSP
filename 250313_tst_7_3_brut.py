import matplotlib.pyplot as plt
import os
# קביעת הנתיב לתקייה בה נמצא הסקריפט
script_dir = os.path.dirname(os.path.abspath(__file__))
# שינוי לתקייה של הסקריפט
os.chdir(script_dir)
print(os.getcwd())  # מדפיס את המיקום הנוכחי
#################################################################################

import numpy as np
import matplotlib.pyplot as plt
import itertools
import os

# קריאת הנקודות מקובץ "dots.txt"
def read_points_from_file(filename):
    points = []
    with open(filename, "r") as file:
        for line in file:
            try:
                x, y = map(float, line.strip().split(","))
                points.append((x, y))
            except ValueError:
                continue  # אם השורה לא חוקית, נדלג עליה
    return points

# פונקציה לחישוב המרחק בין שתי נקודות
def distance(p1, p2):
    return np.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)

# intersect
def check_intersection(p1, p2, p3, p4):
    """
    פונקציה לבדוק אם יש הצטלבות בין שני קווים (p1,p2) ו-(p3,p4).
    """
    def ccw(a, b, c):
        """פונקציה פנימית לבדיקת ccw - האם שלושה נקודות מסודרות נגד כיוון השעון."""
        return (c[1] - a[1]) * (b[0] - a[0]) > (b[1] - a[1]) * (c[0] - a[0])

    return ccw(p1, p3, p4) != ccw(p2, p3, p4) and ccw(p1, p2, p3) != ccw(p1, p2, p4)

def recursive_permutations(points, path=[]):
    # נבדוק אם יש הצטלבות בין קווים
    for j in range(len(path)-3):
        if check_intersection(path[j], path[j+1] , path[-2], path[-1] ):
            return []


    # אם כל הנקודות כבר במסלול, נחזיר אותו
    if not points:
        for j in range(len(path)-3):
            if check_intersection(path[j+1], path[j+2] , path[-1], path[0] ):
                return []
        return [path]
    
    all_permutations = []
    
    # עבור כל נקודה ברשימה, יוצרים את ההיתרים של שאר הנקודות
    for i in range(len(points)):
        current_point = points[i]
        remaining_points = points[:i] + points[i+1:]
        
        # קריאה רקורסיבית תוך העברת המסלול המעודכן
        all_permutations.extend(recursive_permutations(remaining_points, path + [current_point]))

    
    return all_permutations

# אלגוריתם Brute Force
def brute_force(points):
    # יוצרים את כל הסדרים האפשריים של הנקודות
    #all_permutations = list(itertools.permutations(points))
    all_permutations = recursive_permutations(points)
    

    
    # חישוב המרחק עבור כל סידור
    tours = []
    for perm in all_permutations:
        current_distance = 0
        for i in range(len(perm) - 1):
            current_distance += distance(perm[i], perm[i + 1])
        current_distance += distance(perm[-1], perm[0])  # חזרה לנקודת המוצא
        tours.append((perm, current_distance))
        

    
    return tours

# פונקציה לציור מסלול ושמירתו כקובץ תמונה
def plot_and_save(tour, idx, distance, folder="tours"):
    # יצירת תיקייה לשמירת התמונות
    if not os.path.exists(folder):
        os.makedirs(folder)

    # חישוב נקודות הציר X ו-Y
    tour_x, tour_y = zip(*tour)
    
    # החזרת המסלול לנקודת המוצא
    tour_x = list(tour_x) + [tour_x[0]]
    tour_y = list(tour_y) + [tour_y[0]]
    
    # ציור המסלול
    plt.figure(figsize=(6,6))
    plt.scatter(*zip(*tour), color='red', label='Points')  # ציור הנקודות
    plt.plot(tour_x, tour_y, color='blue', marker='o', label='Tour Path')  # ציור המסלול כולל החזרה לנקודת המוצא
    
    # הוספת כותרת עם אורך המסלול
    plt.title(f'Tour {idx+1} - Distance: {distance:.2f}')
    
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.grid(True)
    plt.legend()
    
    # שמירת התמונה
    plt.savefig(f"{folder}/tour_{idx+1}.png")
    plt.close()

# קריאת הנקודות מהקובץ
points = read_points_from_file("dots.txt")

# מתחילים למצוא את הסידור עם המרחק הקצר ביותר
min_distance = float('inf')  # מתחילים במרחק אינסופי
best_tour = None
best_tour_idx = None
    
# אם אין נקודות, נדפיס הודעת שגיאה
if not points:
    print("לא נמצאו נקודות בקובץ.")
else:
    # חישוב כל המסלולים האפשריים והמרחקים
    tours = brute_force(points)
    
    # שמירה של כל המסלולים כקובצי תמונה
    for idx, (tour, distance) in enumerate(tours):
        # אם המרחק הנוכחי הוא הקטן ביותר עד כה, נשמור את המסלול הזה
        if distance < min_distance:
            min_distance = distance
            best_tour = tour
            best_tour_idx = idx
        print(f"Saving tour {idx+1} with distance {distance:.2f}")
        plot_and_save(tour, idx, distance)

    print("המסלולים נשמרו בהצלחה בתיקיית 'tours'.")
    
    
    # הצגת התוצאה
    print(f"מסלול אופטימלי: {best_tour}")
    print(f"מרחק מינימלי: {min_distance}")

    # הצגת המסלול
    tour_x, tour_y = zip(*best_tour)

    # חוזרים לנקודת המוצא בסוף
    tour_x = list(tour_x) + [tour_x[0]]
    tour_y = list(tour_y) + [tour_y[0]]

    # ציור המסלול
    plt.figure(figsize=(6,6))
    plt.scatter(*zip(*tour), color='red', label='Points')  # ציור הנקודות
    plt.plot(tour_x, tour_y, color='blue', marker='o', label='Tour Path')  # ציור המסלול כולל החזרה לנקודת המוצא
    
    # הוספת כותרת עם אורך המסלול
    plt.title(f'Tour {best_tour_idx+1} - Distance: {min_distance:.2f}')
    
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.grid(True)
    plt.legend()
    #show
    plt.show()


#################################################################################
# Enter = input("Press Enter")