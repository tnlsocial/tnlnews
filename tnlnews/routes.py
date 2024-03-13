#!/usr/bin/env python3
import os
from datetime import datetime

from flask import current_app as app
from flask import render_template, abort, request, redirect, flash, url_for, send_from_directory, session, jsonify
from urllib.parse import urlparse

from . import db
from .auth import refrein
from .models import Post
from .util import get_title


@app.route("/", methods=["GET"])
def index():
    current_url = request.url.replace('http://', 'https://', 1)
    auth = request.args.get('auth', None)

    if auth:
        if not refrein(auth):
            return render_template('failure.html', msg="Your auth token did not verify"), 401

    try:
        cookie = session['name']
    except:
        cookie = False

    if not cookie:
        return render_template('auth.html', current_url=current_url), 401

    page = request.args.get('page', 1, type=int)
    per_page = 30  # Number of posts per page

    pagination = Post.query.order_by(Post.time_created.desc()).paginate(page=page, per_page=per_page, error_out=False)
    posts = pagination.items

    next_url = url_for('index', page=pagination.next_num) if pagination.has_next else None
    prev_url = url_for('index', page=pagination.prev_num) if pagination.has_prev else None

    return render_template("index.html", posts=posts, next_url=next_url, prev_url=prev_url, page=page, total_pages=pagination.pages)

@app.route("/<domain>", methods=["GET"])
def domain(domain):
    current_url = request.url.replace('http://', 'https://', 1)
    auth = request.args.get('auth', None)

    if auth:
        if not refrein(auth):
            return render_template('failure.html', msg="Your auth token did not verify"), 401

    try:
        cookie = session['name']
    except:
        cookie = False

    if not cookie:
        return render_template('auth.html', current_url=current_url), 401

    page = request.args.get('page', 1, type=int)
    per_page = 30  # Number of posts per page

    pagination = Post.query.filter_by(hostname=domain).paginate(page=page, per_page=per_page, error_out=False)

    posts = pagination.items

    next_url = url_for('index', page=pagination.next_num) if pagination.has_next else None
    prev_url = url_for('index', page=pagination.prev_num) if pagination.has_prev else None

    return render_template("index.html", posts=posts, next_url=next_url, prev_url=prev_url, page=page, total_pages=pagination.pages)

@app.route("/api/<token>/posturl", methods=["POST"])
def posturl(token):
    if token != 'sometokenyoudefinitelydidnthardcodeinhere':
        abort(401)

    if request.args.get('url') and request.method == "POST":
        post = Post()
        url = request.args.get('url')
        title = urlparse(url).hostname

        row = Post.query.filter_by(url=url).first()

        if(row):
            row.votes += 1
            try:
                db.session.commit()
                resp = jsonify(success=True, msg=f"Incremented vote for {url}")
                return resp, 200
            except Exception as e:
                print(e)
                resp = jsonify(success=False, msg=str(e))
                return resp            

        try:
            t = get_title(url)
            if len(t) <= 140:
                title = t
                row_2 = Post.query.filter_by(title=title).first()
                if(row_2):
                    if(row_2.title == title and title != "DPG Media Privacy Gate"):
                        row_2.votes += 1
                        try:
                            db.session.commit()
                            resp = jsonify(success=True, msg=f"Incremented vote for {url}")
                            return resp, 200
                        except Exception as e:
                            print(e)
                            resp = jsonify(success=False, msg=str(e))
                            return resp
        except Exception as e:
            print(e)
            resp = jsonify(success=False, msg=str(e))
            return resp, 500  

        post.nickname = "sembot"
        post.url = url
        post.title = title
        post.hostname = urlparse(url).hostname

        try:
            db.session.add(post)
            db.session.commit()
        except Exception as e:
            print(e)
            resp = jsonify(success=False, msg=str(e))
            return resp

        resp = jsonify(success=True)
        return resp
    
    return 


@app.errorhandler(404)
def page_not_found(e):
    flash(e, 'info')
    return redirect(url_for('index'))


@app.errorhandler(400)
def page_not_found(e):
    flash(e, 'info')
    return redirect(url_for('index'))


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico',
                               mimetype='image/vnd.microsoft.icon')
