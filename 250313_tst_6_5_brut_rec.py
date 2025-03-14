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
    # אם כל הנקודות כבר במסלול, נחזיר אותו
    if not points:
        return [path]
    
    # נבדוק אם יש הצטלבות בין קווים
    for j in range(len(path)-1):
        if check_intersection(path[-1], path[0], path[j], path[j+1]):
            return []

            
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
    
    # מתחילים למצוא את הסידור עם המרחק הקצר ביותר
    min_distance = float('inf')  # מתחילים במרחק אינסופי
    best_tour = None
    
    for perm in all_permutations:
        # חישוב המרחק של המסלול הנוכחי
        current_distance = 0
        for i in range(len(perm) - 1):
            current_distance += distance(perm[i], perm[i + 1])
        
        # חישוב המרחק בין הנקודה האחרונה לנקודה הראשונה (לסגירת המעגל)
        current_distance += distance(perm[-1], perm[0])
        
        # אם המרחק הנוכחי הוא הקטן ביותר עד כה, נשמור את המסלול הזה
        if current_distance < min_distance:
            min_distance = current_distance
            best_tour = perm
    
    return best_tour, min_distance

# קריאת הנקודות מהקובץ
points = read_points_from_file("dots.txt")

# אם אין נקודות, נדפיס הודעת שגיאה
if not points:
    print("לא נמצאו נקודות בקובץ.")
else:
    # חישוב המסלול והמרחק המינימלי
    best_tour, min_distance = brute_force(points)

    # הצגת התוצאה
    print(f"מסלול אופטימלי: {best_tour}")
    print(f"מרחק מינימלי: {min_distance}")

    # הצגת המסלול
    tour_x, tour_y = zip(*best_tour)

    # חוזרים לנקודת המוצא בסוף
    tour_x = list(tour_x) + [tour_x[0]]
    tour_y = list(tour_y) + [tour_y[0]]

    plt.figure(figsize=(6,6))
    plt.scatter(*zip(*points), color='red', label='Points')  # ציור הנקודות
    plt.plot(tour_x, tour_y, color='blue', marker='o', label='Tour Path')  # ציור המסלול כולל החזרה לנקודת המוצא
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Traveling Salesman Problem - Brute Force')
    plt.grid(True)
    plt.legend()
    plt.show()


#################################################################################
Enter = input("Press Enter")