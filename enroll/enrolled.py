
from datetime import datetime
from enroll.models import enrollments, domainenrollment
from django.core.exceptions import ObjectDoesNotExist


class enrolled:

    def isenrolled(self, user, course):
        try:
            if not user.is_anonymous:
                courses = enrollments.objects.get(user=user, course=course)
                return courses
            else:
                return -1
        except ObjectDoesNotExist:
            return False

    def categoryenrolled(self, user, category):
        try:
            if not user.is_anonymous:
                courses = domainenrollment.objects.get(user=user, domain=category)
                if courses.expiry.replace(tzinfo=None) > datetime.now(tz=None):
                    return courses
                else:
                    return False
            else:
                return -1
        except ObjectDoesNotExist:
            return False

    def categoryenrollments(self,user):
        if not user.is_anonymous:
            return domainenrollment.objects.filter(user=user)
        else:
            return -1

    def getenrollments(self, user):
        if not user.is_anonymous:
            return enrollments.objects.filter(user=user)
        else:
            return -1
