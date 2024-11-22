
document.addEventListener('DOMContentLoaded', () => {
  //On Page Load, open the ticket form and configure delete actions
  const modal = new bootstrap.Modal(document.getElementById('ticket_modal'), {})
  modal.show()
  configureDeleteTicketButton()
  configureDeleteCommentButtons()
})


function configureDeleteTicketButton() {
  //Select the Delete Ticket Button and bind the confirm buttons and Server Path. Skip if no elements selected.
  const deleteButton = document.querySelector('.remove-ticket-btn');

  if (deleteButton == null) return

  deleteButton.addEventListener('click', () => {
    const projectId = deleteButton.getAttribute('data-project-id')
    const ticketId = deleteButton.getAttribute('data-ticket-id');
    const ticketName = deleteButton.getAttribute('data-ticket-name'); 

    const modalDescription = document.querySelector('#delete_ticket_modal .modal-body p');
    const modalFormAction = document.querySelector('#delete_ticket_modal #modalForm');

    modalDescription.textContent = `
    This action is irreversible and will delete the Ticket ${ticketName} and all associated comments, forever.
    \n Are you sure you want to delete ${ticketName}?`;

    modalFormAction.setAttribute('action', `/project/${projectId}/${ticketId}/delete`);
  });
}


function configureDeleteCommentButtons() {
  //Select the Delete Comment Buttons and bind the confirm buttons and Server Path. Skip if no elements selected.
  const deleteButtons = document.querySelectorAll('.remove-comment-btn');
  console.log(deleteButtons.length)
  if (deleteButtons == null || deleteButtons.length === 0) return

  deleteButtons.forEach(button => {
    button.addEventListener('click', () => {
      const projectId = button.getAttribute('data-project-id')
      const ticketId = button.getAttribute('data-ticket-id');
      const commentId = button.getAttribute('data-comment-id');
  
      const modalDescription = document.querySelector('#delete_comment_modal .modal-body p');
      const modalFormAction = document.querySelector('#delete_comment_modal #modalForm');
  
      modalDescription.textContent = `
      This action is irreversible and will delete the comment, forever.
      \n Are you sure you want to delete the comment?`;
  
      modalFormAction.setAttribute('action', `/project/${projectId}/${ticketId}/${commentId}/delete`);
    });
  })
}