import csv
from genericpath import exists
from cv2 import meanShift
from django.http import HttpResponse
from django.shortcuts import render, redirect, reverse
from .forms import StudentModelForm, CustomUserCreationForm
from django.views import generic
from .models import Student, ImageForm,StudentAttendence
from django.contrib.auth.mixins import LoginRequiredMixin
import cv2
import os
from pathlib import Path
import numpy as np
import datetime
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.views import LogoutView



DIR = Path(__file__).resolve().parent
print(DIR)
IMAGE_DIR = Path(__file__).resolve().parent.parent

image_dir = os.path.join(IMAGE_DIR, "media")


haar_model =  os.path.join(IMAGE_DIR,'classifier/haarcascade_frontalface_default.xml')
# print(haar_model)

haar_cascade = cv2.CascadeClassifier(cv2.data.haarcascades+ 'haarcascade_frontalface_default.xml')
# Create your views here.

#class for signup view
class SignUpView(generic.CreateView):
    template_name = "registration/signup.html"
    form_class = CustomUserCreationForm


    def get_success_url(self):
        return reverse("login")


class StudentCreateView(LoginRequiredMixin,generic.CreateView):
    template_name = "ourapp/student_create.html"
    form_class = StudentModelForm

    # def post(self, request, *args, **kwargs):
    #     form_class = self.get_form_class()
    #     form = self.get_form(form_class)
    #     x = request.POST[]
    #     files = request.FILES.getlist('image')
    #     for f in files:
    #         file_instance = Student(image = f)
    #         form.save()
    #     return form
        # # else:
        #     return HttpResponse("<h1>The image couldnot be uploaded</h1>")

    def get_success_url(self):
        return reverse('ourapp:student-list')


class StudentListView(LoginRequiredMixin,generic.ListView):
    template_name = 'ourapp/student_list.html'
    queryset = Student.objects.all()
    context_object_name = "students"

class StudentUpdateView(LoginRequiredMixin,generic.UpdateView):
    template_name = 'ourapp/student_update.html'
    queryset = Student.objects.all()
    form_class = StudentModelForm
    context_object_name = "students"
    def get_success_url(self):
        return reverse('ourapp:student-list')


class StudentDeleteView(LoginRequiredMixin,generic.DeleteView):
    template_name = 'ourapp/student_delete.html'
    queryset = Student.objects.all()
    def get_success_url(self):
        return reverse('ourapp:student-list')



#logic to train model for face detection and making the lbph xml file 
@login_required
def trainmodel(request):
    if os.path.isfile(os.path.join(DIR, "classifier.xml")):
        os.remove(os.path.join(DIR, "classifier.xml"))
    queryset = Student.objects.all()
    for i in queryset:
        print(i.first_name)
        i.is_present = False
        print(i.is_present)
    # images_path = DIR/"media"
    # print(images_path)
    # print(image_dir)
    def train_classifier():
        # path = [os.path.join(data_dir, f) for f in os.listdir(data_dir)]
        # print(path)
        features = []
        ids = []
        for img in os.listdir(image_dir):
            # print(img)
            image_path = os.path.join(image_dir, img)
            # print(image_path)
            for i in os.listdir(image_path):
                final_image_path = os.path.join(image_path, i)
                print(final_image_path,'final_image_path')
                idt = int((final_image_path).split("_")[0][-1])
                print(idt,'idt')
                img=cv2.imread(final_image_path)
                gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
                equliimage =cv2.equalizeHist(gray)
                face_rect=haar_cascade.detectMultiScale(equliimage, scaleFactor=1.3, minNeighbors=5)
                
            # final_image_path = images_path/"img"
            # print(final_image_path)

        # img = Image.open(image).convert('L')
                for x,y,w,h in face_rect:
                    faces_region_of_int = equliimage[y:y+h, x:x+w]
                    features.append(faces_region_of_int)
                    ids.append(idt)
                    
        
    #     # id1s = os.path.split(image)  
        print(f'Length of  features={len(features)}')
        print(f'Length of  labels={len(ids)}')    
        ids_ary = np.array(ids)
  
        features_ary = np.array(features, dtype =object)

        # print(features_ary)
    
    # Train and save classifier
        clf = cv2.face.LBPHFaceRecognizer_create()
        clf.train(features_ary,ids_ary)
        # print(clf)
        clf.save(os.path.join(DIR, "classifier.xml"))

    train_classifier()
    messages.info(request, "The model has been trained successfully")
    return redirect('ourapp:student-list')


