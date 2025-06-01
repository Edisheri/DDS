// // Handle record deletion functionality
export function initRecordList() {
    document.querySelectorAll('.delete-btn').forEach(btn => {
        btn.addEventListener('click', async function(e) {
            e.preventDefault();
            const recordId = this.getAttribute('data-record-id');
            const csrfToken = document.querySelector('table').dataset.csrfToken;
            
            if (confirm('Are you sure you want to delete this record?')) {
                try {
                    const response = await fetch(`/delete/${recordId}/`, {
                        method: 'POST',
                        headers: {
                            'X-CSRFToken': csrfToken,
                            'Content-Type': 'application/json'
                        }
                    });
                    
                    if (response.ok) {
                        this.closest('tr').remove();
                    } else {
                        throw new Error('Failed to delete record');
                    }
                } catch (error) {
                    console.error('Error:', error);
                    alert('Error deleting record: ' + error.message);
                }
            }
        });
    });
    // EDIT 
    document.querySelectorAll('.edit-btn').forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            const recordId = this.getAttribute('data-record-id');
            window.location.href = `/edit-record/${recordId}/`;  // This will load the edit form page
        });
    });
}
