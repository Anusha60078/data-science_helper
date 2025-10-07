from setuptools import setup, find_packages

setup(
    name='ds_helper',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'pandas',
        'matplotlib',
        'seaborn'
    ],
    description='A reusable data science helper library for column detection, visualization, and text cleaning',
    author='Your Name',
    author_email='your_email@example.com',
    url='https://github.com/yourusername/ds_helper',
)
