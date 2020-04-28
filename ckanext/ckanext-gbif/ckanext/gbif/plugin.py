# encoding: utf-8

import ckan.plugins as p
import ckan.plugins.toolkit as tk


def create_country_codes():
    user = tk.get_action('get_site_user')({'ignore_auth': True}, {})
    context = {'user': user['name']}
    try:
        data = {'id': 'country_codes'}
        tk.get_action('vocabulary_show')(context, data)
    except tk.ObjectNotFound:
        data = {'name': 'country_codes'}
        vocab = tk.get_action('vocabulary_create')(context, data)
        for tag in (u'uk', u'ie', u'de', u'fr', u'es'):
            data = {'name': tag, 'vocabulary_id': vocab['id']}
            tk.get_action('tag_create')(context, data)


def country_codes():
    create_country_codes()
    try:
        tag_list = tk.get_action('tag_list')
        country_codes = tag_list(data_dict={'vocabulary_id': 'country_codes'})
        return country_codes
    except tk.ObjectNotFound:
        return None


class IGBIFPlugin(p.SingletonPlugin, tk.DefaultDatasetForm):
    p.implements(p.IDatasetForm)
    p.implements(p.IConfigurer)
    p.implements(p.ITemplateHelpers)

    def get_helpers(self):
        return {'country_codes': country_codes}

    def create_md_element(self, schema, name, type):
        if type == 'MODIFY':
            schema.update({
                name: [tk.get_validator('ignore_missing'),
                       tk.get_converter('convert_to_extras')]
            })
        elif type == 'SHOW':
            schema.update({
                name: [tk.get_converter('convert_from_extras'),
                       tk.get_validator('ignore_missing')]
            })
        return schema

    def _modify_package_schema(self, schema, type):
        schema = self.create_md_element(schema, 'administrative_contact_full', type)
        schema = self.create_md_element(schema, 'administrative_contact_name', type)
        schema = self.create_md_element(schema, 'metadata_contact_full', type)
        schema = self.create_md_element(schema, 'metadata_contact_name', type)
        schema = self.create_md_element(schema, 'originator_full', type)
        schema = self.create_md_element(schema, 'originator_name', type)
        schema = self.create_md_element(schema, 'eml_created', type)
        schema = self.create_md_element(schema, 'eml_modified', type)
        schema = self.create_md_element(schema, 'maintenance_frequency', type)
        schema = self.create_md_element(schema, 'start_datetime', type)
        schema = self.create_md_element(schema, 'end_datetime', type)
        schema = self.create_md_element(schema, 'geo_desc', type)
        schema = self.create_md_element(schema, 'taxonomic_coverage', type)
        schema = self.create_md_element(schema, 'actual_taxa', type)
        schema = self.create_md_element(schema, 'occurrences', type)
        schema = self.create_md_element(schema, 'doi', type)
        schema = self.create_md_element(schema, 'doi_gbif', type)
        schema = self.create_md_element(schema, 'study_extent', type)
        schema = self.create_md_element(schema, 'quality_control', type)
        schema = self.create_md_element(schema, 'method_steps', type)
        return schema

    def show_package_schema(self):
        schema = super(IGBIFPlugin, self).show_package_schema()
        '''schema.update({
            'custom_text': [tk.get_converter('convert_from_extras'),
                            tk.get_validator('ignore_missing')]
        })'''
        self._modify_package_schema(schema, 'SHOW')
        return schema

    def create_package_schema(self):
        schema = super(IGBIFPlugin, self).create_package_schema()
        schema = self._modify_package_schema(schema, 'MODIFY')
        return schema

    def update_package_schema(self):
        schema = super(IGBIFPlugin, self).update_package_schema()
        schema = self._modify_package_schema(schema, 'MODIFY')
        return schema

    def is_fallback(self):
        # Return True to register this plugin as the default handler for
        # package types not handled by any other IDatasetForm plugin.
        return True

    def package_types(self):
        # This plugin doesn't handle any special package types, it just
        # registers itself as the default (above).
        return []

    # update config
    def update_config(self, config):
        # Add this plugin's templates dir to CKAN's extra_template_paths, so
        # that CKAN will use this plugin's custom templates.
        tk.add_template_directory(config, 'templates')
