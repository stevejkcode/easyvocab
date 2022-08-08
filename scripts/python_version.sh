VERSION=$(python --version | awk '{print $2}')

echo "$VERSION" | awk 'BEGIN {FS="."} {OFS="."} {print $1"."$2}'