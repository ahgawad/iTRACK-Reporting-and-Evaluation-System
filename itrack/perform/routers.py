class PerformRouters(object):
    def db_for_read(self,model, **hints):
        if model._meta.app_label == 'perform':
            return 'pridb'
        return None

    def db_for_write(self,model, **hints):
        if model._meta.app_label == 'perform':
            return 'pridb'
        return None

    def allow_relation(self,obj1, obj2, **hints):
        if obj1._meta.app_label == 'perform' and \
           obj2._meta.app_label == 'perform':
           return True
        return None

    '''
    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label == 'perform':
            return db == 'pridb'
        else:
            if app_label == 'perform' and db == 'default':
                return False
        return None
    '''