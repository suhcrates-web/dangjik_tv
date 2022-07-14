from flask import Flask, render_template, url_for, request, redirect, jsonify
from datetime import datetime, timedelta
from jonghap import jonghap
from mbc_checker import mbc_checker
from jtbc_checker import jtbc_checker
from sql_toolbox import time_checker


checkers_dic = {'mbc': mbc_checker,
                'jtbc':jtbc_checker}
# def checkers(brod):
#     checkers_dic[brod]()
#
# print(checkers("mbc"))
#
print(checkers_dic['mbc']())