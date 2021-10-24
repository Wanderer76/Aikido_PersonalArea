import datetime
import json
from ctypes import ArgumentError

import openpyxl
from openpyxl.styles import numbers, PatternFill
from PersonalArea import models


def parseXlcToDb(xlcFile):
    pass


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
