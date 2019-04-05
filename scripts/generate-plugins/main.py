#!/usr/bin/python


#  Copyright 2019 Bhooshan Mogal
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


import argparse
import os
import sys
import json
import markdown
import pandas
import pytablewriter
from pprint import pprint
from bs4 import BeautifulSoup
from distutils.version import LooseVersion, StrictVersion
from collections import OrderedDict


PLUGIN_DISPLAY_TYPES = {
  'batchsource': 'Source',
  'streamingsource': 'Source',
  'batchsink': 'Sink',
  'sparksink': 'Sink',
  'realtimesink': 'Sink',
  'transform': 'Transform',
  'splittertransform': 'Transform',
  'alertpublisher': 'Alert Publisher',
  'action': 'Action',
  'sparkprogram': 'Action',
  'postaction': 'Action',
  'batchaggregator': 'Analytics',
  'sparkcompute': 'Analytics',
  'windower': 'Analytics',
  'batchjoiner': 'Analytics',
  'condition': 'Condition',
  'errortransform': 'Error Handler'
}


class VersionRange:
  def __init__(self, lower, upper, lower_inclusive, upper_inclusive):
    self.lower = lower
    self.upper = upper
    self.lower_inclusive = lower_inclusive
    self.upper_inclusive = upper_inclusive

  @staticmethod
  def parse(version_range):
    first_char = version_range[0]
    last_index = len(version_range) - 1
    last_char = version_range[last_index]
    brackets_removed = version_range[1:last_index]
    range_split = brackets_removed.split(',')
    lower = range_split[0].strip()
    upper = range_split[1].strip()
    # print lower, upper, first_char == '[', last_char == ']'
    return VersionRange(lower, upper, first_char == '[', last_char == ']')


def populate_built_in_plugins(artifacts_dir):
  built_in_plugins = OrderedDict()
  plugin_json_files = [pos_json for pos_json in os.listdir(artifacts_dir) if pos_json.endswith('.json')]

  for plugin_json_file in plugin_json_files:
    with open(os.path.join(artifacts_dir, plugin_json_file)) as f:
      parsed_plugin = parse_plugin_json(f)
      # check if any plugins were parsed. In certain scenarios, json files do not have any plugins. So ignore them.
      if parsed_plugin:
        built_in_plugins.update(parsed_plugin)

  return built_in_plugins


def populate_hub_plugins(hub_dir, cdap_version):
  hub_plugins = OrderedDict()
  packages_dir = os.path.join(hub_dir, "packages")
  # print "packages_dir", packages_dir
  for package_dir in os.listdir(packages_dir):
    # package_dir is a package name
    # print package_dir
    if os.path.isfile(os.path.join(packages_dir, package_dir)) or package_dir.startswith('.'):
      continue

    for version_dir in os.listdir(os.path.join(packages_dir, package_dir)):
      # version_dir is a version number of the package
      if os.path.isfile(os.path.join(packages_dir, package_dir, version_dir)) or version_dir.startswith('.'):
        continue

      if not is_valid_plugin(os.path.join(packages_dir, package_dir, version_dir, "spec.json"), cdap_version):
        # print 'not a valid plugin'
        continue

      # found a valid plugin. now parse its json file.
      plugin_json_file = get_plugin_json_file(os.path.join(packages_dir, package_dir, version_dir))
      with open(plugin_json_file) as f:
        hub_plugins.update(parse_plugin_json(f))

  return hub_plugins


