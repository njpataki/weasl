from setuptools import setup


setup(name='weasl',
      version='0.1',
      description='Weakly supervised active learning',
      license='MIT',
      url='https://github.com/njpataki/weasl',
      packages=['weasl'],
      entry_points={
            'console_scripts': ['weasl = weasl.main:top_level_command']
      },
      install_requires=['numpy', 'scipy', 'scikit-learn',
                        'matplotlib', 'pandas', 'seaborn']
      )
