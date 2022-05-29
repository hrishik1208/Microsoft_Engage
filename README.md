Attendance Portal
This project uses the library like opencv mediapipe cvzone,etc. Django is used as a backen framework in this project. Users are able to signup and login to their account. Teachers are able to create courses. Students are join the courses.

Note: this prototype is only made for Universities and colleges as it includes verification and identification of students by administration.

There is authentication system created for both Instructors and Students with different types of Interface. Both will be required to register in the portal in order to use it.
At the beginning of each semester/course, Instructors can create a course by just giving Course name and automatically a six-digit join code will be created. This join code will be required to students to join the that course. 
At the time of  joining the course from student’s side, the portal will capture the face of student along with it’s Id no. and also the join code sent by corresponding Instructor. 
This data will be sent to Pending request section on respective Instructor’s  portal. Instructor can verify the Id no. and student image from administration of College and University, and can either accept or reject his approval for joining Course. 

<hr>
Demo Video
Youtube: https://youtu.be/iMnCIT0iKfk

Drive: https://drive.google.com/file/d/1KVtR1j4G2VLMyefVszeApLYBScP6rGxA/view?usp=sharing
<hr>

Presentation Link :- https://docs.google.com/presentation/d/1nSNpLZrVvjRq3aJuDqFCagUEog4Vkoj5m4UZafhaunY/edit#slide=id.g12f87fdeb4e_0_0

<hr>

Demo User credentials

(you can also create new users if required)

Teacher
username: george (case sensitive) password:1234

Student
username: hrishik1208 (case sensitive) password:1234
 <hr>
 
Features

Teacher side :->

1.  Can create a Course and can automatically send invite main with join code to students for that course.

2.  Can delete a course and all it’s history.

3.  Can read details of each course in ‘my courses section’. Details include all registered students, course join code and course name. Instructor can also take actions like removing particular students from course or remove all at once.

4. In start attendance feature which is present in ‘my courses’ section, Instructors can publish attendance for each course with the option of time duration within which he wants students to mark attendance. After the time finishes, no more attendances will be accepted from student’s side. 

5.  Can use Geolocation Feature. This feature collects your location data from your device with the help of geolocation api. Once you click on allow, a map with the current location will be displayed below using Google maps javascript api. You can confirm your location from there.

6.  Then you will be prompted to enter the radius distance. This is the maximum distance from your location to 	which student can mark their attendance. 

  If location is displaying wrong then you need to check following things:
  
  	a. Check Your internet connectivity, location services and your browser should be in latest version.
    
		b. Open google maps, if it will shows same wrong location then, problem is with device settings.
    
		c. If it is so, then this link contains detailed information about it and how to fix it.
			https://support.google.com/maps/answer/2839911

    Currently Microsoft Edge is most compatible with geolocation api for Desktop. So it is recommended more. It might have a little location error but most precisely correct.

7.  Can see all attendances insights and details in records section. These include details about all attended and unattended students.

8.  There is an option to send email to all the unattended students at once. It will automatically send email to all unattended ones.



<hr>

Student Side:->

1.  Can Join the course just by submitting join code sent by Instructor. During this, Camera will capture student’s image along with College Id and process it to corresponding Instructor who have created that course for approval.
 
2.  Can view live classes of which attendance has been started and in which he/she has been successfully accepted by instructor that are running.

3.  Student can only see one attendance running live on it’s portal. This is done because, it will be ethical that same student does not attend multiple classes at the same time.

4.  Can see list of all courses he is successfully registered in ‘my courses’ section.

5.  Can mark attendance by just providing Face and palm. Providing both at the same time is necessary. If the face is not matched, then it gives error that “face does not matched”. If the Instructor has turned on Location feature, then attendance will be only marked if he is under the region specified by Instructor at the time of Starting attendance.

6.  Can See his/her all past attendance records of all the courses he is currently registered in. Once the course is deleted all history of it from both sides- ‘instructor’ and ‘student’ shall be deleted.

<hr>
Common :->

Authentication (signup, login, logout)

<hr>

How to run Github source code in localhost (python version=> Python 3.9.0)

1. Clone the github repository

2. Move into Microsoft_Engage directory

3. Move into Hello Directory

4. Install all dependencies

5. Run manage.py file


For better Understanding :

a. git clone https://github.com/hrishik1208/Microsoft_Engage

b. cd Microsoft_Engage

c. cd Hello

d. pip install –r requirements.txt 
    /** Alternative:=> pip install  django opencv-python cmake dlib face-recognition cvzone mediapipe numpy

e. python manage.py runserver


<hr>
Contact Details
Name: Hrishik Kanade Email: ashihrishik@gmail.com


