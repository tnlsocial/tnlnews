#!/usr/bin/env python3
import humanize
from . import db
from datetime import datetime

class Post(db.Model):
    __tablename__ = "Post"
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(100), nullable=False)
    title = db.Column(db.String(140), nullable=False, unique=True)
    url = db.Column(db.String, nullable=False, unique=True)
    hostname = db.Column(db.String)
    votes = db.Column(db.Integer, default=0)
    time_created = db.Column(db.DateTime, default=datetime.utcnow)

    @property
    def humanized_time(self):
        _t = humanize.i18n.activate("nl_NL")
        return humanize.naturaltime(datetime.utcnow() - self.time_created)
