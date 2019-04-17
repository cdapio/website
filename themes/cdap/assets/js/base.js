/*
 * * Copyright © 2019 Cask Data, Inc.
 *
 *  Licensed under the Apache License, Version 2.0 (the "License"); you may not
 *  use this file except in compliance with the License. You may obtain a copy of
 *  the License at
 *
 *  http://www.apache.org/licenses/LICENSE-2.0
 *
 *  Unless required by applicable law or agreed to in writing, software
 *  distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
 *  WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
 *  License for the specific language governing permissions and limitations under
 *  the License.
 */

const menuButton = $('#menuBtn');
const closeButton = $('#closeBtn');
const mobileMenu = $('#mobileMenu');
const hideTeamButton = $('#hideTeamBtn');
const showTeamButton = $('#showTeamBtn');
const heroDescription = $('#heroDescription');
const hero = $('#hero');
const heroTeam = $('#heroTeam');

$(document).ready(() => {
    if (window.location.hash === "#premises") {
      $("#on-premises").addClass("active");
      $("#premises-tab").addClass("in active show");
      window.location.hash = '';
    } else {
      $("#on-cloud").addClass("active");
      $("#cloud-tab").addClass("in active show");
    }
  }
);

menuButton.on('click', () => mobileMenu.show(300));
closeButton.on('click', () => mobileMenu.hide(300));
showTeamButton.on('click', () => {
  heroTeam.show(300);
  heroDescription.hide(300);
  hero.addClass('opened');
});
hideTeamButton.on('click', () => {
  heroTeam.hide(300);
  heroDescription.show(300);
  hero.removeClass('opened');
});

function learnMore(id) {
  const toggleButton = $(`#${id}btn`)[0];
  const collapseContainer = $(`#${id}`);

  collapseContainer.on('show.bs.collapse', () => {
    toggleButton.innerText = 'Hide';
  });

  collapseContainer.on('hidden.bs.collapse', () => {
    toggleButton.innerText = 'Learn more';
  });
}

const searchResult = document.querySelector('.plugins-small__search-result');
const quantityWrapper = document.querySelector('.plugins__quantity-wrapper');
const quantity = document.querySelector('.plugins__quantity-wrapper > span');

function displayQuantityInformation(items) {
  if (searchResult !== null && quantityWrapper !== null) {
    searchResult.style.display = items.length > 0 ? 'none' : '';
    quantityWrapper.style.display = items.length > 0 ? '' : 'none';

    if (items.length !== 0) {
      quantity.innerHTML = items.length;
    }
  }
}

const plugins = document.querySelectorAll('.plugins-small__item');
const showMoreContainer = document.querySelectorAll('.plugins-small__inner-description');
const select = document.querySelector('.plugins-small__select');
const selectDropdown = document.querySelector('.plugins-small__select-wrapper');
const chipWrapper = document.querySelector('.plugins-small__chips');

if (select !== null) {
  select.addEventListener('click', () => select.classList.toggle('active'));
}

function showPlugins() {
  const checkboxes = Array.from(document.querySelectorAll('input[name="type"]'));

  const namesOfActiveCheckboxes = checkboxes
    .filter(checkbox => checkbox.checked)
    .map(x => x.value.toLowerCase());

  let selectedPlugins = [];
  if (namesOfActiveCheckboxes.length > 0) {
    const pluginTypes = Array.from(document.querySelectorAll('.plugins-small__type'))
      .map(el => el.innerText)
      .filter((x, index, self) => self.indexOf(x) === index)
      .map(x => x.toLowerCase().trim());

    const itemsByType = pluginTypes
      .map(type => ({ [type]: Array.from(document.querySelectorAll(`[data-select='${type}']`)) }))
      .reduce((acc, curr) => Object.assign(acc, curr), {});

    selectedPlugins = namesOfActiveCheckboxes
      .map(type => itemsByType[type])
      .reduce((acc, pluginsByType) => [...acc, ...pluginsByType], []);
  } else {
    selectedPlugins = plugins;
  }

  const searchInput = document.querySelector('.plugins-small__search-input');
  const searchCriteria = searchInput.value.toUpperCase().replace(/\s/g, '');

  plugins.forEach(plugin => plugin.style.display = 'none');

  const result = Array.from(selectedPlugins).filter((plugin) => {
    const title = plugin.dataset.title;
    if (title.toUpperCase().replace(/\s/g, '').indexOf(searchCriteria) > -1) {
      plugin.style.display = '';
      return plugin;
    } else {
      plugin.style.display = 'none';
    }
  });
  displayQuantityInformation(result);
  return result;
}

