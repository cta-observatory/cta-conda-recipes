Building conda packages for CTA
===============================

The following information is for CTA pipelines code administrators to
create packages (it is not needed by regular users)

Create a new recipe for your revision
-------------------------------------

For *each* release, there should be a subdirectory in this repo called `<package>-<version>.conda/`
that contains the recipe. This way we can build past versions as well in an automated fashion.  You do not need to keep separate dirs for each *build number*, just for released versions.  For example: `ctapipe-v0.2.0.conda/`

Create the package recipe
--------------------------

1. create a subdir for your release as above.
2. Create or select a version branch/tag of the package (e.g. v1.2)
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

conda build <package name>.conda

conda build purge # optional, to clean up if everything worked

```

Next, make a new clean conda environment to test that everything works
and all the dependencies are ok:

```sh

conda create -n ctatest
source activate ctatest ipython

```

Finally, try installing the new `ctapipe` package into this
environment. You should get `pyhessio` and other dependencies
automatically. For now you must use the `--use-local` option, until we
setup a conda channel

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

Notes
=====

You must build each package on a 64-bit *macOS* system and a *linux*
system to ensure compatiblity with all CTA machines.  However, if the
package has no compiled C code in it, you can use `conda convert
<package filename> -p <target>` to convert it automatically.  Targets
are `osx-64` or `linux-64`
