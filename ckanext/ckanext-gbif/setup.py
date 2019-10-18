from setuptools import setup, find_packages

version = '1.1.1'

setup(
    name='ckanext-gbif',
    version=version,
    description="A CKAN plugin to have GBIF fields",
    long_description="""\
    """,
    classifiers=[],
    keywords='',
    author='Thomas Vandenberghe',
    author_email='tvandenberghe@naturalsciences.be',
    url='',
    license='MIT',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    namespace_packages=['ckanext'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
            # dependencies are specified in pip-requirements.txt
            # instead of here
    ],
    tests_require=[
        'nose',
        'mock',
    ],
    test_suite='nose.collector',
    entry_points='''
    [ckan.plugins]
    ckanext_gbif=ckanext.gbif.plugin:IGBIFPlugin
''',
    message_extractors={
        'ckanext': [
            ('**.py', 'python', None),
            ('**.js', 'javascript', None),
            ('**/templates/**.html', 'ckan', None),
        ],
    }
)
