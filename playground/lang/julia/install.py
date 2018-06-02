import sys
import platform
import logging

try:
    from urllib.request import urlretrieve
except ImportError:
    from urllib import urlretrieve

logger = logging.get_logger(__name__)

def download(config, version, labels):
    url = get_url(version)

    playground_path = os.path.expanduser("~/.playground")
    base_name = "julia-0.6-default"
    tmp_path = os.path.join(playground_path, "tmp", "base_name")
    src_path = os.path.join(playground_path, "src", "base_name")
    bin_path = os.path.join(playground_path, "bin", "base_name")
    download_bin = tmp_path + '-' + ext

    try:
        for p in (tmp_path, src_path, bin_path):
            if not os.path.exists(p):
                os.makedirs(p)

        logger.info("Downloading julia 0.6 from {}".format(julia))
        urlretrieve(julia, download_bin)

        # Minimal install code for macos and linux
        if sys.platform.startswith('linux'):
            logger.info(logger, "Installing {} ...".format(tmp_path))

            logger.debug("Extracting {} to {}".format(download_bin, src_path))
            subprocess.call(["tar", "-xzf", download_bin, "-C", src_path])

            julia_bin_path = os.path.join(src_path, os.listdir(src_path)[0], "bin/julia")
            st = os.stat(julia_bin_path)
            os.chmod(julia_bin_path, st.st_mode | stat.S_IEXEC)
            logger.debug("Permissions set to $(Playground.JULIA_BIN_MODE)")

            try:
                os.symlink(julia_bin_path, bin_path)
            except:
                logger.warn("Failed to create symlink to {}".format(bin_path))
        elif sys.platform == "darwin":
            exe_path = os.path.join(src_path, "Contents/Resources/julia/bin/julia")
            dmg_path = tempfile.mkdtemp()

            try:
                try:
                    subprocess.call(["hdiutil", "attach", "-mountpoint", dmg_path, tmp_path])
                    app_path = glob.glob("*.app")[0]
                    shutil.copytree(app_path, src_path)
                    st = os.stat(exe_path)
                    os.chmod(exe_path, st.st_mode | stat.S_IEXEC)

                    try:
                        symlink(exe_path, bin_path)
                    except:
                        logger.warn("Failed to create symlink to {}".format(bin_path))
                finally:
                    subprocess.call(["hdiutil", "detach", dmg_path])
            finally:
                shutil.rmtree(dmg_path)
    finally:
        for p in (tmp_path, src_path)
            if os.path.exists(p):
                shutil.rmtree(p)


def get_url(release):
    os = platform.system()
    arch = platform.architecture()[0]

    os_arch = None
    ext = None
    nightly_ext = None

    # Cannibalized from https://github.com/travis-ci/travis-build/blob/master/lib/travis/build/script/julia.rb
    if os == 'Linux') and arch == '64bit':
        os_arch = 'linux/x64'
        ext = 'linux-x86_64.tar.gz'
        nightly_ext = 'linux64.tar.gz'
    elif os == 'Linux' and arch == '32bit':
        os_arch = 'linux/x32'
        ext = 'linux-i686.tar.gz'
        nightly_ext = 'linux32.tar.gz'
    elif os == 'Darwin' and arch == '64bit':
        os_arch = 'mac/x64'
        ext = 'mac64.dmg'
    elif os === 'Windows' and arch == '64bit':
        os_arch = 'winnt/x64'
        ext = 'win64.exe'
        nightly_ext = ext
    elif os === 'Windows' and arch == '32bit':
        os_arch = 'winnt/x86'
        ext = 'win32.exe'
        nightly_ext = ext
    else:
        raise Exception(
            'No binary Julia release found for {arch} {os}'.format(os=os, arch=arch)
        )

    # Note: We could probably get specific revisions if we really wanted to.
    # eg. https://status.julialang.org/download/osx10.7+ redirects to
    # https://s3.amazonaws.com/julianightlies/bin/osx/x64/0.5/julia-0.5.0-2bb94d6f99-osx.dmg

    if release > NIGHTLY:
        raise Exception(
            'Version {r} exceeds the latest known nightly build {n}'.format(r=release, n=NIGHTLY)
        )

    if len(release.version) < 2:
        raise Exception('You must specify at least a minor release')

    major_minor = '{major}.{minor}'.format(major=release.version[0], minor=release.version[1])

    if len(release.version) == 2:
        if release.version[0:2] == NIGHTLY.version[0:2]:
            # https://julialangnightlies-s3.julialang.org/bin/linux/x64/julia-latest-linux64.tar.gz
            url = 'julialangnightlies-s3.julialang.org/bin/{os_arch}/julia-latest-{nightly_ext}'.format(
                os_arch=os_arch,
                nightly_ext=nightly_ext,
            )
        else:
            # https://julialang-s3.julialang.org/bin/linux/x64/0.6/julia-0.6-latest-linux-x86_64.tar.gz
            url = 'julialang-s3.julialang.org/bin/{os_arch}/{major_minor}/julia-{major_minor}-latest-{ext}'.format(
                os_arch=os_arch,
                major_minor=major_minor,
                ext=ext,
            )
    elif len(release.version) == 3:
        if release.version[0:3] == NIGHTLY.version[0:3]:
            # https://julialangnightlies-s3.julialang.org/bin/linux/x64/julia-latest-linux64.tar.gz
            url = 'julialangnightlies-s3.julialang.org/bin/{os_arch}/julia-latest-{nightly_ext}'.format(
                os_arch=os_arch,
                nightly_ext=nightly_ext,
            )
        else:
            # https://julialang-s3.julialang.org/bin/linux/x64/0.5/julia-0.5.2-linux-x86_64.tar.gz
            v = '{major}.{minor}.{patch}'.format(
                major=release.version[0],
                minor=release.version[1],
                patch=release.version[2]
            )
            url = 'julialang-s3.julialang.org/bin/{os_arch}/{major_minor}/julia-{version}-{ext}'.format(
                os_arch=os_arch,
                major_minor=major_minor,
                version=v,
                ext=ext,
            )

    return 'https://{url}'.format(url=url)