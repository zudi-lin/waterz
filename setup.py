from setuptools import setup

setup(
        name='waterz',
        version='0.8',
        description='Simple watershed and agglomeration for affinity graphs.',
        url='https://github.com/donglaiw/waterz',
        license='MIT',
        requires=['cython','numpy','scipy'],
        packages=['waterz'],
        package_data={
            '': [
                'waterz/*.h',
                'waterz/*.hpp',
                'waterz/*.cpp',
                'waterz/*.pyx',
                'waterz/backend/*.hpp',
            ]
        },
        include_package_data=True,
        zip_safe=False
)
