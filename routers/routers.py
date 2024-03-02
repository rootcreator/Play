class AppRouter:
    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'scrapper':
            return 'scrapper'
        elif model._meta.app_label == 'catalog':
            return 'catalog'
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'scrapper':
            return 'scrapper'
        elif model._meta.app_label == 'catalog':
            return 'catalog'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        # Allow relations if both objects are in the same app
        if obj1._meta.app_label == obj2._meta.app_label:
            return True
        # Allow relations if both objects are in app1 or app2
        elif obj1._meta.app_label in ['scrapper', 'catalog'] and obj2._meta.app_label in ['scrapper', 'catalog']:
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        # Allow migrations only on the relevant database for each app
        if app_label == 'scrapper':
            return db == 'scrapper'
        elif app_label == 'catalog':
            return db == 'catalog'
        return None
