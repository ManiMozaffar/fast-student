from fast_acl import models as models


class Database:
    users: list[models.User] = []
    students: list[models.User] = []
    teachers: list[models.Teacher] = []
    advisors: list[models.Advisor] = []
    classrooms: list[models.ClassRoom] = []
    relations: list[models.ClassRoomRelation] = []
