Building conda packages for CTA
===============================

The following information is for CTA pipelines code administrators to
create packages (it is not needed by regular users)

Update the package definition
-----------------------------

1. Create or select a version branch/tag of the package (e.g. v1.2)
2. edit  `<package>.conda/meta.yaml`:

   - change the `git_rev` field to be the branch/tag name you chose
   - make sure the `entry_points` are the same as in the `setup.py`
     file of the main package
   - make sure the `requirements/build` list is also the same as in
     `setup.py` (any new dependencies must be added)


Build the packages locally
--------------------------

Run the following to create the package files.  The output will be
usually in `<ANACONDA>/conda-bld/<ARCH>/*.bz2`, where `<ANACONDA>` is
the path to your *Anaconda* or *miniconda* installation, but you can
check for sure by running `conda build ctapipe.conda --output`, which
will give you the path to the package.

```sh

conda build pyhessio.conda
conda build ctapipe.conda

conda build purge # to clean up if everything worked

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

conda install --use-local ctapipe
ctapipe-info --version --dependencies --tools

```

If all goes well, and you are the administrator for the
cta-observatory channel on *Anaconda Cloud*, you can upload the
packages like this:

```

anaconda login --username cta-observatory
anaconda upload <package files>

```

Notes
=====

You must build each package on a 64-bit *macOS* system and a *linux*
system to ensure compatiblity with all CTA machines.  However, if the
package has no compiled C code in it, you can use `conda convert
<package filename> -p <target>` to convert it automatically.  Targets
are `osx-64` or `linux-64`
