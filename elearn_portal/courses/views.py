# courses/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Course, Topic, CourseRating, Enrollment
from .forms import CourseForm, TopicForm

@login_required
def admin_dashboard(request):
    return render(request, 'courses/admin_dashboard.html')

@login_required
def staff_dashboard(request):
    return render(request, 'courses/staff_dashboard.html')

@login_required
def student_dashboard(request):
    return render(request, 'courses/student_dashboard.html')

@login_required
def add_course(request):
    if request.user.user_type != 'staff':
        return redirect('courses:course_list')
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES)
        if form.is_valid():
            course = form.save()
            return redirect('courses:course_detail', course_id=course.id)
    else:
        form = CourseForm()
    return render(request, 'courses/add_course.html', {'form': form})

@login_required
def add_topic(request, course_id):
    if request.user.user_type != 'staff':
        return redirect('courses:course_list')
    course = get_object_or_404(Course, pk=course_id)
    if request.method == 'POST':
        form = TopicForm(request.POST, request.FILES)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.course = course
            topic.save()
            return redirect('courses:course_detail', course_id=course.id)
    else:
        form = TopicForm()
    return render(request, 'courses/add_topic.html', {'form': form, 'course': course})

@login_required
def course_list(request):
    courses = Course.objects.all()
    return render(request, 'courses/course_list.html', {'courses': courses})

@login_required
def course_detail(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    topics = course.topics.all()  # Assuming related_name='topics' in Course model's ForeignKey
    return render(request, 'courses/course_detail.html', {'course': course, 'topics': topics})

@login_required
def edit_course(request, course_id):
    if request.user.user_type != 'staff':
        return redirect('courses:course_list')
    course = get_object_or_404(Course, pk=course_id)
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES, instance=course)
        if form.is_valid():
            form.save()
            return redirect('courses:course_detail', course_id=course.id)
    else:
        form = CourseForm(instance=course)
    return render(request, 'courses/edit_course.html', {'form': form, 'course': course})

@login_required
def delete_course(request, course_id):
    if request.user.user_type != 'staff':
        return redirect('courses:course_list')
    course = get_object_or_404(Course, pk=course_id)
    if request.method == 'POST':
        course.delete()
        return redirect('courses:course_list')
    return render(request, 'courses/delete_course.html', {'course': course})

@login_required
def rate_course(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    if request.method == 'POST':
        rating = request.POST.get('rating')  # Assuming you have a form field named 'rating'
        CourseRating.objects.create(course=course, user=request.user, rating=rating)
        # You can add logic to handle duplicate ratings or update existing ratings if needed
        return redirect('courses:course_detail', course_id=course.id)
    return render(request, 'courses/rate_course.html', {'course': course})

@login_required
def enroll_course(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    enrollment, created = Enrollment.objects.get_or_create(course=course, student=request.user)
    if created:
        # Handle success message or redirect
        pass  # Placeholder for handling enrollment success
    else:
        # Handle error message or redirect (if student is already enrolled)
        pass  # Placeholder for handling enrollment error
    return redirect('courses:course_detail', course_id=course.id)
