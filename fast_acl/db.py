# to simpilfy we'd just use memory as db, but this could be any other DB.

from fast_acl import models as models


class Database:
    users: list[models.User] = []
    students: list[models.Student] = []
    teachers: list[models.Teacher] = []
    admins: list[models.Admin] = []
    advisors: list[models.Advisor] = []
    classrooms: list[models.ClassRoom] = []
    relations: list[models.ClassRoomRelation] = []

    @classmethod
    def read_users(cls):
        return cls.users

    @classmethod
    def read_teachers(cls):
        return cls.teachers

    @classmethod
    def read_students(cls):
        return cls.students

    @classmethod
    def read_advisors(cls):
        return cls.advisors

    @classmethod
    def read_classrooms(cls):
        return cls.classrooms

    @classmethod
    def read_relations(cls):
        return cls.relations

    @classmethod
    def add_user(cls, user: models.User):
        cls.users.append(user)

    @classmethod
    def add_student(cls, student: models.Student):
        cls.students.append(student)

    @classmethod
    def add_teacher(cls, teacher: models.Teacher):
        cls.teachers.append(teacher)

    @classmethod
    def add_advisor(cls, advisor: models.Advisor):
        cls.advisors.append(advisor)

    @classmethod
    def add_classroom(cls, classroom: models.ClassRoom):
        cls.classrooms.append(classroom)

    @classmethod
    def add_relation(cls, relation: models.ClassRoomRelation):
        cls.relations.append(relation)
