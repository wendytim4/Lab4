from flask import Flask, request,jsonify
app = Flask(__name__)
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

app.app_context().push()

class Voters(db.Model):
    voters_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, )
    class_group = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"{self.name} - {self.class_group}"
   
class Election(db.Model):
     id = db.Column(db.Integer, primary_key=True)
     name = db.Column(db.String(80), unique=True, )
     start_time = db.Column(db.String(80))
     end_time = db.Column(db.String(80))
     def __repr__(self):
        return f"{self.name} - {self.start_time} - {self.end_time} "

class Candidate(db.Model):
    candidate_id = db.Column(db.Integer, primary_key=True)
    candidate_name = db.Column(db.String(80), unique=True, )
    candidate_major =  db.Column(db.String(80), nullable=False)
    def __repr__(self):
        return f"{self.candidate_name} - {self.candidate_major}  "


class Voting(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    voters_id = db.Column(db.Integer, db.ForeignKey(Voters.voters_id),nullable=False)
    candidate_id = db.Column(db.Integer, db.ForeignKey(Candidate.candidate_id), nullable=False)
    def __repr__(self):
        return f"{self.voters_id} - {self.candidate_id}"

#Retrieving all voters
@app.route('/voters', methods=['GET'])
def get_voter():
    voters = Voters.query.all()
    return jsonify([{
        'id': v.voters_id,
        'name': v.name,
        'cass_group': v.class_group,
     
    } for v in voters]), 200

#Retrieving all voters
@app.route('/voters/<id>', methods=['GET'])

def get_voters(id):
    voter=Voters.query.get_or_404(id)
    return {"name":voter.name, "class group":voter.class_group}


my_dicts = []
#Registering a student as  a voter
@app.route('/voters', methods=['POST'])
def add_voters():
    voter=Voters(name=request.json['name'],class_group=request.json['class_group'])
    db.session.add(voter)
    db.session.commit()



    vot={"name":voter.name, "class_group":voter.class_group,  "voter_Id":voter.voters_id}
    my_dicts.append(vot)

    save_file = open("Voters.json", "w")  
    json.dump(my_dicts, save_file, indent = 6)  
    save_file.close() 

    return {"name":voter.name, "class group":voter.class_group,  "Voter ID":voter.voters_id}

#deregistering a voter
@app.route('/voters/<id>', methods=['DELETE'])
def delete_voters(id):
    voter=Voters.query.get(id)
    if voter is None:
        return{"error":"not found"}
    db.session.delete(voter)
    db.session.commit()
    return {"message":"Deleted successfully"}


#updating a register-voter
@app.route('/voters/<int:voter_id>', methods=['PUT'])
def update_voter(voter_id):
    voter = Voters.query.get(voter_id)
    if not voter:
        return jsonify({'error': 'Voter not found'}), 404

    voter_data = request.json
    voter.name = voter_data['name']
    voter.class_group = voter_data['class_group']

    vot={"name":voter.name, "class_group":voter.class_group,  "voter_Id":voter.voters_id}

    save_file = open("filename.json", "w")  
    json.dump(vot, save_file, indent = 6)  
    save_file.close()

    db.session.commit()
    return jsonify({'message': 'Voter information updated successfully'}), 200


#Create an election
my_dicts = []
@app.route('/election', methods=['POST'])
def create_election():
    election=Election(name=request.json['name'],start_time=request.json['start_time'],end_time=request.json['end_time'])
    db.session.add(election)
    db.session.commit()
    
    vot={"name":election.name, "start_time":election.start_time,  "end_time":election.end_time}
    my_dicts.append(vot)

    save_file = open("Election.json", "w")  
    json.dump(my_dicts, save_file, indent = 6)  
    save_file.close() 

    return {"name":election.name, "start_time":election.start_time,  "end_time":election.end_time}

#retrieve an election
@app.route('/election/<id>', methods=['GET'])
def get_election(id):
    election=Election.query.get_or_404(id)
    return {"name":election.name, "start day":election.start_time, "end day":election.end_time}

#delete an election
@app.route('/election/<id>', methods=['DELETE'])
def delete_election(id):
    election = Election.query.get(id)
    if election is None:
        return{"error":"not found"}
    db.session.delete(election)
    db.session.commit()
    return {"message":"Deleted successfully"}



#Voting in an election
@app.route('/vote', methods=['POST'])
def votes():
    voting1=Voting(candidate_id=request.json['candidate_id'], voters_id=request.json['voters_id'])
    candidate = Candidate.query.filter_by(candidate_id=voting1.candidate_id).first()
    if candidate:
        db.session.add(voting1)
        db.session.commit()
        return {
                "Candidate ID": voting1.candidate_id,
                "Candidate Name": candidate.candidate_name,
                "Candidate Major": candidate.candidate_major,
                "Voter ID": voting1.voters_id
            }
     
    return {"message": "No Candidate Exist as such"}





    








