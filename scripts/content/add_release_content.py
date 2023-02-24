import json
import copy

def generate_card(template_filename, cdap_version, release_notes_url):
    template_filepath = f'./templates/{template_filename}'
    short_version = cdap_version.replace('.', '')
    destination_filename = template_filename.replace('template', short_version)
    destination_filepath = f'../../content/en/get-started/cards/{destination_filename}'
    print(f'Reading template from: "{template_filepath}" to generate file: "{destination_filepath}"')

    with open(template_filepath) as source_file:
        source_file_content = source_file.read()
        source_file_content = source_file_content.replace('${CDAP_VERSION}', cdap_version)
        source_file_content = source_file_content.replace('${RELEASE_NOTES_URL}', release_notes_url)
        with open(destination_filepath, 'w') as destination_file:
            destination_file.write(source_file_content)


def generate_cards(cdap_version):
    print('[1/2] Generating get-started card files...')
    print('Enter the CDAP release notes link:')
    release_notes_url = input()
    generate_card('docker-template.md', cdap_version, release_notes_url)
    generate_card('linux-mac-template.md', cdap_version, release_notes_url)
    generate_card('vm-template.md', cdap_version, release_notes_url)


def update_data(cdap_version):
    print('[2/2] Updating get-started json data...')
    data_filepath = '../../data/en/get_started.json'
    print('Updating data file', data_filepath)
    short_version = cdap_version.replace('.', '')
    
    data = None
    with open(data_filepath) as data_file:
        data = json.load(data_file)

    short_title_map = {}
    short_title_map['Linux/Mac OSX'] = 'Linux/Mac'
    short_title_map['CDAP for VM'] = 'VM'
    short_title_map['CDAP for Docker'] = 'Docker'

    id_map = {}
    id_map['Linux/Mac OSX'] = 'linuxmac'
    id_map['CDAP for VM'] = 'vm'
    id_map['CDAP for Docker'] = 'docker'

    button_id_map = {}
    button_id_map['Linux/Mac OSX'] = f'version-{short_version}-mac'
    button_id_map['CDAP for VM'] = f'version-{short_version}-vm'
    button_id_map['CDAP for Docker'] = f'version-{short_version}-docker'

    button_href_map = {}
    button_href_map['Linux/Mac OSX'] = f'https://github.com/cdapio/cdap-build/releases/download/v{cdap_version}/cdap-sandbox-{cdap_version}.zip'
    button_href_map['CDAP for VM'] = f'https://github.com/cdapio/cdap-build/releases/download/v{cdap_version}/cdap-sandbox-{cdap_version}.ova'
    button_href_map['CDAP for Docker'] = 'https://hub.docker.com/r/caskdata/cdap-sandbox/'  

    details_map = {}
    details_map['Linux/Mac OSX'] = f'content/en/get-started/cards/linux-mac-{short_version}.md'
    details_map['CDAP for VM'] = f'content/en/get-started/cards/vm-{short_version}.md'
    details_map['CDAP for Docker'] = f'content/en/get-started/cards/docker-{short_version}.md'

    overlay_items_cache = {}
    pos = 0
    overlay_items = data['onPremises'][0]['evaluate'][0]['overlayItems']
    for overlay_item in overlay_items:
        overlay_item_title = overlay_item['item']['title']
        dropdown_item = {}
        dropdown_item['linkTitle'] = f'CDAP {cdap_version} {short_title_map[overlay_item_title]}'
        dropdown_item['id'] = f'{id_map[overlay_item_title]}-{short_version}'
        overlay_item['item']['dropdownItems'].insert(0, dropdown_item)

        if overlay_item_title not in overlay_items_cache:
            overlay_items_cache[overlay_item_title] = (copy.deepcopy(overlay_item), pos)

        pos = pos + 1

    inserted = 0
    for title, overlay_item_pos in overlay_items_cache.items():
        overlay_item = overlay_item_pos[0]
        title = overlay_item['item']['title']
        overlay_item['id'] = f'{id_map[title]}-{short_version}'
        overlay_item['item']['buttons'][0]['buttonTitle'] = f'CDAP {cdap_version} for {short_title_map[title]}'
        overlay_item['item']['buttons'][0]['id'] = f'{button_id_map[title]}'
        overlay_item['item']['buttons'][0]['buttonHref'] =  button_href_map[title]
        overlay_item['item']['dropdownItems'][0]['active'] = True
        del overlay_item['item']['dropdownItems'][1]['active']
        overlay_item['details'] = details_map[title]

        pos = overlay_item_pos[1]
        overlay_items.insert(pos + inserted, overlay_item)
        inserted = inserted + 1

    items = data['onPremises'][0]['evaluate'][0]['items']
    linux_mac_item = items[0]
    linux_mac_item['button']['buttonTitle'] = f'CDAP {cdap_version} for Linux/Mac'
    linux_mac_item['button']['id'] = button_id_map['Linux/Mac OSX']
    linux_mac_item['button']['buttonHref'] = button_href_map['Linux/Mac OSX']
    linux_mac_item['linkId'] = f'linuxmac-{short_version}'
    linux_mac_item['overlayPane']['id'] = f'version-{short_version}-mac'
    linux_mac_item['overlayPane']['linkTitle'] = f'CDAP {cdap_version} Linux/Mac'
    linux_mac_item['overlayPane']['title'] = f'CDAP {cdap_version} for Linux/Mac'
    docker_item = items[1]
    docker_item['buttons']['buttonTitle'] = f'CDAP {cdap_version} for Linux/Mac'
    docker_item['buttons']['id'] = button_id_map['CDAP for Docker']
    docker_item['buttons']['buttonHref'] = button_href_map['CDAP for Docker']
    docker_item['linkId'] = f'docker-{short_version}'
    docker_item['overlayPane']['id'] = f'version-{short_version}-docker'
    docker_item['overlayPane']['linkTitle'] = f'CDAP {cdap_version} Docker'
    docker_item['overlayPane']['title'] = f'CDAP {cdap_version} for Docker'

    with open(data_filepath, 'w') as data_file:
        json.dump(data, data_file, indent=2)


def main():
    print('Adding content for new CDAP version...\n')

    print('Enter the CDAP version (Eg. 6.8.0, 6.7.3):')
    cdap_version = input()

    generate_cards(cdap_version)
    update_data(cdap_version)

if __name__ == "__main__":
    main()
