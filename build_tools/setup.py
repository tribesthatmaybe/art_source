import setuptools

setuptools.setup(
    name='tribes_art_build_tools',
    version='0.1',
    py_modules=['export_maps'],
    # ToDo differentiate for py3
    install_requires=['six', 'toml']
)
