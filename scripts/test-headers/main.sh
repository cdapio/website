#! /bin/bash

lic=$(
for file in $(find . -type f ! -path '*/\.*' ! -path './public/*' ! -path './resources/*' ! -path './node_modules/*' ! -path './static/*' ! -path './themes/cdap/assets/vendor/*' ! -path './bin/*' ! -path './bin/*' ! -name '*.md' ! -name '*.json' ! -name '*.txt' ! -name '*.svg' ! -name '*.py' ! -name '*.sh' ! -name 'LICENSE' -print -name '*.html' -o -name '*.js' -o -name '*.scss' -o -name '*.yml' -o -name '*.toml'); do
	head -n3 "${file}" | grep -Eq "(Copyright)" || echo "${file}"
done;)
if [ -n "${lic}" ]; then
	echo -e "license header checking failed in:\n${lic}"
	exit 255
fi
