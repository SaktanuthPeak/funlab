from flask import (
    Blueprint,
    render_template,
    redirect,
    request,
    url_for
)
from flask_login import current_user, login_required
from funlab import models
from .. import forms

module = Blueprint("course",__name__,url_prefix="/course")

@module.route("/", methods = ["GET","POST"])
def index():
    courses = models.Course.objects()
    return render_template("/courses/index.html",courses = courses)

@module.route("/create", methods = ["GET","POST"], defaults = dict(course_id = None))
@module.route("/<course_id>/edit", methods = ["GET","POST"])
def create_or_edit(course_id): 
    form = forms.courses.CourseForm()
    users = models.User.objects()
    course = None

    if course_id:
        course = models.Course.objects(id=course_id).first()
        form.professors.data = course.professor
        form = forms.courses.CourseForm(obj = course)
        
    form.professors.choices = [(user.id, user.get_fullname()) for user in users]   
    if not form.validate_on_submit():
        return render_template("/courses/create_or_edit.html", form = form)
    
    if not course_id:
        course = models.Course()

    user = models.User.objects.get(id = form.professors.data)
    form.populate_obj(course)
    course.professor = user
    course.save()
    
    return redirect(url_for("course.index"))
        
    