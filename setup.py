from setuptools import setup

setup(
    name='korean_school',
    version='1.0',
    packages=['korean_school'],
    url='https://github.com/gunyu1019/korean_school_py',
    license='MIT',
    author='gunyu1019',
    author_email='gunyu1019@yhs.kr',
    description='이 파이썬 래퍼는 NEIS OpenAPI를 위하여 제작된 라이브러리 입니다.',
    python_requires='>=3.6',
    long_description=open('README.md', encoding='UTF-8').read(),
    long_description_content_type='text/markdown',
    include_package_data=True,
    install_requires=open('requirements.txt', encoding='UTF-8').read(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Natural Language :: Korean',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Internet',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities'
    ]
)