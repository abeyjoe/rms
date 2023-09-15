def gpa_calculator(grades_list):
    grades = []
    for i in grades_list:
        if i < 40:
            grades.append("F")
        elif i >= 40 and i < 45:
            grades.append("DE")
        elif i >= 45 and i < 50:
            grades.append("D")
        elif i >= 50 and i < 55:
            grades.append("CD")
        elif i >= 55 and i < 60:
            grades.append("C")
        elif i >= 60 and i < 65:
            grades.append("BC")
        elif i >= 65 and i < 70:
            grades.append("B")
        elif i >= 70 and i < 75:
            grades.append("AB")
        elif i >= 75:
            grades.append("A")			
    points = 0
    i = 0
    grade_c = {"A":5.0,"AB":4.5,"B":4.0,"BC":3.5,"C":3.0, "CD":2.5,"D":2.0,"DE":1.5,"F":0.0}
    if grades != []:
        for grade in grades:
            points += grade_c[grade]
        gpa = points / len(grades)
        return gpa
    else:
        return None
 
print(gpa_calculator([40,40,55,52,70,9,44,65,90]))
