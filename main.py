# -*- coding: utf-8 -*-
"""
Created on Thu Jan  5 11:09:53 2023

@author: bpohl
"""

from website import create_app

app = create_app()

if __name__ == '__main__':    #only run if main is launched
    app.run(debug=True)     #rerun every change (debug=True)
    