from flask_wtf import Form
from wtforms import StringField, TextAreaField, SelectField, validators
from wtforms.validators import Regexp, NoneOf
from MyModels import *


class BaseForm(Form):
    def finder(self, contents: list):
        for i in range(len(self)):
            if self.get_item(i).data:
                contents = list(filter(lambda x: str(self.get_item(i).data.lower()) in str(x.get_by_id(i)), contents))
        return contents


class DrugForm(BaseForm):
    name = StringField('name',
                       validators=[NoneOf(['"', "'", ";", "/", "\\"], message="\", ', ;, /, \\ are not allowed")])
    description = TextAreaField('description', validators=[Regexp(".*")])
    prescription = StringField('prescription', validators=[Regexp("[01]", message="0 - без рецета, 1 - по рецепту")])

    def get_item(self, index):
        return {
            0: self.name,
            1: self.description,
            2: self.prescription
        }[index]

    def __len__(self):
        return 3

    def create_instance(self, _id=0):
        if _id == 0:
            drug = Drug(name=self.name.data, description=self.description.data, prescription=self.prescription.data)
        else:
            drug = Drug.get_by_id(_id)
            drug.name = self.name.data
            drug.description = self.description.data
            drug.prescription = self.prescription.data
        drug.save()

    def delete_instance(self, _id):
        drug = Drug.get_by_id(_id)
        drug.delete_instance()


class SymptomForm(BaseForm):
    name = StringField('name',
                       validators=[NoneOf(['"', "'", ";", "/", "\\"], message="\", ', ;, /, \\ are not allowed")])
    description = TextAreaField('description', validators=[Regexp(".*")])

    def get_item(self, index):
        return {
            0: self.name,
            1: self.description
        }[index]

    def __len__(self):
        return 2

    def create_instance(self, _id=0):
        if _id == 0:
            sym = Symptom(name=self.name.data, description=self.description.data)
        else:
            sym = Symptom.get_by_id(_id)
            sym.name = self.name.data
            sym.description = self.description.data
        sym.save()

    def delete_instance(self, _id):
        sym = Symptom.get_by_id(_id)
        sym.delete_instance()


class SicknessForm(BaseForm):
    name = StringField('name',
                       validators=[NoneOf(['"', "'", ";", "/", "\\"], message="\", ', ;, /, \\ are not allowed")])
    description = TextAreaField('description', validators=[Regexp(".*")])
    severity = StringField('prescription', validators=[Regexp("[1-5]", message="Введите тяжесть от 1 до 5")])

    def get_item(self, index):
        return {
            0: self.name,
            1: self.description,
            2: self.severity
        }[index]

    def __len__(self):
        return 3

    def create_instance(self, _id=0):
        if _id == 0:
            sick = Sickness(name=self.name.data, description=self.description.data, severity=self.severity.data)
        else:
            sick = Sickness.get_by_id(_id)
            sick.name = self.name.data
            sick.description = self.description.data
            sick.severity = self.severity.data
        sick.save()

    def delete_instance(self, _id):
        sick = Sickness.get_by_id(_id)
        sick.delete_instance()


class Drug_for_Symptom_Form(Form):
    drug = SelectField('drug', validators=[validators.DataRequired()])
    symptom = SelectField('symptom', validators=[validators.DataRequired()])


class Symptom_for_Sickness_Form(Form):
    symptom = SelectField('symptom', validators=[validators.DataRequired()])
    sickness = SelectField('sickness', validators=[validators.DataRequired()])

