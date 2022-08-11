

from smtplib import _AuthObject


AUTH_APPS = {'auth', 'contenttypes', 'admin','sessions'}
OBJECT_APPS = {'q','leaderboard','quiz','question'}


#,'ads','category','core'
class AuthRouter:
    route_app_labels = AUTH_APPS

    def db_for_read(self, model, **hints):
        if model._meta_app_label in self.route_app_labels:
            return 'auth_db'
        return None
        

    def db_for_write(self, model, **hints):
        if model._meta_app_label in self.route_app_labels:
            return 'auth_db'
        return None
        

    def allow_relation(self, obj1, obj2, **hints):
        if(
            obj1._meta_app_label in self.route_app_labels or
            obj2._meta_app_label in self.route_app_labels
        ):
            return True
        return None


    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label in self.route_app_labels:
            return db == 'auth_db'
        return None
        

    def allow_syncdb(self, db, model):
        if db == 'auth_db':
            return model._meta.app_label in self.route_app_labels or model._meta.app_label in OBJECT_APPS
        elif model._meta.app_label in self.route_app_labels:
            return False
        return True


class ObjectRouter:
    route_app_labels = OBJECT_APPS

    def db_for_read(self, model, **hints):
        if model._meta_app_label in self.route_app_labels:
            return 'object_db'
        return None
        

    def db_for_write(self, model, **hints):
        if model._meta_app_label in self.route_app_labels:
            return 'object_db'
        return None
        

    def allow_relation(self, obj1, obj2, **hints):
        if(
            obj1._meta_app_label in self.route_app_labels or
            obj2._meta_app_label in self.route_app_labels
        ):
            return True
        return None


    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label in self.route_app_labels:
            return db == 'object_db'
        return None
        


    def allow_syncdb(self, db, model):
        if db == 'auth_db':
            return model._meta.app_label in self.route_app_labels or model._meta.app_label in AUTH_APPS
        elif model._meta.app_label in self.route_app_labels:
            return False
        return True














        