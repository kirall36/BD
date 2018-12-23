from peewee import *

database = MySQLDatabase('apteka', **{'charset': 'utf8', 'use_unicode': True, 'user': 'root', 'password': 'root'})


class UnknownField(object):
    def __init__(self, *_, **__): pass


class BaseModel(Model):
    class Meta:
        database = database


class Drug(BaseModel):
    description = CharField()
    iddrug = AutoField(column_name='idDrug')
    name = CharField()
    prescription = IntegerField(null=True)

    class Meta:
        table_name = 'drug'


class Symptom(BaseModel):
    description = CharField()
    idsymptom = AutoField(column_name='idSymptom')
    name = CharField()

    class Meta:
        table_name = 'symptom'


class DrugForASymptom(BaseModel):
    iddrug = ForeignKeyField(column_name='idDrug', model=Drug)
    idsymptom = ForeignKeyField(column_name='idSymptom', model=Symptom)

    class Meta:
        table_name = 'drug_for_a_symptom'
        indexes = (
            (('iddrug', 'idsymptom'), True),
        )
        primary_key = CompositeKey('iddrug', 'idsymptom')


class Sickness(BaseModel):
    description = CharField()
    idsickness = AutoField(column_name='idSickness')
    name = CharField()
    severity = IntegerField()

    class Meta:
        table_name = 'sickness'


class SymptomOfSickness(BaseModel):
    idsickness = ForeignKeyField(column_name='idSickness', model=Sickness)
    idsymptom = ForeignKeyField(column_name='idSymptom', model=Symptom)

    class Meta:
        table_name = 'symptom_of_sickness'
        indexes = (
            (('idsymptom', 'idsickness'), True),
        )
        primary_key = CompositeKey('idsickness', 'idsymptom')

