#! /bin/bash

#  Copyright © 2019 CDAP
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

lic=$(
for file in $(find . -type f ! -path '*/\.*' ! -path './public/*' ! -path './resources/*' ! -path './node_modules/*' ! -path './static/*' ! -path './themes/cdap/assets/vendor/*' ! -path './bin/*' ! -path './bin/*' ! -name '*.md' ! -name '*.json' ! -name '*.txt' ! -name '*.svg' ! -name '*.py' ! -name '*.sh' ! -name 'LICENSE' -print -name '*.html' -o -name '*.js' -o -name '*.scss' -o -name '*.yml' -o -name '*.toml'); do
	head -n3 "${file}" | grep -Eq "(Copyright)" || echo "${file}"
done;)
if [ -n "${lic}" ]; then
	echo -e "license header checking failed in:\n${lic}"
	exit 255
fi
