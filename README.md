Building conda packages for CTA
===============================

The following information is for CTA pipelines code administrators to
create packages (it is not needed by regular users)


Building a package
```
conda build -c cta-observatory <package>
```

If the package needs no compilation, then you can use `conda convert`
to build packages for other architectures as well (make sure both
macOS and Linux-64 packages are built and uploaded). Otherwise, you
must build the packages on both a macOS machine and a CentOS7 machine.


If all goes well, and your account has upload access for the
cta-observatory organization's channel on *Anaconda Cloud*, you can upload the
packages like this:

```

anaconda login --user <your anaconda username>
anaconda upload --user cta-observatory <package files>

```

From then on, users can install the package via:

```
conda install -c cta-observatory <package>
```

Notes
=====

* You must build each package on a 64-bit *macOS* system and a *linux*
 system to ensure compatiblity with all CTA machines.  However, if the
 package has no compiled C code in it, you can use `conda convert
 <package filename> -p <target>` to convert it automatically.  Targets
 are `osx-64` or `linux-64`.  

* For Linux, please *only build on a CENTOS7 machine* or 
 compatible system (SL6.8 is used currently) to ensure the package works on 
 CTA grid machines. Building on newer Linux distros will cause problems due to 
 changes in `glibc` that are not backward compatible.

* To build for multiple python versions use a conda_build_config.yml file in the package. 
