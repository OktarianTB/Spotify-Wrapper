from distutils.core import setup
setup(
  name = 'easy_spotify',         # How you named your package folder (MyLib)
  packages = ['easy_spotify'],   # Chose the same as "name"
  version = 'v0.1-alpha',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Simple access the Spotify WEB API for general requests about artists, albums or songs',   # Give a short description about your library
  author = 'Tilney-Bassett Oktarian',                   # Type in your name
  author_email = 'ogt@connect.ust.hk',      # Type in your E-Mail
  url = 'https://github.com/user/OktarianTB',
  download_url = 'https://github.com/OktarianTB/easy_spotify/archive/v0.1-alpha.tar.gz',
  keywords = ['SPOTIFY', 'WEB API'],   # Keywords that define your package best
  install_requires=[
          'requests'
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)