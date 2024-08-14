import cv2
import mysql.connector
from mysql.connector import Error

def create_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='prasanth',
            database='image_db'
        )
        if connection.is_connected():
            print("Connected to MySQL database")
        return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

# Insert the image into the database
def insert_image(connection, image_name, image_data):
    try:
        cursor = connection.cursor()
        query = "INSERT INTO images (name, image) VALUES (%s, %s)"
        cursor.execute(query, (image_name, image_data))
        connection.commit()
        print("Image stored in database")
    except Error as e:
        print(f"Error inserting image: {e}")

# Convert image to binary data
def convert_to_binary_data(filename):
    with open(filename, 'rb') as file:
        binary_data = file.read()
    return binary_data

# Capture and store images
def capture_images():
    cam = cv2.VideoCapture(0)
    cv2.namedWindow("Image Capturing")

    img_counter = 0
    connection = create_connection()

    if connection is None:
        return

    while True:
        ret, frame = cam.read()

        if not ret:
            print("Failed to grab frame")
            break

        cv2.imshow("test", frame)

        k = cv2.waitKey(1)

        if k % 256 == 27:
            # ESC pressed
            print("Closing app")
            break

        elif k % 256 == 32:
            # SPACE pressed
            img_name = "opencv_frame_{}.png".format(img_counter)
            cv2.imwrite(img_name, frame)
            print("Image taken")

            # Convert the image to binary and store in database
            binary_data = convert_to_binary_data(img_name)
            insert_image(connection, img_name, binary_data)

            img_counter += 1

    cam.release()
    cv2.destroyAllWindows()

    if connection.is_connected():
        connection.close()
        print("MySQL connection closed")

# Run the capture function
capture_images()