def is_valid_plugin(package_spec_absolute_path, cdap_version):
  # print "checking valid plugin"
  with open(package_spec_absolute_path) as f:
    package_spec  = json.load(f)
    categories = package_spec['categories']
    # must be a plugin
    if not "hydrator-plugin" in categories:
      return False
    # must fall within version range, if such a range is defined
    if not 'cdapVersion' in package_spec:
      return True
    cdap_version_range = VersionRange.parse(package_spec['cdapVersion'])
    # print cdap_version_range.lower
    # print cdap_version_range.upper
    # print cdap_version_range.lower_inclusive
    # print cdap_version_range.upper_inclusive
    if LooseVersion(cdap_version_range.lower) < LooseVersion(cdap_version) < LooseVersion(cdap_version_range.upper):
      return True

    if cdap_version_range.lower_inclusive and LooseVersion(cdap_version_range.lower) == LooseVersion(cdap_version):
      return True

    if cdap_version_range.upper_inclusive and LooseVersion(cdap_version_range.upper) == LooseVersion(cdap_version):
      return True

    return False


def get_plugin_json_file(dir):
  json_files = [pos_json for pos_json in os.listdir(dir) if pos_json.endswith('.json') and pos_json != 'spec.json']
  return os.path.join(dir, json_files[0])


def parse_plugin_json(plugin_json_file):
  data = json.load(plugin_json_file)
  properties = data['properties']
  parsed_plugins = OrderedDict()
  for key in properties:
    # {
    #   "<plugin-name>": {
    #     "name": "<plugin-name>",
    #     "type": "<plugin-type>",
    #     "description": "<short description>",
    #     "icon": "<base64-encoded-icon>",
    #   }
    # }
    splits = key.split('.')
    config_type = splits[0]
    plugin_name_and_type = splits[1].split('-')
    plugin_name = plugin_name_and_type[0]
    # this should never happen. It only happens when a plugin file is not named correctly.
    # that scenario points to a different bug, which should be fixed.
    # e.g. https://github.com/data-integrations/change-data-capture/pull/1
    if len(plugin_name_and_type) < 2:
      plugin_type = ""
    else:
      plugin_type = plugin_name_and_type[1]

    # initialized plugin in result, if it is not already present
    if plugin_name not in parsed_plugins:
      parsed_plugins[plugin_name] = OrderedDict()

    # add name
    parsed_plugins[plugin_name]['Name'] = plugin_name
    # initialize display name to name. if available, this will be overriden by display-name from widgets json
    parsed_plugins[plugin_name]['Display Name'] = plugin_name

    # add type
    # conditional also due to same bug indicated above. Should never happen
    if plugin_type in PLUGIN_DISPLAY_TYPES:
      parsed_plugins[plugin_name]['Type'] = PLUGIN_DISPLAY_TYPES[plugin_type]
    else:
      parsed_plugins[plugin_name]['Type'] = "Unknown"

    if config_type == 'widgets':
      # add display name and icon
      add_display_name_and_icon(plugin_name, properties[key], parsed_plugins)
    elif config_type == 'doc':
      # add description
      add_description(plugin_name, properties[key], parsed_plugins)

  return parsed_plugins


def add_display_name_and_icon(plugin_name, widgets, dict_to_update):
  parsed_widgets = json.loads(widgets)
  if 'display-name' in parsed_widgets:
    dict_to_update[plugin_name]['Display Name'] = parsed_widgets['display-name']
  # add icon if available, else add N/A  
  dict_to_update[plugin_name]['Icon'] = 'N/A'
  if 'icon' in parsed_widgets:
    dict_to_update[plugin_name]['Icon'] = get_icon(parsed_widgets['icon'])
  pass


def add_description(plugin_name, docs, dict_to_update):
  description = find_description_element(docs)
  if description is None:
    print("Could not find description for - ", docs)
    return

  # print("Found description as: ", description.string)
  dict_to_update[plugin_name]['Description'] = description.string


