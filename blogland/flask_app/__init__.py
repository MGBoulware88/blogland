from flask import Flask, render_template, request, redirect, session, flash
app = Flask(__name__)
app.secret_key = "CHANGEME"
DB = "writing_between_the_lines"