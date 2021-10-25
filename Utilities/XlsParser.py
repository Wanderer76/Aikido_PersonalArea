import datetime
import json
from ctypes import ArgumentError
import os

import openpyxl
from openpyxl.styles import numbers, PatternFill
from PersonalArea import models


def parseXlcToDb(xlcFile):

    book = openpyxl.open(xlcFile, read_only=True)
    book.iso_dates = True
    sheet = book.active

    for row in sheet.iter_rows(min_row=2, max_row=sheet.max_row):
        seminar = models.Seminar()
        seminar.name = os.path.basename(xlcFile)
        seminar.region = int(row[6].value)
        seminar.club = row[7].value
        seminar.trainer = row[8].value
        seminar.city = row[11].value
        seminar.attestation_date = row[12].value
        seminar.start_date = row[10].value
        seminar.oldKu = int(row[9].value)
        seminar.newKu = int(row[13].value)
        seminar.isChild = True if row[14].value == '+' else False
        seminar.examiner = row[15].value

        member_id = row[0].value

        if not (models.Aikido_Member.objects.filter(id=member_id).exists()):
            aikiboy = models.Aikido_Member.objects.create(
                id = member_id,
                password = '',
                surname = row[2].value,
                name = row[3].value,
                second_name = row[4].value,
                birthdate = row[5].value,
                region = int(row[6].value),
                city = 'Екатеринбург',
                club = row[7].value,
                photo = None,
                isTrainer = False,
                trainer_id = row[1].value
         )
            seminar.member = aikiboy
            seminar.save()

        else:
            aikiboy = models.Aikido_Member.objects.get(id = member_id)
            seminar.member = aikiboy
            seminar.save()


def parseRecordsToXlc(eventName):
    # нужны датарождения, фио
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
            workSheet.append([
                member.surname, member.name, member.second_name, str(seminar['oldKu']) + "кю", member.id,
                member.birthdate,
                seminar['region'],
                seminar['club'], seminar['trainer'], member.trainer_id, seminar['start_date'], seminar['city'],
                seminar['attestation_date'],
                                                                 str(seminar['newKu']) + "кю",
                "да" if seminar['isChild'] else "нет", seminar['examiner']])

        except:
            continue
    for i in workSheet.iter_rows(min_row=1, max_row=workSheet.max_row):
        i[5].number_format = numbers.FORMAT_DATE_DDMMYY
        i[10].number_format = numbers.FORMAT_DATE_DDMMYY
        i[12].number_format = numbers.FORMAT_DATE_DDMMYY
    wb.save(f"{eventName}.xlsx")


def set_blue_row(workSheet):
    for row in workSheet.iter_rows(min_row=1, max_row=1):
        for cell in row:
            cell.fill = PatternFill(patternType='solid', start_color="538dd5", end_color='538dd5')
