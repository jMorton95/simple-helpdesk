 /*Immediately invoked function expression (IIFE) (https://developer.mozilla.org/en-US/docs/Glossary/IIFE)
      This is required to dynamically append Swimlane form options that have HTML attributes the backend recognises as our form.
  */
  //TODO: There must be a simpler way of keeping track of our swimlanes dynamically, check Django docs for implicit methods
document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('#swimlanes input').forEach(x => x.required = true);
  const addSwimlaneButton = document.getElementById('add-swimlane');
  const swimlanesDiv = document.getElementById('swimlanes');
  const totalFormsInput = document.querySelector('#id_form-TOTAL_FORMS');
  const emptyFormDiv = document.getElementById('empty-form').innerHTML;

  let formIndex = parseInt(totalFormsInput.value, 10);

  configureSwimlaneButtons(formIndex, addSwimlaneButton, emptyFormDiv, swimlanesDiv, totalFormsInput)
  configureSwimlanes(swimlanesDiv, totalFormsInput)
  configureDeleteButtons()
  configureProjectDeleteButton()
});

function configureSwimlaneButtons(formIndex, addSwimlaneButton, emptyFormDiv, swimlanesDiv, totalFormsInput){
  addSwimlaneButton.addEventListener('click',  () => {
    const newFormHtml = emptyFormDiv.replace(/__prefix__/g, formIndex);
    swimlanesDiv.insertAdjacentHTML('beforeend', newFormHtml);

    formIndex++;
    totalFormsInput.value = formIndex;

    const removeButton = swimlanesDiv.querySelector(`#form-${formIndex - 1} .remove-swimlane-btn`);
    removeButton.style.display = 'block';

    /* Allow each form created on the UI to remove itself if necessary and update the indexes of other forms. */
    removeButton.addEventListener('click',  () => {
      const formRow = removeButton.closest('.form-row');

      // Prevent removal if the form is a database driven swimlane
      if (formRow.classList.contains('saved-swimlane')) {
        return;
      }

      formRow.remove();
      reindexForms(swimlanesDiv, totalFormsInput);
    });
  });
}

function configureDeleteButtons(){
 /* Collect and iterate over all current swimlanes, configure the delete_swimlane_modal.html
    template variables to dynamically set the swimlane the user is targeting for deletion */
    const deleteButtons = document.querySelectorAll('.remove-swimlane-btn');

    deleteButtons.forEach( (button) => {
      button.addEventListener('click', function() {
          const swimlaneId = button.getAttribute('data-swimlane-id');
          const swimlaneName = button.getAttribute('data-swimlane-name');
          const projectId = document.getElementById("delete_project_button").getAttribute('data-project-id')

          const modalDescription = document.querySelector('#delete_swimlane_modal .modal-body p');
          const modalFormAction = document.querySelector('#delete_swimlane_modal #modalForm');

          modalDescription.textContent = `This action is irreversible and will delete the Swimlane ${swimlaneName} and all associated tickets, forever. \n Are you sure you want to delete ${swimlaneName}?`;

          modalFormAction.setAttribute('action', `/project/${projectId}/swimlane/delete/${swimlaneId}`);
      });
    });
}

function configureSwimlanes(swimlanesDiv, totalFormsInput){
 /* Allow removal of existing swimlanes on page load and ensure reindexing */
 swimlanesDiv.addEventListener('click', (event) => {
  if (event.target.classList.contains('remove-swimlane-btn')) {
    const formRow = event.target.closest('.form-row');

    if (formRow.classList.contains('saved-swimlane')) {
      return;
    }

    formRow.remove();
    reindexForms(swimlanesDiv, totalFormsInput);
  }
});
}

 // Reindex forms and update management form data
function reindexForms(swimlanesDiv, totalFormsInput) {
  const forms = swimlanesDiv.querySelectorAll('.form-row.container:not(.saved-swimlane)');
  forms.forEach((formRow, index) => {
    formRow.querySelectorAll('[name]').forEach(input => {
        const nameAttr = input.getAttribute('name');
        const idAttr = input.getAttribute('id');
        if (nameAttr) {
            input.setAttribute('name', nameAttr.replace(/\d+/, index));
        }
        if (idAttr) {
            input.setAttribute('id', idAttr.replace(/\d+/, index));
        }
    });
  });
  totalFormsInput.value = forms.length;
}

function configureProjectDeleteButton(){
  const button = document.getElementById("delete_project_button");

  button.addEventListener('click', () => {
    const projectId = button.getAttribute('data-project-id');
    const projectName = button.getAttribute('data-project-name');

    const modalDescription = document.querySelector('#delete_project_modal .modal-body p');
    const modalFormAction = document.querySelector('#delete_project_modal #modalForm');

    modalDescription.textContent = `This action is irreversible and will delete the Project ${projectName} and all associated swimlanes and tickets, forever. \n Are you sure you want to delete ${projectName}?`;

    modalFormAction.setAttribute('action', `/project/${projectId}/delete`);
  });
}