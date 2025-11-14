document.addEventListener('DOMContentLoaded', function() {
    const modal = document.getElementById('confirmModal');
    const backdrop = modal.querySelector('.confirm-modal-backdrop');
    const messageElement = modal.querySelector('.confirm-modal-message');
    const cancelButton = modal.querySelector('.confirm-modal-cancel');
    const confirmButton = modal.querySelector('.confirm-modal-confirm');
    
    let currentForm = null;
    let currentButton = null;
    
    function showModal(message, form, button) {
        messageElement.textContent = message;
        currentForm = form;
        currentButton = button;
        modal.classList.add('active');
        document.body.style.overflow = 'hidden';
    }
    
    function hideModal() {
        modal.classList.remove('active');
        document.body.style.overflow = '';
        currentForm = null;
        currentButton = null;
    }
    
    function handleConfirm() {
        if (currentForm) {
            currentForm.submit();
        } else if (currentButton) {
            currentButton.click();
        }
        hideModal();
    }
    
    cancelButton.addEventListener('click', hideModal);
    confirmButton.addEventListener('click', handleConfirm);
    backdrop.addEventListener('click', hideModal);
    
    document.addEventListener('click', function(e) {
        const button = e.target.closest('[data-confirm]');
        if (button) {
            e.preventDefault();
            e.stopPropagation();
            
            const message = button.getAttribute('data-confirm');
            const form = button.closest('form');
            
            if (form) {
                button.type = 'button';
                showModal(message, form, null);
            } else {
                showModal(message, null, button);
            }
        }
    });
    
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && modal.classList.contains('active')) {
            hideModal();
        }
    });
});

