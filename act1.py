print("1. area of a circle")
print("2. area of a square")
print("3. area of a rectangle")
print("4. area of a triangle")

num = int(input("Choose a number: "))

if num == 1 or num == 2 or num == 3 or num == 4:
    if num == 1:
        print("You chose to compute for the area of a circle")
        radius = float(input("Input the value for a radius: "))
        pi = float(input("Input the value of Pi: "))
        answer1 = pi * (radius * radius)
        print("Area of the circle:" ,answer1)

    elif num == 2:
        print("You chose to compute for the area of a square")
        side = float(input("Input the value for the side: "))
        answer2 = side * side
        print("Area of the square:" ,answer2)

    elif num == 3:
        print("You chose to compute for the area of a rectangle")
        width = float(input("Input the value of the width: "))
        length = float(input("Input the value of the length: "))
        answer3 = width * length
        print("Area of the rectangle: ", answer3)

    elif num == 4:
        print("You chose to compute for the area of a triangle")
        base = float(input("Input the value of the base: "))
        height = float(input("Input the value of the height: "))
        answer4 = (base * height) / 2
        print("Area of the triangle: ",answer4)
else:
    print("Invalid choice. Please enter a number from 1 to 4.")
