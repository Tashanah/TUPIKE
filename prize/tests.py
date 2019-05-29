from django.test import TestCase
from .models import Profile,Projects,Comments

class ProfileTestClass(TestCase):
    def setUp(self):
        self.Tash = Profile(first_name = 'Tash',last_name='Muhando',username='Tash.M',email='tmuhando99@gmail.com')

    def test_instance(self):
        self.assertTrue(isinstance(self.Tash,Profile))

    def test_save(self):
        self.Tash.save_profile()
        profiles = Profile.objects.all()
        self.assertTrue(len(profiles)>0)
 

 class ProjectsTestClass(TestCase):
    def setUp(self):
        self.Tash = Profile(first_name = 'Tash',last_name='Muhando',username='Tash.M',email='tmuhando99@gmail.com')
        self.Tash.save_profile()

        self.new_tag=tag(tag='testing')
        self.new_tag.save()

        self.new_project =Projects(caption="testing testing 1,2",profile=self.Tash)
        self.new_project.save()

        self.new_project.tag.add(self.new_tag)

    def tearDown(self):
        Profile.objects.all().delete()
        tag.objects.all().delete()
        Posts.objects.all().delete()    

    def test_projects(self):
        projects = Projects.projects()
        self.assertTrue(len(projects)>0)
