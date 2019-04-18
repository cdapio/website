const ctaBtns = document.querySelectorAll('.premises-services__button');
const closeBtns = document.querySelectorAll('.get-started__close-wrapper');
const dropdownEvaluationItems = document.querySelectorAll('.evaluation-nav-js');
const dropdownProductionItems = document.querySelectorAll('.production-nav-js');
const dropDownCta = document.querySelector('.dropdown-toggle');
const panesEvaluation = document.querySelectorAll('.evaluation-wrapper-js');
const panesProduction = document.querySelectorAll('.production-wrapper-js');
let persistBtnText = dropDownCta.innerText.trim();
let datasetContext = {};

function handleDropdownItemClick(items, panes, callback) {
  items.forEach(item => {
    item.addEventListener('click', function () {
      document.querySelector(`#dropdownBtn-${this.dataset.id}`).innerText = this.innerText;
      callback(panes, this);
    });
  });
}

function processOverlay(items, context) {
  items.forEach(item => {
    item.classList.remove('d-flex');
    if (context.dataset.id === item.dataset.reflect) {
      item.classList.add('d-flex');
    }
  });
}

handleDropdownItemClick(
  dropdownEvaluationItems,
  panesEvaluation,
  processOverlay
);
handleDropdownItemClick(
  dropdownProductionItems,
  panesProduction,
  processOverlay,
);

function open() {
  ctaBtns.forEach(btn => {
    btn.addEventListener('click', function () {
      datasetContext = { linkId: this.dataset.linkId, wrapper: this.dataset.wrapper };
      if (datasetContext) {
        const button = document.querySelector(`#${datasetContext.linkId}`);
        if (button !== null) {
          button.classList.add('d-flex');
        }
        document.querySelector(`.${datasetContext.wrapper}-js`).classList.add('d-none');
      }
    });
  });
}

function close() {
  closeBtns.forEach(closeBtn => {
    closeBtn.addEventListener('click', function() {
      this.parentNode.classList.remove('d-flex');
      document.querySelector(`.${this.dataset.reflect}`).classList.remove('d-none');
      dropDownCta.innerText = persistBtnText;
    });
  });
}

open();
close();
