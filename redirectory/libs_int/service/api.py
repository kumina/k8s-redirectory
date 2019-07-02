from flask_restplus import Api as BaseApi


class Api(BaseApi):

    def _register_doc(self, app_or_blueprint):
        if self._add_specs and self._doc:
            # Register documentation before root if enabled
            app_or_blueprint.add_url_rule(self._doc, 'doc', self.render_doc)

        # This is the line that causes you not to be able to bind the root
        # WTF FLASK, PEOPLE WANT TO BIND THE ROOT
        # app_or_blueprint.add_url_rule(self._doc, 'root', self.render_root)

    @property
    def base_path(self):
        return ''
