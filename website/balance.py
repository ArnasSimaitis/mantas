from .models import User,Groupuser,Group_Bills,Groups
from . import db
from flask_login import current_user

def count_balance():
    groups = Groupuser.query.filter_by(user=current_user.id).all()
    other_bills = 0
    my_bills_list = Group_Bills.query.filter_by(user=current_user.name).all()
    my_bills = 0
    if len(my_bills_list) < 1:
        my_bills = 0
    else:
        for x in my_bills_list:
            my_bills += x.sum
    for x in groups:
        other_bills_list = Group_Bills.query.filter_by(group=x.group).all()
        group_self_list = Groups.query.filter_by(id=x.group).first()
        if len(other_bills_list) < 1:
            continue
        else:
            for y in other_bills_list:
                if y.user == current_user.name:
                    continue
                other_bills += round(y.sum/group_self_list.users,2)
    balance = my_bills - other_bills
    return [my_bills,other_bills,balance]