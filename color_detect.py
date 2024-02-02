import csv
import cv2

camera = cv2.VideoCapture(0)

r = g = b = xpos = ypos = 0

# Read colors from CSV file manually
colors = []
with open('colors.csv', 'r') as csvfile:
    csvreader = csv.reader(csvfile)
    for row in csvreader:
        color_info = {
            "color_name": row[1],
            "hex": row[2],
            "R": int(row[3]),
            "G": int(row[4]),
            "B": int(row[5])
        }
        colors.append(color_info)

def get_color_name(R, G, B):
    minimum = 10000
    for color in colors:
        d = abs(R - color["R"]) + abs(G - color["G"]) + abs(B - color["B"])
        if d < minimum:
            minimum = d
            cname = color["color_name"] + '   Hex=' + color["hex"]
    return cname

def identify_color(event, x, y, flags, param):
    global b, g, r, xpos, ypos
    xpos = x
    ypos = y
    b, g, r = frame[y, x]
    b = int(b)
    g = int(g)
    r = int(r)

cv2.namedWindow('image')
cv2.setMouseCallback('image', identify_color)

while True:
    (grabbed, frame) = camera.read()
    frame = cv2.resize(frame, (900, frame.shape[0]))

    cv2.rectangle(frame, (20, 20), (800, 60), (b, g, r), -1)
    text = get_color_name(b, g, r) + '   R=' + str(r) + ' G=' + str(g) + ' B=' + str(b)
    cv2.putText(frame, text, (50, 50), 2, 0.8, (255, 255, 255), 2, cv2.LINE_AA)

    if r + g + b >= 600:
        cv2.putText(frame, text, (50, 50), 2, 0.8, (0, 0, 0), 2, cv2.LINE_AA)

    cv2.imshow('image', frame)

    if cv2.waitKey(20) & 0xFF == 27:
        break

camera.release()
cv2.destroyAllWindows()
