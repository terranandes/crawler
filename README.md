
Project clawler aims to 
provide sorted expansion rate(AKA ROI) of each stock laid in following countries using python or perl to fetch data on internet.
  - Taiwan
  - China
  - America

Deployed PyCharm to develop modules and packages.
Plug-in Code-With-Me allows real time coding collaboratively.

MiniConda (or AnaConda if you don't mind disk size) is a MUST for self study on jupyter/IPython case.
In some cases, some modules like pandas can't be installed or might run into trouble, you probably need Conda.

Owner of Taiwan: Terran (https://github.com/terranandes)
Main Web of crawler : https://www.moneycome.in/tool/compound_interest
Status of project_tw:
  -- Data collected successfully. Outputs (CSV, JSON) ready as well.
  -- Data being analyzed using pandas.
  -- Tool for presentation of animation is ready. ( https://app.flourish.studio/visualisation/5774508/edit? )

Owner of China:
TBD

Owner of America:
TBD

Python Tutorial:
https://www.w3schools.com/python/python_intro.asp
The Python Package Index
https://pypi.org/

GIT learning resource:
https://learngitbranching.js.org/

Crawler learing resouce:
In Chinese:
https://mofanpy.com/tutorials/data-manipulation/scraping/
https://youtu.be/IMOUf4BYTG8 <==critial technique to react with JSS frontend(AJAX)
https://youtu.be/9Z9xKWfNo7k
https://youtu.be/ZMjhBB17KVY
https://youtu.be/MQH4Rau_F_A
Pandas:
https://youtu.be/5QZqzKCDCQ4
NumPy & Pandas:
https://www.jianshu.com/p/04d180d90a3f
https://www.jianshu.com/p/62524f4c240e

requests & selenium & beauifualsoup4 & pandas in a youtube video:
https://youtu.be/jV6eHoLzD2E

asyncio & httpx:
Asynchronously crawler web data by asyncio and replacing requests with httpx
asyncio:
https://docs.python.org/3/library/asyncio-task.html
https://www.maxlist.xyz/2020/03/29/python-coroutine/
https://docs.python.org/3/library/asyncio-task.html#asyncio.gather
https://www.dongwm.com/post/understand-asyncio-1
https://ithelp.ithome.com.tw/articles/10199385

httpx:
https://pypi.org/project/httpx/
golden example for nested httpx request:
https://github.com/terranfund/exercise_docs/blob/master/test/asyncio_gather_high_level_golden_httptx.py
https://towardsdatascience.com/supercharge-pythons-requests-with-async-io-httpx-75b4a5da52d7



In English:
Pandas:
https://www.youtube.com/watch?v=vmEHCJofslg
https://www.w3schools.com/python/pandas/default.asp

Needed python packages:
=== requests & selenium & beautifulsoup4 & pandas ===
https://pypi.org/project/requests/
https://pypi.org/project/beautifulsoup4/
https://pypi.org/project/selenium/
https://pypi.org/project/pandas/

Unix ENV for
Windows:
Ubuntu on Windows Store

Miniconda on Windows:
https://docs.conda.io/en/latest/miniconda.html#windows-installers
Miniconda on Windows Ubuntu:
https://docs.conda.io/en/latest/miniconda.html#linux-installers

MAC:
  - iTerm2+Zim+Powerlevel10k+Homebrew (Please google)
  - install Miniconda on Homebrew
    - https://formulae.brew.sh/cask/miniconda#default
  - other way to install Miniconda(use MAC's terminal)
    - https://conda.io/projects/conda/en/latest/user-guide/install/macos.html
    - Step 1: download bash file
    - Step 2: verify installer hash ( Command: shasum -a 256 /path/to/your/file/Miniconda3-<LatestVersion>-MacOSX-x86_64.sh )
    - Step 3: Install ( Command: bash /path/to/your/file/Miniconda3-<LatestVersion>-MacOSX-x86_64.sh )
    - Step 4: Test installation: Re-open terminal and type "conda list"
  - install modules like pandas, which fail in some MAC(M1) pip3 ...
    - conda install pandas

Why Conda?
Generally, we might learn Python using JupyterNotebook(or JupyterLab) from conda more quickly.
And furthur python modules are owned by Conda.
In M1, module like panda cannot be installed via default pip or homebrew pip.
For concern of disk usage, you can start with Miniconda instead of Anaconda.

Output:
  - A CSV, A JSON file to present expansion rate of each stock
    with statistical analysis by module pandas or even AI
  - BAR-CHART-RACE animations by native python module to engage audience
    https://pypi.org/project/bar-chart-race/

  - Or alternaive by outsourcing from Web
    https://flourish.studio/
    Demo:
    https://bit.ly/39WtfP1

Shared directoy is moved to https://github.com/terranfund/exercise_docs.

Contact us:
  Owner:     Terran  (TBD)
  Co-worker: Rodrigo ( jf20704jf@gmail.com )
