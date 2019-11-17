from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Language(models.Model):
    name = models.CharField(max_length=32)

    def __str__(self):
        return self.name


class Level(models.Model):
    name = models.CharField(max_length=32)

    def __str__(self):
        return self.name

class UserType(models.Model):
    name = models.CharField(max_length=32)

    def __str__(self):
        return self.name

'''
    User model posiada pola:
        first_name, last_name, username, email, password
'''
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    userType = models.ForeignKey(UserType, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username + " - " + self.userType.name

# Klasa reprezentuje pojedyncze cwiczenie. Sklada sie z:
#   - autora
#   - tytulu
#   - języka programowania
#   - tresci cwiczenia
#   - poziomu zaawansowania
class Exercise(models.Model):
    author = models.ForeignKey(User, related_name="exercises", blank=True, null=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=128)
    language = models.ForeignKey(Language, related_name="language", blank=True, null=True, on_delete=models.CASCADE)
    content = models.TextField()
    level = models.ForeignKey(Level, related_name="level", blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.title + " - " + self.language + " - " + self.author.username


# Klasa reprezentuje test jednostkowy przypisany do konkretnego cwiczenia
#   - pathTofile - sciezka do pliku w ktorym zapisany jest test
#   - exercise - zadanie z ktorym test jest powiazany
class UnitTest(models.Model):
    pathToFile = models.FilePathField()
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)

# Klasa reprezentuje kolokwium, ktore sklada sie z kilku cwiczen
#   - name - nazwa kolokwium
#   - exercises - cwiczenia tworzace kolokwium 
class Test(models.Model):
    name = models.CharField(max_length=32)
    exercises = models.ManyToManyField(Exercise)

# Klasa reprezentuje rodzaj zadania (jest tylko Test lub Exercise)
#   - name - nazwa rodzaju zadania 
class TaskType(models.Model):
    name = models.CharField(max_length=32)

    def __str__(self):
        return self.name

# Klasa reprezentuje zadanie ktore mozna przydzielac studentom.
#   - author - autor zadania
#   - taskType - rodzaj zadania (Test/kolokwium lub Exercise/cwiczenie)
#   - title - tytul zadania
#   - exercise - klucz powaizany z obiektem typu Exercise (zalezne od taskType)
#   - test - klucz powiazany z obiektem typu Test (zalezne od taskType)
#   - isActive - czy jest aktywny
class Task(models.Model):
    author = models.ForeignKey(User, related_name="my_tasks", blank=True, null=True, on_delete=models.CASCADE)
    taskType = models.ForeignKey(TaskType, null=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=64, blank=True, null=True)
    exercise = models.ForeignKey(Exercise, null=True, on_delete=models.CASCADE)
    test = models.ForeignKey(Test, blank=True, null=True, on_delete=models.CASCADE)
    isActive = models.BooleanField(default=True)

    def __str__(self):
        return self.author.username + " - " + self.taskType.name + " - " + self.title


# Klasa reprezentuje grupe skladajaca sie z uzytkownikow (studentow)
#   - name - nazwa grupy
#   - owner - wlasciciel grupy
#   - users - uzytkownicy
#   - tasks - zadania przypisane konkretnej grupie
class Group(models.Model):
    name = models.CharField(max_length=32)
    owner = models.ForeignKey(User, related_name="group", blank=True, null=True, on_delete=models.CASCADE)
    users = models.ManyToManyField(User, related_name="membershipGroups", blank=True)
    tasks = models.ManyToManyField(Task, related_name="assignedTo", blank=True)

    def __str__(self):
        return self.name

# Klasa reprezentuje rozwiazanie nadeslane przez uzytkownika
#   - pathToFile - sciezka do pliku z rozwiazaniem
#   - task - zadanie ktorego tyczy sie rozwiazanie
#   - user - autor rozwiazania
#   - rate - ocena rozwaizania
class Solution(models.Model):
    pathToFile = models.FilePathField()
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rate = models.IntegerField()




