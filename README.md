# Face_Recognition-Attend
Automated Attendance via Facial Recognition Reat-Time Database

FaceRec-RealTimeAttendance is an automated system that leverages state-of-the-art facial recognition technology to monitor and log attendance in real-time.

**Features**
Real-Time Recognition: Instantly identify and log attendees.
Firebase Integration: Real-time storage and management of attendance records in Firebase.
Robust Accuracy: Minimize false positives and negatives with advanced algorithms.
Easy Setup: Seamless integration with existing camera systems.

**Installation**
Prerequisites
Python 3.x
Pycharm 
Visual Studio
Firebase account and set up a Firebase project

**Steps:**
Creating a Firebase account involves using a Google account and setting up a project within the Firebase platform. 
After that Run add datatodata base.
Run Encode Generator.
At last Run main.py

**Google Account:**

If you already have a Google account (like Gmail), you can use that.
If not, you'll need to create one at Google Account Creation.
Access Firebase:

Once you have a Google account, go to Firebase Console.
Click on "Sign in" in the upper-right corner.
Log in using your Google account credentials.
**Create a New Firebase Project:**

After logging in, you'll land on the Firebase console dashboard.
Click on the "Add project" card.
Provide a name for your project.
Choose your preferred settings for Google Analytics and accept the terms.
Click on "Create Project".
Project Dashboard:

After your project is created, you'll be taken to the dashboard for your new Firebase project.
From here, you can integrate various Firebase services like Realtime Database.
**Configure SDKs & Libraries:**

Depending on what platform or language you're working in (iOS, Android, Web, Node, Python, etc.), you can set up Firebase SDKs accordingly.
Under your project settings (the gear icon next to "Project Overview"), you'll find your project's unique configuration details, which you can use to initialize Firebase in your app or service.
**Security:**

Ensure that you set up security rules for any services you use, especially if using Firestore or Firebase Storage. By default, Firebase's database and storage rules might allow public access, and it's important to lock these down to prevent unauthorized access or data modification.



**Known Issues**
Lighting conditions can impact recognition accuracy.
Ensure the camera quality is clear for optimal results.
**License**
This project is licensed under the MIT License - see the LICENSE.md file for details.

**Acknowledgments**
Thanks to face_recognition library for the core recognition mechanism.
Firebase for providing a seamless real-time database solution.
All contributors who have participated in the evolution of this project.






