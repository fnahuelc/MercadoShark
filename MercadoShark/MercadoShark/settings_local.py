#!/usr/bin/python
# -*- coding: utf-8 -*-
#asdada
import platform

LOCAL_DEVELOPMENT = ('fnahuelc.pythonanywhere.com' not in platform.node())

if LOCAL_DEVELOPMENT:
    # Debug Settings
    print 'Running settings for local_development'

    DEBUG = True
    CLIENT_ID = 7292933213227627
    CLIENT_SECRET = 'hElyNu2AWz4btCFGEgYu9997WeopUod0'
    REDIRECT_URI = 'http://www.localhost:8000/managerApp/authorize_meli'

    USER_TEST_INFO = {
        "id": 249620029,
        "nickname": "TETE9430306",
        "password": "qatest4690",
        "site_status": "active",
        "email": "test_user_30720982@testuser.com"
    }

else:
    # Debug Settings
    print 'Running settings for pythonanywhere'

    DEBUG = False
    CLIENT_ID = 4704790082736526
    CLIENT_SECRET = 'V94M94z1GYoQC5PLXHL95O6mS6p6mOVH'
    REDIRECT_URI = 'https://fnahuelc.pythonanywhere.com/managerApp/authorize_meli'

