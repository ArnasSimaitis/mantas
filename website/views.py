from urllib import request
from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import User, Groupuser, Groups, Group_Bills, Approvals
from . import db
from .balance import count_balance


views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    return render_template("home.html", user=current_user, bills=count_balance())

@views.route('/bills', methods=['GET', 'POST'])
@login_required
def bills():
    if request.method == 'POST':
        submitted_data = request.get_json(force=True)
        submitted_req = submitted_data['req']
        submitted_user = submitted_data['user']
        if submitted_req == 1:
            user = User.query.filter_by(name=submitted_user).first()
            groups = Groupuser.query.filter_by(user=user.id).all()
            if len(groups) >= 7:
                return jsonify({'response':f"Vartotojas <i>{user.name}</i> jau turi 7 grupes"})
            if user:
                return jsonify({'response':1})
            else:
                return jsonify({'response':"Vartotojas nerastas!"})
        elif submitted_req == 2:
            group_name = submitted_data['group_name']
            group_description = submitted_data['group_description']
            group_users = submitted_data['group_users']
            if len(group_name) > 150: 
                return jsonify({'response':'Grupės pavadinimas negali būti ilgesnis nei 150 simbolių'})
            elif len(group_description) > 150: 
                return jsonify({'response':'Grupės aprašymas negali būti ilgesnis nei 150 simbolių'})
            group_creator = User.query.filter_by(name=submitted_user).first()
            new_group = Groups(name=group_name,description=group_description,creator=group_creator.id,users=len(group_users))
            db.session.add(new_group)
            db.session.commit()
            print(group_users)
            for x in group_users:
                print(x)
                new_user = User.query.filter_by(name=x).first()
                new_group_user = Groupuser(user=new_user.id,group=new_group.id)
                db.session.add(new_group_user)
                db.session.commit()
            return jsonify({'response':1})
        elif submitted_req == 3:
            user = User.query.filter_by(name=submitted_user).first()
            groups = Groupuser.query.filter_by(user=user.id).all()
            if len(groups) < 1:
                return jsonify({'response':0})
            names = []
            descriptions = []
            for x in groups:
                group_info = Groups.query.filter_by(id=x.group).first()
                names.append(group_info.name)
                descriptions.append(group_info.description)
            return jsonify({'response':1,'names':names,'descriptions':descriptions,'how_many':len(groups)})
        elif submitted_req == 4:
            user = User.query.filter_by(name=submitted_user).first()
            groups = Groupuser.query.filter_by(user=user.id).all()
            list_number = submitted_data['group_list_number']
            if len(groups) < 1:
                return 0
            bills = Group_Bills.query.filter_by(group=groups[list_number].group).all()
            if len(bills) < 1:
                return jsonify({'response':0})
            sums = []
            users = []
            names = []
            for x in bills:
                names.append(x.name)
                users.append(x.user)
                sums.append(x.sum)
            return jsonify({'response':0,'names':names,'sums':sums,'users':users})
        elif submitted_req == 5:
            user = User.query.filter_by(name=submitted_user).first()
            groups = Groupuser.query.filter_by(user=user.id).all()
            list_number = submitted_data['group_list_number']
            bill_name = submitted_data['bill_name']

            sum = submitted_data['sum']
            new_bill = Group_Bills(name=bill_name,sum=sum,group=groups[list_number].group,user=submitted_user)
            db.session.add(new_bill)
            db.session.commit()
            print(new_bill.name,bill_name)
            return jsonify({'response':1})
        elif submitted_req == 6:
            submitted_group = submitted_data['group']
            print(submitted_group)
            groups = Groups.query.filter_by(name=submitted_group).first()
            if groups is None:
                groups = Groups.query.filter_by(id=submitted_group).first()
                if groups is None:
                    return jsonify({'response':'Ši grupė neegzistuoja.</br>Patikrinkite įvestą pavadinimą/ID.'})
            group_users = Groupuser.query.filter_by(user=submitted_user).all()
            for x in group_users:
                if x.group == groups.id:
                    return jsonify({'response':'Jūs jau priklausote šiai grupei'})
            if len(group_users) > 7:
                return jsonify({'response':'Jūs jau priklausote 7 grupėm.'})
            new_group_user = Approvals(group=groups.id,user=submitted_user,user_name=current_user.name,admin=groups.creator,group_name=groups.name)
            db.session.add(new_group_user)
            db.session.commit()
            return jsonify({'response':1})
        elif submitted_req == 7:
            approvals = Approvals.query.filter_by(admin=submitted_user).all()
            if len(approvals) == 0:
                return jsonify({'response':0})
            waiting_users = []
            waiting_groups = []
            waiting_ids = []
            for x in approvals:
                waiting_users.append(x.user_name)
                waiting_groups.append(x.group_name)
                waiting_ids.append(x.id)
            return jsonify({'response':1,'users':waiting_users,'groups':waiting_groups,'ids':waiting_ids})
        elif submitted_req == 8: #submitted_user veikia kaip Approvals ID
            approval = Approvals.query.filter_by(id=submitted_user).first()
            new_group_user = Groupuser(user=approval.user,group=approval.group)
            db.session.add(new_group_user)
            db.session.delete(approval)
            db.session.commit()
            return jsonify({'response':1})
        elif submitted_req == 9: #submitted_user veikia kaip Approvals ID
            approval = Approvals.query.filter_by(id=submitted_user).first()
            db.session.delete(approval)
            db.session.commit()
            return jsonify({'response':1})

    return render_template("bills.html", user=current_user, bills=count_balance())
