"""app/admin/views.py"""

import app 
from flask                  import flash, redirect, render_template, url_for
from flask_login            import current_user,login_required
from app.firestore_service  import import__export_data,backend_only_create_tenant

from . import admin

@admin.route('/admin/import', methods=['GET'])
@login_required
def import_export_data():
    try:
        # import__export_data()

        return {'message': 'Done'},200
    except Exception as inst:
        print(type(inst))    # the exception instance
        print(inst.args)     # arguments stored in .args
        print(inst)          # __str__ allows args to be printed directly,
                             # but may be overridden in exception subclasses
        return {'message': 'Error importing or exporting data'},400
        

@admin.route('/admin/createTenant/<newTenant>', methods=['GET'])
@login_required
def createTenant(newTenant):
    try:
        backend_only_create_tenant(newTenant)

        return {'message': 'Done'},200
    except Exception as inst:
        print(type(inst))    # the exception instance
        print(inst.args)     # arguments stored in .args
        print(inst)          # __str__ allows args to be printed directly,
                             # but may be overridden in exception subclasses
        return {'message': 'Error creating tenant'},400
   



