from typing import List, Any, Dict

from PersonalArea.models import Aikido_Member
from PersonalArea.serializations import Profile_Serializer
from clubs.models import Club
from clubs.serializators import Clubs_Serializer


def get_club_info(club: Club, is_detail: bool = False) -> Dict[str, str]:
    club_info = Clubs_Serializer(club).data
    main_trainers = Profile_Serializer(
        Aikido_Member.objects.filter(club=club, is_main_trainer=True), many=True).data
    if not is_detail:
        club_info['main_trainers'] = list(
            map(lambda x: f"{x['surname']} {x['name']} {x['second_name']}", main_trainers))
    else:
        club_info['main_trainers'] = list(
            map(lambda x:
                {
                    "name": f"{x['surname']} {x['name']} {x['second_name']}",
                    "id": f"{x['id']}"
                },
                main_trainers))
    return club_info


def get_main_trainers(query) -> List[Any]:
    main_trainers = query.getlist('main_trainers', default=None)
    if len(main_trainers) != 0:
        query.pop('main_trainers')
    return main_trainers


def set_main_trainers(main_trainers: List[int], club_obj: Club) -> None:
    Aikido_Member.objects.filter(club=club_obj, is_main_trainer=True).update(is_main_trainer=False)

    for trainer_id in main_trainers:
        trainer = Aikido_Member.objects.get(id=trainer_id)
        trainer.club = club_obj
        trainer.is_main_trainer = True
        trainer.save()
