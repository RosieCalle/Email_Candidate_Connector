"""
This module contains functions to send emails using the Gmail API."""

import os
import os.path

import dateutil.parser as parser

import pandas as pd
from jinja2 import Environment, FileSystemLoader
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import itables.options as opt
from itables import show
from itables import init_notebook_mode
from bs4 import BeautifulSoup
from process_emails import process_email_data

def create_response(template, first_name):
    output = template.render(first_name=first_name)
    return output

def load_template(template_name):
    file_loader = FileSystemLoader('templates')
    env = Environment(loader=file_loader)
    template = env.get_template(template_name)
    return template

def render_template(template_name, **kwargs):
    template = load_template(template_name)
    output = template.render(**kwargs)
    return output

def send_email(subject, body, to_email, from_email, password):
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(from_email, password)
    text = msg.as_string()
    server.sendmail(from_email, to_email, text)
    server.quit()

