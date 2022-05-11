#saving images into media directpory part

# run()
# iu=Mains.objects.get(name="kshh")
# ipg=cv2.imread('static/1.jpg',1)
# print(iu.img)
# ipg=cv2.imread(str(iu.img),1)
# cv2.imshow('vacd',ipg)
# cv2.waitKey(0)
# cv2.destroyAllWindows()


# Detecting the faces.

# image = face_recognition.load_image_file("media/H1.jpg")
# face_locations = face_recognition.face_locations(image)
# print(face_locations)

# recognition part

# img1=cv2.imread('media/H1.jpg')
# img2=cv2.imread('media/Frame0.jpg')
# rgb_img1=cv2.cvtColor(img1,cv2.COLOR_BGR2RGB)
# img1_encoding=face_recognition.face_encodings(rgb_img1)[0]

# rgb_img2=cv2.cvtColor(img2,cv2.COLOR_BGR2RGB)
# img2_encoding=face_recognition.face_encodings(rgb_img2)[0]

# result = face_recognition.compare_faces([img1_encoding],img2_encoding)


# saving image to model part

# con=Mains(name="kah",img='Frame0.jpg')
# con.save()