def find_description_element(docs):
  html = markdown.markdown(docs)
  # print(html)
  soup = BeautifulSoup(html, 'html.parser')
  description = soup.find(lambda elm: elm.name == "h2" and "Description" in elm.text)
  if description is not None:
    # print("h2 description = ", description)
    return description.next_sibling.next_sibling

  # print("Docs with no description h2 element = ", docs)
  # ideally, this should not happen. however, impossible to fix all docs, so try to get
  # it as the first element after the title
  doc_title = find_title_element(soup)
  if doc_title is not None:
    # print("doc_title = ", doc_title)
    # should not happen. should fix these docs. they have a title but no content.
    # 1. Google Cloud Storage File Reader
    # 2. Speech Translator
    if doc_title.next_sibling is None:
      # print("None next_sibling: doc_title = %s, docs = %s", doc_title, docs)
      return None

    return doc_title.next_sibling.next_sibling

  # if we still can't find it, give up
  print("Give up! Can't find description for doc = ", docs)
  return


def find_title_element(soup):
  all_h1 = soup.find_all('h1')
  if all_h1:
    return all_h1[0]

  all_h2 = soup.find_all('h2')
  if all_h2:
    return all_h2[0]

  all_h3 = soup.find_all('h3')
  if all_h3:
    return all_h3[0]


def get_icon(icon):
  icon_type = icon['type']
  icon_arguments = icon['arguments']
  # print ("icon type = ", icon_type)
  # print ("icon arguments = ", icon_arguments)
  if icon_type == 'inline':
    icon_data = icon_arguments['data']
    # print ("inline icon data = ", icon_data)
    # TODO: if render type is markdown:
    rendered_icon = '![](' + icon_data + ')'
    rendered_icon = '<img src=\'' + icon_data + '\'/>'
    # print ("rendered icon = ", rendered_icon)
    return rendered_icon


def pivot_by_plugin_type(all_plugins):
  pivoted = {}
  for key, value in all_plugins.items():
    # print("type = ", value['type'])
    plugin_type = value['Type']
    # Since type is redundant in the value, remove it.
    del value['Type']
    if plugin_type not in pivoted:
      pivoted[plugin_type] = []

    pivoted[plugin_type].append(value)

  return pivoted


def write_as_md(plugins_by_type, output_path):
  writer = pytablewriter.MarkdownTableWriter()
  output = ''
  output += '# CDAP Plugins Reference\n'
  output += '\n'
  for key, value in plugins_by_type.items():
    plugin_type = key
    output += '## ' + plugin_type + ' (' + str(len(value)) + ')' + '\n'
    output += '\n'
    df = pandas.DataFrame(value)
    writer.from_dataframe(df)
    output += writer.dumps()
    output += '\n\n'

  with open(output_path, "w") as output_file:
    output_file.write(output)


def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('cdap_sandbox_dir', help='Absolute path to the directory containing the CDAP Sandbox')
  parser.add_argument('hub_dir', help='Absolute path to the directory containing the Hub source')
  parser.add_argument('-v', '--cdap_version', help='CDAP version to build plugin list for', default='5.0.0')
  parser.add_argument('-f', '--output_format', help='The format to generate output in', default='json')
  parser.add_argument('-o', '--output_path', help='Absolute path to output file. Output file must not exist. Containing directory must exist.', default='plugins')
  args = parser.parse_args()

  artifacts_dir = os.path.join(args.cdap_sandbox_dir, 'artifacts')

  built_in_plugins = populate_built_in_plugins(artifacts_dir)
  # print "########### built in #########"
  # print json.dumps(built_in_plugins)
  hub_plugins = populate_hub_plugins(args.hub_dir, args.cdap_version)
  # print "########### hub #########"
  # print json.dumps(hub_plugins)

  # combine/union
  all_plugins = {}
  all_plugins.update(built_in_plugins)
  all_plugins.update(hub_plugins)
  # print("########## everything #########")
  # print(json.dumps(all_plugins))

  
  # generate output
  # JSON
  if args.output_format == 'json':
    f = open(args.output_path, 'w')
    f.write(json.dumps(all_plugins))
  elif args.output_format == 'md':
    pivoted_by_plugin_type = pivot_by_plugin_type(all_plugins)
    # print(json.dumps(pivoted_by_plugin_type))
    write_as_md(pivoted_by_plugin_type, args.output_path)


if __name__ == '__main__':
  main()