@login_required
def takeattendance(request):
    students = Student.objects.all()
    student_id = []
    for i in students:
        student_id.append(i.roll_no)
        my_student = Student.objects.filter(roll_no = i.roll_no)
        my_student.update(is_present = False)
        print(f'{i.is_present} {i.first_name}{i.roll_no}')
    def attendance(name,id):
        with open(os.path.join(DIR/'Atttendence.csv'), 'r+') as f:
            f.truncate()
            myDataList = f.readlines()
            nameList = []
            for line in myDataList:
                entry = line.split(',')
                nameList.append(entry[0])
            if name not in nameList:
                now_date=datetime.datetime.now()
                dtstring=now_date.strftime("%Y:%m:%d")
                f.writelines(f'\n{name},{dtstring},{id}')

    def draw_boundary(img, classifier, scaleFactor, minNeighbors, color, clf):
        gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        equliimage =cv2.equalizeHist(gray_img)
        features = classifier.detectMultiScale(equliimage, scaleFactor, minNeighbors)
    
        for (x,y,w,h) in features:
            cv2.rectangle(img, (x,y), (x+w,y+h), color, 2 )
        
            id, pred = clf.predict(equliimage[y:y+h,x:x+w])
            confidence = int(100*(1-pred/300))

            if id in student_id:
                if confidence > 70:
                    obj = Student.objects.filter(roll_no = id)
                    for i in obj:
                        names = i.first_name
                        obj.update(is_present = True)
                        # i.is_present = True
                    cv2.putText(img, str(names), (x,y-5), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 1, cv2.LINE_AA)
                    attendance(str(names),id)
                else:
                    cv2.putText(img, "UNKNOWN", (x,y-5), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,0,255), 1, cv2.LINE_AA)
            else:
                cv2.putText(img, "UNKNOWN", (x,y-5), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,0,255), 1, cv2.LINE_AA)
    
        return img




# loading classifier
    # faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

    clf = cv2.face.LBPHFaceRecognizer_create()
    clf.read(os.path.join(DIR, "classifier.xml"))

    video_capture = cv2.VideoCapture(0) #-1 for  linux and 0 for window and 1 for other multiple  camera

    while True:
        ret, img = video_capture.read()
        img = draw_boundary(img, haar_cascade, 1.3, 6, (0,255,0), clf)
        cv2.imshow("face Detection", img)
        
        if cv2.waitKey(5)  == 13:
            break

    video_capture.release()

    cv2.destroyAllWindows()

    messages.info(request, "Attendance has been taken successfully. Please check the attendance")
    return redirect('ourapp:view-attendance')


@login_required
def moreimages(request, pk):
    names = Student.objects.filter(id = pk)
    for i in names:
        first_name= i.first_name
        roll_no=i.roll_no
    if request.method == "POST":
        named = request.POST.get('namess')
        print(named)
        files = request.FILES.getlist('image')
        for f in files:
            ImageForm(stu_name = named, image_field = f,roll_no=roll_no).save()
        return redirect('ourapp:view-attendance') 
    
    context = {
        'first_name':first_name
    }
    return render(request, 'ourapp/imageform.html', context)

@login_required
def viewattendance(request):
    from datetime import datetime
    import pytz
    present_student = Student.objects.all()
    datetime_present = datetime.now(pytz.timezone('Asia/Kathmandu'))
    attendance_date = datetime_present.strftime('%Y:%m:%d %H:%M:%S')

    context = {
        'present_student':present_student,
        'attendance_date':attendance_date
    }
    return render(request, "ourapp/viewattendance.html", context)

@login_required
def exportattendance(request):
    response = HttpResponse(content_type = 'text/csv')
    response ['content-Disposition'] = 'attachement; filename = Attendance' + str(datetime.datetime.now())+ '.csv'
    
    writer = csv.writer(response)
    writer.writerow(['Name', 'Email', 'Roll number', 'Status','Date'])

    attendance = Student.objects.all()
    for i in attendance:
        if i.is_present == True:
            status = 'present'
        else:
            status = 'Absent'
        writer.writerow([i.first_name +' '+i.last_name, i.email, i.roll_no, status,str(datetime.datetime.now().strftime('%Y/%m/%d'))])

    return response

@login_required
def bulk_insert_attendence(request):
    
    attendance = Student.objects.all()
    student_list = []
    for i in attendance:
        if i.is_present == True:
            i.is_present =  i.is_present
        else:
             i.is_present = not i.is_present
        student_attendance = StudentAttendence(
            name=f'{i.first_name} {i.last_name}',
            roll_no=i.roll_no,
            age=i.age,
            phone_no=i.phone_no,
            email=i.email,
            date=datetime.datetime.now(),
            is_present=i.is_present
        )
        student_list.append(student_attendance)
    print(attendance,'studentsAttendance')
    StudentAttendence.objects.bulk_create(student_list)
    messages.info(request, "Attendance has been taken successfully. Please check the attendance")
    return redirect('ourapp:student-list')
