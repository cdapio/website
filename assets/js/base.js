const toggleButton = $('#toggleBtn')[0];
const collapseContainer = $('#companies');

collapseContainer.on('show.bs.collapse', () => {
  toggleButton.innerText = 'Close';
});

collapseContainer.on('hidden.bs.collapse', () => {
  toggleButton.innerText = 'Show more';
});
