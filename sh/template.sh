#!/bin/bash -eux

# Choose what you want
#!/bin/bash -eu
set -eu
set -eux
set -euo pipefail
set -euxo pipefail

shellcheck "$0"
echo shellcheck OK
