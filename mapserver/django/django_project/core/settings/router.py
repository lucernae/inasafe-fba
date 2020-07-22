from django.apps import apps


class CustomRouter(object):

    def db_for_read(self, model, **hints):
        database = getattr(model, "_DATABASE", None)
        if database:
            return database
        else:
            return "default"

    def db_for_write(self, model, **hints):
        database = getattr(model, "_DATABASE", None)
        if database:
            return database
        else:
            return "default"

    def allow_relation(self, obj1, obj2, **hints):
        """
        Relations between objects are allowed if both objects are
        in the master/slave pool.
        """
        db_list = ('default')
        if obj1._state.db in db_list and obj2._state.db in db_list:
            return True
        return None

    def allow_migrate(self, target_db, app_label, model_name=None, **hints):
        model_name = model_name or hints.pop('model_name', None)
        belongs_to = None
        if model_name:
            try:
                model = apps.get_model(app_label, model_name)
                belongs_to = getattr(model, "_DATABASE", 'default')
            except LookupError:
                # Due to model deletion
                belongs_to = 'default'

        is_belong = (belongs_to == target_db)
        if not is_belong:
            is_belong = (target_db == app_label)
        return is_belong
