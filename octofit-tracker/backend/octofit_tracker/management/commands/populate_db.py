from django.core.management.base import BaseCommand
from django.conf import settings
from djongo import models
from pymongo import MongoClient

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **kwargs):
        client = MongoClient('localhost', 27017)
        db = client['octofit_db']

        # Clear collections
        db.users.delete_many({})
        db.teams.delete_many({})
        db.activities.delete_many({})
        db.leaderboard.delete_many({})
        db.workouts.delete_many({})

        # Create unique index on email for users
        db.users.create_index([('email', 1)], unique=True)

        # Sample data
        users = [
            {'name': 'Iron Man', 'email': 'ironman@marvel.com', 'team': 'Marvel'},
            {'name': 'Captain America', 'email': 'cap@marvel.com', 'team': 'Marvel'},
            {'name': 'Spider-Man', 'email': 'spiderman@marvel.com', 'team': 'Marvel'},
            {'name': 'Superman', 'email': 'superman@dc.com', 'team': 'DC'},
            {'name': 'Batman', 'email': 'batman@dc.com', 'team': 'DC'},
            {'name': 'Wonder Woman', 'email': 'wonderwoman@dc.com', 'team': 'DC'},
        ]
        teams = [
            {'name': 'Marvel', 'members': ['Iron Man', 'Captain America', 'Spider-Man']},
            {'name': 'DC', 'members': ['Superman', 'Batman', 'Wonder Woman']},
        ]
        activities = [
            {'user': 'Iron Man', 'activity': 'Running', 'duration': 30},
            {'user': 'Superman', 'activity': 'Flying', 'duration': 60},
        ]
        leaderboard = [
            {'team': 'Marvel', 'points': 120},
            {'team': 'DC', 'points': 110},
        ]
        workouts = [
            {'user': 'Batman', 'workout': 'Strength', 'suggestion': 'Push-ups'},
            {'user': 'Wonder Woman', 'workout': 'Cardio', 'suggestion': 'Running'},
        ]

        db.users.insert_many(users)
        db.teams.insert_many(teams)
        db.activities.insert_many(activities)
        db.leaderboard.insert_many(leaderboard)
        db.workouts.insert_many(workouts)

        self.stdout.write(self.style.SUCCESS('octofit_db database populated with test data.'))
