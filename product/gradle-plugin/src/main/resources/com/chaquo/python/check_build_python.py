# Be careful about what syntax and APIs are used in this file: it should give the
# correct error message on old Python versions going as far back as possible.

import sys


expected = sys.argv[1]
actual = "{}.{}".format(*sys.version_info[:2])
if actual != expected:
    # Our stderr will be appended to the message "$bpSetting is not a valid Python
    # $version command: ".
    sys.exit("it is version {}".format(actual))

# The Gradle plugin will use this path as a file input property, so the build
# environment will be rebuilt if either the executable's path or content changes.
print(sys.executable)