function search() {
  showPlugins();
}

function onSelect() {
  const checkboxes = Array.from(document.querySelectorAll('input[name="type"]'));

  const activeCheckboxes = checkboxes
    .filter(checkbox => checkbox.checked);

  showPlugins();

  clearContainer(chipWrapper);
  activeCheckboxes.forEach(addChip);
  event.stopPropagation();
  selectDropdown.classList.toggle('active');
  document.addEventListener('click', () => selectDropdown.classList.remove('active'));
}

function addChip(checkbox) {
  const name = checkbox.value;
  const chip = document.createElement('div');
  const closeBtn = document.createElement('span');
  chip.setAttribute(`data-chip`, name);
  chip.classList.add('plugins-small__chip');
  closeBtn.classList.add('plugins-small__chip-close');
  closeBtn.innerText = 'X';
  chip.innerText = name;
  chip.appendChild(closeBtn);
  closeBtn.addEventListener('click', () => {
    checkbox.checked = false;
    chipWrapper.removeChild(chip);
    showPlugins();
  });
  chipWrapper.appendChild(chip);
}

function clearContainer(element) {
  return element.innerHTML = '';
}

function toggleDetails(index) {
  const elementClassList = showMoreContainer[index].classList;
  elementClassList.contains('active') ? elementClassList.remove('active') : elementClassList.add('active');
}

const showMoreVideos = document.querySelector('#toggleBtn');
const videos = document.querySelectorAll('.videos-page__video-block');
const videosByDisplayShow = Array.from(videos).filter(video => video.style.display === '');
const videosWrapper = document.querySelector('.videos-page__wrapper');
let VIDEOS_TO_SHOW;
if (videosWrapper !== null) {
  VIDEOS_TO_SHOW = videosWrapper.dataset.videosToShow
}

function showVideos(videos, display, label) {
  Array.from(videos)
    .map((video, index) => {
      if (videosWrapper !== null && index > VIDEOS_TO_SHOW) {
        video.style.display = display;
      }
    });
  showMoreVideos.innerText = label;
}

if (showMoreVideos !== null) {
  showMoreVideos.addEventListener('click', () => {
    if (showMoreVideos.innerText === 'Show more') {
      showVideos(videos, 'block', 'Show less');
      displayQuantityInformation(videos);
    } else {
      showVideos(videos, 'none', 'Show more');
      displayQuantityInformation(videosByDisplayShow);
    }
  });
}

function openVideoModal(title, link) {
  const videoModal = $('#video-modal');
  const videoLink = $('#videoModalLink');
  const videoTitle = $('#videoModalTitle')[0];

  videoLink.attr('src', link);
  videoTitle.innerText = title;
  videoModal.modal('show');
}

function searchVideos() {
  const searchCriteria = document.querySelector('#searchInput').value.toUpperCase().replace(/\s/g, '');
  const result = Array.from(videos)
    .filter(video => {
      const title = video.dataset.title;
      if (title.toUpperCase().replace(/\s/g, '').indexOf(searchCriteria) > -1) {
        video.style.display = '';
        return video;
      } else {
        video.style.display = 'none';
      }
    });
  displayQuantityInformation(result);

  searchCriteria.length > 0 && (result.length > VIDEOS_TO_SHOW || result.length < VIDEOS_TO_SHOW)
    ? showMoreVideos.style.display = 'none'
    : showMoreVideos.style.display = 'block';
  if (searchCriteria.length === 0) {
    showVideos(videos, 'none', 'Show more');
    displayQuantityInformation(videosByDisplayShow);
  }
  return result;
}

if (window.location.href.match('plugins')) {
  displayQuantityInformation(plugins);
}

if (window.location.href.match('videos')) {
  displayQuantityInformation(videosByDisplayShow);
}
