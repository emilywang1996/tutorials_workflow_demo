from django.test import TestCase

# Create your tests here.
from django.urls import reverse
import pytest

#By providing a view name to the reverse() function, we can get the URL of the view.
#We will write a test to make sure that when we reverse the view named home, we get the expected path for the homepage on the website, which is "/". 

def test_homepage_access():
    url = reverse('home')
    assert url == "/"

# Integration Testing

#Integration tests determine whether multiple components in an application are able to integrate with one another.
#We will next write integration tests to see whether we can successfully interact with the database via Django models/ORM.

from tutorials.models import Tutorial

#fix the runtime error which can not access to the database in order to run the test
# @pytest.mark.django_db
# def test_create_tutorial():
#     tutorial = Tutorial.objects.create(
#         title='Pytest',
#         tutorial_url='https://pytest-django.readthedocs.io/en/latest/index.html',
#         description='Tutorial on how to apply pytest to a Django application',
#         published=True
#     )
#     assert tutorial.title == "Pytest"
#This test verifies that we are able to successfully create a Tutorial object in the database
#The reason is that pytest does not have access to the database in order to run the test.
#To fix this, we must again add the marker: @pytest.mark.django_db directly above the test function declaration:

# Using fixtures to test Django models 
@pytest.fixture
def new_tutorial(db):
    tutorial = Tutorial.objects.create(
        title='Pytest',
        tutorial_url='https://pytest-django.readthedocs.io/en/latest/index.html',
        description='Tutorial on how to apply pytest to a Django application',
        published=True
    )
    return tutorial

#This causes the new_tutorial() fixture function to be run first when either of these tests is run.
#The first test, test_search_tutorials(), simply checks that the object created by the fixture exists, by searching for an object with the same title.

def test_search_tutorials(new_tutorial):
    assert Tutorial.objects.filter(title='Pytest').exists()

#The second test, test_update_tutorial, updates the title of the new_tutorial object, saves the update, and asserts that a tutorial with the updated name exists in the database. 
# Note: Inside this test function's body, new_tutorial refers not to the new_tutorial fixture function, but to the object returned from that fixture function.

def test_update_tutorial(new_tutorial):
    new_tutorial.title = 'Pytest-Django'
    new_tutorial.save()
    assert Tutorial.objects.filter(title='Pytest-Django').exists()

# adding another fixture function that creates a different Tutorials object:
@pytest.fixture
def another_tutorial(db):
    tutorial = Tutorial.objects.create(
        title='More-Pytest',
        tutorial_url='https://pytest-django.readthedocs.io/en/latest/index.html',
        description='Tutorial on how to apply pytest to a Django application',
        published=True
    )
    return tutorial

# add a test that uses both fixtures as parameters:
def test_compare_tutorials(new_tutorial, another_tutorial):
    assert new_tutorial.pk != another_tutorial.pk
#understanding:
#Both the objects returned from the new_tutorial and another_tutorial fixtures are passed in.
#Then, the test asserts that the .pk attributes are not equal to the other.
#The .pk attribute in the Django ORM refers to the primary key of a database object, which is automatically generated when it is created.
# not equal, so passed