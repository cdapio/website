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

const toggleButton = $('#toggleBtn')[0];
const collapseContainer = $('#companies');
const collapseVideos = $('#videos');

collapseVideos.on('show.bs.collapse', () => {
  toggleButton.innerText = 'Show less';
});

collapseVideos.on('hidden.bs.collapse', () => {
  toggleButton.innerText = 'Show more';
});

collapseContainer.on('show.bs.collapse', () => {
  toggleButton.innerText = 'Show less';
});

collapseContainer.on('hidden.bs.collapse', () => {
  toggleButton.innerText = 'Show more';
});

const menuButton = $('#menuBtn');
const closeButton = $('#closeBtn');
const mobileMenu = $('#mobileMenu');

menuButton.on('click', () => mobileMenu.show(300));
closeButton.on('click', () => mobileMenu.hide(300));

const hideTeamButton = $('#hideTeamBtn');
const showTeamButton = $('#showTeamBtn');
const heroDescription = $('#heroDescription');
const hero = $('#hero');
const heroTeam = $('#heroTeam');

showTeamButton.on('click', () => { heroTeam.show(300); heroDescription.hide(300); hero.addClass('opened'); });
hideTeamButton.on('click', () => { heroTeam.hide(300); heroDescription.show(300); hero.removeClass('opened'); });

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

function openVideoModal(title, link) {
  const videoModal = $('#video-modal');
  const videoLink = $('#videoModalLink');
  const videoTitle = $('#videoModalTitle')[0];

  videoLink.attr('src', link);
  videoTitle.innerText = title;
  videoModal.modal('show');
}

if (window.location.href.match('plugins')) {
  const quantityWrapper = document.querySelector('.plugins__quantity-wrapper');
  const quantity = document.querySelector('.plugins__quantity-wrapper > span');
  const plugins = document.querySelectorAll('.plugins-small__item');
  const searchResult = document.querySelector('.plugins-small__search-result');
  const showMoreContainer = document.querySelectorAll('.plugins-small__inner-description');
  const select = document.querySelector('.plugins-small__select');
  const selectDropdown = document.querySelector('.plugins-small__select-wrapper');
  const chipWrapper = document.querySelector('.plugins-small__chips');

  select.addEventListener('click', () => select.classList.toggle('active'));

  function showPlugins() {
    const checkboxes = Array.from(document.querySelectorAll('input[name="type"]'));

    const namesOfActiveCheckboxes = checkboxes
      .filter(checkbox => checkbox.checked)
      .map(x => x.value);

    let selectedPlugins;
    if (namesOfActiveCheckboxes.length > 0) {
      const pluginTypes = Array.from(document.querySelectorAll('.plugins-small__type'))
        .map(el => el.innerText)
        .filter((x, index, self) => self.indexOf(x) === index)
        .map(x => x.toLowerCase().replace(/\s/g, ''));

      const itemsByType = pluginTypes
        .map(type => ({[type]: Array.from(document.querySelectorAll(`[data-select='${type}']`))}))
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

    displayInformation(result);
    return result;
  }

  function displayInformation(plugins) {
    searchResult.style.display = plugins.length > 0 ? 'none' : '';
    quantityWrapper.style.display = plugins.length > 0 ? '' : 'none';
    if (plugins.length !== 0) {
      quantity.innerHTML = plugins.length;
    }
  }

  displayInformation(plugins);

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
}

function searchVideos() {
  const searchCriteria = document.querySelector('#searchInput').value.toUpperCase().replace(/\s/g, '');
  console.log(searchCriteria)
  Array.from(document.querySelectorAll('.videos-page__video-block'))
    .map(video => {
      console.log(video)
      const title = video.dataset.title;
      if (title.toUpperCase().replace(/\s/g, '').indexOf(searchCriteria) > -1) {
        video.style.display = '';
        return video;
      } else {
        video.style.display = 'none';
      }
    });
}
