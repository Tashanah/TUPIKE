from django.test import TestCase
from .models import Profile,Projects,Comments
from django.contrib.auth.models import User

class ProfileTestClass(TestCase):
    def setUp(self):
        self.Tash = Profile(bio = 'Happy',profile_name='Tash.M',profile_photo='defaultl.jpeg')

    def test_instance(self):
        self.assertTrue(isinstance(self.Tash,Profile))

    def test_save(self):
        self.Tash.save_profile()
        profiles = Profile.objects.all()
        self.assertTrue(len(profiles)>0)
 

class ProjectsTestClass(TestCase):
    def setUp(self):
        self.Tash = User(bio = 'Happy',profile_name='Tash.M',profile_photo='defaultl.jpeg')
        self.Tash.save()

        # self.new_title=title(title='testing')
        # self.new_title.save()

        self.new_project =Projects(description="testing testing 1,2",profile=self.Tash,title="testing")
        self.new_project.save()

        self.new_project.title.add(self.new_title)

    def tearDown(self):
        Profile.objects.all().delete()
        tag.objects.all().delete()
        Projects.objects.all().delete()    

    def test_projects(self):
        projects = Projects.projects()
        self.assertTrue(len(projects)>0)
