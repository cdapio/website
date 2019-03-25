const toggleButton = $('#toggleBtn')[0];
const collapseContainer = $('#companies');

collapseContainer.on('show.bs.collapse', () => {
  toggleButton.innerText = 'Show less';
});

collapseContainer.on('hidden.bs.collapse', () => {
  toggleButton.innerText = 'Show more';
});



function learnMore(id) {
  const toggleButton = $("#" + id + "btn")[0];
  const collapseContainer = $("#" + id);

  collapseContainer.on('show.bs.collapse', () => {
    toggleButton.innerText = 'Hide';
  });

  collapseContainer.on('hidden.bs.collapse', () => {
    toggleButton.innerText = 'Learn more';
  });
}
