from setuptools import setup, find_packages

setup(
    name='paas-manager',
    version='0.1.0',
    description='Module to run MapReduce tasks with Hadoop',
    long_description=open('README.md').read(),
    author='Natsumi Asahara, Daniel Perez',
    author_email='n-asahara@nii.ac.jp, tuvistavie@gmail.com',
    url='https://github.com/pbl-cloud/paas-manager',
    download_url='https://github.com/pbl-cloud/paas-manager/archive/master.zip',
    license='MIT',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=True,
    test_suite='test',
    install_requires=open('requirements.txt').read().splitlines(),
    classifiers=[
        'Development Status :: 1 - Planning'
        'Environment :: Other Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries'
    ],
)
