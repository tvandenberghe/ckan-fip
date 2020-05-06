# encoding: utf-8
import json

import sys
import ckan.plugins as p
import ckan.plugins.toolkit as tk

from collections import OrderedDict

import logging
log = logging.getLogger(__name__)
#def create_taxa_tags():
#    user = tk.get_action('get_site_user')({'ignore_auth': True}, {})
#    context = {'user': user['name']}
#    try:
#        data = {'id': 'taxa_tags'}
#        tk.get_action('vocabulary_show')(context, data)
#    except tk.ObjectNotFound:
#        data = {'name': 'taxa_tags'}
#        vocab = tk.get_action('vocabulary_create')(context, data)
#        for tag in (u'uk', u'ie', u'de', u'fr', u'es'):
#            data = {'name': tag, 'vocabulary_id': vocab['id']}
#            tk.get_action('tag_create')(context, data)


def taxa_tags():
    #create_taxa_tags()
    try:
        tag_list = tk.get_action('tag_list')
        print(tag_list)
        taxa_tags = tag_list(data_dict={'vocabulary_id': 'taxonomic_coverage_taxa'})
        return taxa_tags
    except tk.ObjectNotFound:
        return None


class IGBIFPlugin(p.SingletonPlugin, tk.DefaultDatasetForm):
    p.implements(p.IDatasetForm)
    p.implements(p.IConfigurer)
    p.implements(p.ITemplateHelpers)
    p.implements(p.IFacets)

    def get_helpers(self):
        return {'taxonomic_coverage_taxa': taxa_tags}

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

    def create_md_element_from_vocab_tag(self, schema, name, type):
        if type == 'MODIFY':
            schema.update({
                name: [
                    tk.get_validator('ignore_missing'),
                    tk.get_converter('convert_to_tags')(name)
                ]
            })
        elif type == 'SHOW':
            schema.update({
                name: [
                    tk.get_converter('convert_from_tags')(name),
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
        schema = self.create_md_element(schema, 'occurrences', type)
        schema = self.create_md_element(schema, 'occurrence_count', type)
        schema = self.create_md_element(schema, 'doi', type)
        schema = self.create_md_element(schema, 'doi_gbif', type)
        schema = self.create_md_element(schema, 'study_extent', type)
        schema = self.create_md_element(schema, 'quality_control', type)
        schema = self.create_md_element(schema, 'method_steps', type)

        self.create_md_element_from_vocab_tag(schema,'taxonomic_coverage_taxa',type)
        self.create_md_element_from_vocab_tag(schema, 'actual_taxa', type)
        self.create_md_element_from_vocab_tag(schema, 'gcmd_keywords', type)
        self.create_md_element_from_vocab_tag(schema, 'gcmd_iso_topics', type)
        self.create_md_element_from_vocab_tag(schema, 'gbif_dataset_type', type)
        self.create_md_element_from_vocab_tag(schema, 'gbif_dataset_subtype', type)

        return schema

    def show_package_schema(self):
        schema = super(IGBIFPlugin, self).show_package_schema()
        self._modify_package_schema(schema, 'SHOW')

        #schema['tags']['__extras'].append(tk.get_converter('free_tags_only')) #irrelevant as all non-free tags are taken up as other variables
        #since the tags are a bit of a mess it's best not to show where they actually come from. So disable to hide vocabbed tags.

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

    def dataset_facets(self, facets_dict, package_type):
        '''Add new search facet (filter) for datasets.
        This must be a field in the dataset (or organization or
        group if you're modifying those search facets, just change the function).
        '''
        # the way to append as in the docs is not followed as we want to actibely delete some facet groups. ie. facets_dict['groups']
        #we replace the whole dict to keep the ordering fixed.
        facets_dict = OrderedDict({'organization': tk._('Organisations'),
                       'tags': tk._('Tags'),
                       'license_id': tk._('License'),
                       'vocab_taxonomic_coverage_taxa': tk._('Taxa')})
        #)prepending it with 'vocab_' is crucial!! Not mentioned at all in the documentation

        # Return the updated facet dict.
        return facets_dict
