from flask import Flask, render_template, flash, redirect, url_for, request
from MyModels import *
from forms import *

form_dict = {
        "drug": DrugForm,
        "symptom": SymptomForm,
        "sickness": SicknessForm
    }

instance_dict = {
    "drug": Drug,
    "symptom": Symptom,
    "sickness": Sickness
}

data = {
        0: 'name',
        1: 'description',
        2: 'prescription'
    }

data_sick = {
        0: 'name',
        1: 'description',
        2: 'severity'
}

statistics_dict = {
    "drugs": len(Drug.select()),
    "symptoms": len(Symptom.select()),
    "sicknesses": len(Sickness.select()),
    "drugforsick": len(Drug.select().join(DrugForASymptom).join(Symptom).join(SymptomOfSickness).join(Sickness))
    }

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

'''my_db = MySQLDatabase(
    'apteka',
    user='root',
    password='root',
    host='127.0.0.1',
    port=3306'''

'''select d.*, s.name
 from drug d
join drug_for_a_symptom ds
 on ds.idDrug = d.idDrug
join symptom s
 on s.idSymptom = ds.idSymptom'''


@app.route('/', methods=['GET', 'POST'])
def index():
    drugs = Drug.select()
    symptoms = Symptom.select()
    sicknesses = Sickness.select()
    flash('Hello')
    return render_template("tables.html", drugs=drugs, symptoms=symptoms, sicknesses=sicknesses, statistics_dict=statistics_dict)


@app.route('/drugforsymandsick', methods=['GET', 'POST'])
def test():
    drugs = (
    Drug.select(Drug.iddrug, Drug.name, Symptom.name.alias('symname'), Sickness.name.alias('sickname')).
        join(DrugForASymptom).join(Symptom).join(SymptomOfSickness).join(Sickness).objects())
    return render_template("drug_for_symandsick.html", drugs=drugs, statistics_dict=statistics_dict)


@app.route("/create/<instance>", methods=["GET", "POST"])
def create(instance):
    form = form_dict[instance.lower()]
    form = form()
    if form.validate_on_submit():
        form.create_instance()
        return redirect(url_for('index'))
    return render_template("create.html", title='Create', form=form, instance=instance.lower(), statistics_dict=statistics_dict)


@app.route('/createdrugforsym/', methods=['GET', 'POST'])
def drugforsym():
    form = Drug_for_Symptom_Form()
    form.drug.choices = [(drug.iddrug, drug.name) for drug in Drug.select()]
    form.symptom.choices = [(symptom.idsymptom, symptom.name) for symptom in Symptom.select()]
    drugsyms = Drug.select(Drug.name, Symptom.name.alias('symname')).join(DrugForASymptom).join(Symptom).objects()
    if request.method == 'POST':
        DrugForASymptom.insert(iddrug=form.drug.data, idsymptom=form.symptom.data).execute()
        return redirect(url_for('index'))
    return render_template("createdrugforsym.html", form=form, drugsyms=drugsyms, statistics_dict=statistics_dict)


@app.route("/createsymforsick/", methods=['GET', 'POST'])
def symforsick():
    form = Symptom_for_Sickness_Form()
    form.symptom.choices = [(symptom.idsymptom, symptom.name) for symptom in Symptom.select()]
    form.sickness.choices = [(sickness.idsickness, sickness.name) for sickness in Sickness.select()]
    symsicks = Symptom.select(Symptom.name, Sickness.name.alias('sickname')).join(SymptomOfSickness).join(Sickness).objects()
    if request.method == 'POST':
        SymptomOfSickness.insert(idsymptom=form.symptom.data, idsickness=form.sickness.data).execute()
        return redirect(url_for('index'))
    return render_template("createsymforsick.html", form=form, symsicks=symsicks, statistics_dict=statistics_dict)


@app.route('/change/<chtype>/<changing>', methods=['GET', 'POST'])
def change(changing, chtype):
    contents_dict = {
        "drug": Drug.select(),
        "symptom": Symptom.select(),
        "sickness": Sickness.select()
    }
    form = form_dict[chtype]
    form = form()
    if form.validate_on_submit():
        form.create_instance(_id=changing)
        return redirect(url_for('index'))
    if chtype == 'sickness':
        for i in range(len(form)):
            form.get_item(i).data = instance_dict[chtype].get_by_id(int(changing)).__getattribute__(data_sick[i])
    else:
        for i in range(len(form)):
            form.get_item(i).data = instance_dict[chtype].get_by_id(int(changing)).__getattribute__(data[i])

    return render_template("change.html", title='Change', form=form, index=changing, chtype=chtype, contents_dict=contents_dict, statistics_dict=statistics_dict)


@app.route('/delete/<chtype>/<deleting>', methods=['GET', 'POST'])
def delete(deleting, chtype):
    contents_dict = {
        "drug": Drug.select(),
        "symptom": Symptom.select(),
        "sickness": Sickness.select()
    }
    form = form_dict[chtype]
    form = form()
    if form.validate_on_submit():
        form.delete_instance(_id=deleting)
        return redirect(url_for('index'))
    if chtype == 'sickness':
        for i in range(len(form)):
            form.get_item(i).data = instance_dict[chtype].get_by_id(int(deleting)).__getattribute__(data_sick[i])
    else:
        for i in range(len(form)):
            form.get_item(i).data = instance_dict[chtype].get_by_id(int(deleting)).__getattribute__(data[i])

    return render_template("delete.html", title='Delete', form=form, index=deleting, chtype=chtype, contents_dict=contents_dict, statistics_dict=statistics_dict)


@app.route("/find/<instance>", methods=["GET", "POST"])
def find(instance):
    contents_dict = {
        "drug": Drug.select(),
        "symptom": Symptom.select(),
        "sickness": Sickness.select()
    }
    form = form_dict[instance.lower()]
    form = form()
    if request.method == 'POST':
        finder = instance_dict[instance.lower()].select().where(instance_dict[instance.lower()].name == form.get_item(0).data)
        if finder:
            return render_template("find.html", finder=finder[0], findtype=instance.lower(), statistics_dict=statistics_dict)
        else:
            return redirect(url_for('index'))
    return render_template("finder.html", form=form, instance=instance, statistics_dict=statistics_dict)


'''@app.route('/', methods=['GET', 'POST'])
def index():

    #row = Drug(name='Активированй уголь', description='Энтеросорбирующее средство', prescription=0)
    #row.save()
    drugs = (Drug.select(Drug.iddrug, Drug.name, Symptom.name.alias('namesym')).join(DrugForASymptom).join(Symptom).objects())
    
    #Drug.select().join(DrugForASymptom).join(Symptom)
    for drug in drugs:
        print('id = {0}, name = {1}, symname = {2},'.format(drug.iddrug, drug.name, drug.namesym)
    #drugs = Drug.select()

    for sick in Sickness.select():
        print('id = {0}, name = {1}, description = {2}, severity = {3}'.format(sick.idsickness, sick.name,
                                                                               sick.description, sick.severity))
    return render_template('./apteka.html', drugs=drugs)'''


if __name__ == '__main__':
    app.run(debug=True)
    #try:
        #my_db.connect()
    #except InternalError as px:
        #print(str(px))
