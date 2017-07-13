from setuptools import setup, find_packages

setup(name='weasl',
      version='0.1',
      description='Weakly supervised active learning',
      license='MIT',
      url='https://github.com/njpataki/weasl',
      packages=find_packages(),
      entry_points={'console_scripts': ['weasl = weasl.main:top_level_command']},
      install_requires=['numpy', 'scipy', 'scikit-learn', 'pandas', 'seaborn', 
                        'pyyaml', 'flask', 'Flask-WTF', 'flask-bootstrap'])
