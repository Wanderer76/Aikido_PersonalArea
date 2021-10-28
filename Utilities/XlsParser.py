import datetime
import os
import openpyxl
from ctypes import ArgumentError

from django.db import transaction
from openpyxl.styles import numbers, PatternFill
from PersonalArea import models
from Utilities import password_generantor


def get_id(record):
    if isinstance(record, int):
        return int(record)
    else:
        if isinstance(record, str):
            if record[0] == '№':
                return int(record[1::])
        raise ArgumentError('Таблица заполнена не правильно')


def get_ku(record):
    if isinstance(record, int):
        return record
    else:
        if "дан" in record:
            pass
        else:
            return int(record.replace(' ', '').replace("кю", ""))
    raise ArgumentError('Таблица заполнена не правильно')


def parse_eu_date_to_us(record):
    return datetime.datetime.strptime(record, "%d.%m.%Y").strftime("%Y-%m-%d")


@transaction.atomic
def parseXlcToDb(xlcFile):
    book = openpyxl.open(xlcFile, read_only=True)
    book.iso_dates = True
    sheet = book.active
    print(sheet.max_row)

    for row in sheet.iter_rows(min_row=2, max_row=sheet.max_row):

        fileName = os.path.basename(xlcFile)
        member_id = get_id(row[4].value)

        if models.Seminar.objects.filter(name=fileName[0:fileName.find('.')], member_id = member_id).exists():
            continue

        seminar = models.Seminar()
        seminar.name = fileName[0:fileName.find('.')]
        seminar.club = row[7].value
        seminar.trainer = row[8].value
        seminar.city = row[11].value
        seminar.start_date = row[10].value
        seminar.attestation_date = row[12].value
        seminar.oldKu = get_ku(row[3].value)
        seminar.newKu = get_ku(row[13].value)
        seminar.isChild = True if row[14].value == '+' else False
        seminar.examiner = row[15].value

        trainer_id = get_id(row[9].value)
        set_trainer_status(trainer_id)
        if not (models.Aikido_Member.objects.filter(id=member_id).exists()):
            aikiboy = models.Aikido_Member.objects.create(
                id=member_id,
                password=password_generantor.generate_password(),
                name=row[1].value,
                surname=row[0].value,
                second_name=row[2].value,
                birthdate=row[5].value,
                region=int(row[6].value),
                club=row[7].value,
                photo=None,
                isTrainer=False,
                trainer_id=trainer_id
            )
            seminar.member = aikiboy
            seminar.save()

        else:
            aikiboy = models.Aikido_Member.objects.get(id=member_id)
            seminar.member = aikiboy
            seminar.save()


def set_trainer_status(trainer_id):
    if models.Aikido_Member.objects.filter(id=trainer_id).exists():
        trainer = models.Aikido_Member.objects.get(id=trainer_id)
        trainer.isTrainer = True
        trainer.save()


@transaction.atomic
def parseRecordsToXlc(eventName):
    wb = openpyxl.Workbook(iso_dates=True)
    workSheet = wb.active
    workSheet.append(["Фамилия", "Имя", "Отчество", "степень кю/дан", "#ID", "Дата рождения",
                      "Регион", "Клуб", "Тренер", "id тренера", "семинар", "место проведения", "аттестация",
                      "Присвоенная степень", "детский", "Экзаменатор"])
    set_blue_row(workSheet)

    seminars = models.Seminar.objects.filter(name=eventName)
    if len(seminars) == 0:
        raise ArgumentError()

    for seminar in seminars.values():
        try:
            member = models.Aikido_Member.objects.get(id=seminar["member_id"])
            workSheet.append(form_row(member, seminar))
        except:
            continue
    for i in workSheet.iter_rows(min_row=1, max_row=workSheet.max_row):
        i[5].number_format = numbers.FORMAT_DATE_DDMMYY
        i[10].number_format = numbers.FORMAT_DATE_DDMMYY
        i[12].number_format = numbers.FORMAT_DATE_DDMMYY
    wb.save(f"{eventName}.xlsx")


def form_row(member, seminar):
    return [
        member.surname, member.name, member.second_name, str(seminar['oldKu']) + "кю", member.id,
        member.birthdate,
        member.region,
        seminar['club'], seminar['trainer'], member.trainer_id, seminar['start_date'], seminar['city'],
        seminar['attestation_date'],
                                                         str(seminar['newKu']) + "кю",
        "да" if seminar['isChild'] else "нет", seminar['examiner']]


def set_blue_row(workSheet):
    for row in workSheet.iter_rows(min_row=1, max_row=1):
        for cell in row:
            cell.fill = PatternFill(patternType='solid', start_color="538dd5", end_color='538dd5')
