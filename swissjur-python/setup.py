from setuptools import setup

requirements = [
    # package requirements go here
    'lxml',
    'requests',
]

setup(
    name='swiss-jurisprudence',
    version='0.1.0',
    description="Parse all the swiss jurisprudence from TF, ingest and clean",
    author="Sebastien Duc",
    author_email='sebastien.sduc@gmail.com',
    url='https://github.com/sduc/swiss-jurisprudence',
    packages=['swissjur'],
    entry_points={
        'console_scripts': [
            'swissjur=swissjur.cli:cli'
        ]
    },
    install_requires=requirements,
    keywords='swiss-jurisprudence',
    classifiers=[
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.6',
    ]
)
