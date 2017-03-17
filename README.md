Building conda packages for CTA
===============================

The following information is for CTA pipelines code administrators to
create packages (it is not needed by regular users)

Create a new recipe for your revision
-------------------------------------

For *each* release, there should be a subdirectory in this repo called `<package>-<version>.conda/`
that contains the recipe. This way we can build past versions as well in an automated fashion.  
The `<version>` should be `major.minor` or `major.minor.sub`,  for example: `ctapipe-0.2.0.conda/`.
For re-builds of the same version release  you do not need to create a new directory 
(just increment the internal build number).

Create the recipe for your release
----------------------------------

1. create a subdir for your release as above.
2. Create or select a version branch/tag of the package (e.g. v1.2.0)
3. edit  `<package>.conda/meta.yaml` (copy it from previous version):

   - change the `git_rev` field to be the branch/tag name you chose
   - make sure the `entry_points` are the same as in the `setup.py`
     file of the main package, otherwise any command-line utils will not be
     installed
   - make sure the `requirements/build` list is also the same as in
     `setup.py` (any new dependencies should be added)


Build the packages locally
--------------------------

Run the following to create the package files.  The output will be
usually in `<ANACONDA>/conda-bld/<ARCH>/*.bz2`, where `<ANACONDA>` is
the path to your *Anaconda* or *miniconda* installation, but you can
check for sure by running `conda build ctapipe.conda --output`, which
will give you the path to the package.

```sh

conda build [--python=<version>] <package name>.conda

# for example:
conda build --python=3.5 ctapipe-0.3.3.conda
```

Next, make a new clean conda environment to test that everything works
and all the dependencies are ok:

```sh

conda create -n ctatest 
source activate ctatest 

```

Finally, try installing the new `ctapipe` package into this
environment. You should get `pyhessio` and other dependencies
automatically. For now you must use the `--use-local` option, until the package
is uploaded to Anaconda Cloud in the cta-observatory channel (see next step).

```sh

conda install --use-local ctapipe=<version>  # leave out =version to get latest
ctapipe-info --version --dependencies --tools

```

If all goes well, and your account has upload access for the
cta-observatory organization's channel on *Anaconda Cloud*, you can upload the
packages like this:

```

anaconda login --username <your anaconda username>
anaconda upload --username cta-observatory <package files>

```

From then on, users can install the package via:

```
conda install -c cta-observatory <package>
```

Automatic Building for multiple Python Versions
===============================================

A script, `buildall.py` is included to run the above steps for several
python versoins, to speed up creating packages. Use it as follows:

```
python buildall.py <package> [<package> ...]
```

It will build for each supported python version, and upload the
package to anaconda cloud (assuming you are already logged in)

Notes
=====

* You must build each package on a 64-bit *macOS* system and a *linux*
 system to ensure compatiblity with all CTA machines.  However, if the
 package has no compiled C code in it, you can use `conda convert
 <package filename> -p <target>` to convert it automatically.  Targets
 are `osx-64` or `linux-64`.  

* For Linux, please *only build on a SL6.X* or 
 compatible system (SL6.8 is used currently) to ensure the package works on 
 CTA grid machines. Building on newer Linux distros will cause problems due to 
 changes in `glibc` that are not backward compatible.

* To build for multiple python versions (e.g. 3.4, 3.5, 3.6), you need
 to re-run the conda build command with for example the `--python=3.5`
 option, once per python version, and upload all packages
