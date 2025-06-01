// Initialize all form interactions
export function initCashFlowForm() {
    /**
     * Generic function to handle dynamic field addition
     * @param {string} selectId - ID of the select element
     * @param {string} addBtnId - ID of the "Add" button
     * @param {string} containerId - ID of the new input container
     * @param {string} inputId - ID of the new input field
     * @param {string} saveBtnId - ID of the save button
     * @param {string} endpoint - API endpoint for saving
     * @param {Object} extraParams - Additional parameters for the request
     */
    const setupAddField = (selectId, addBtnId, containerId, inputId, saveBtnId, endpoint, extraParams = {}) => {
        const select = document.getElementById(selectId);
        const addBtn = document.getElementById(addBtnId);
        const container = document.getElementById(containerId);
        const input = document.getElementById(inputId);
        const saveBtn = document.getElementById(saveBtnId);

        addBtn.addEventListener('click', () => {
            container.classList.toggle('d-none');
            input.focus();
        });

        const saveHandler = () => {
            const value = input.value.trim();
            if (!value) return;
            
            const formData = new URLSearchParams();
            formData.append('name', value);
            
            for (const [param, getValue] of Object.entries(extraParams)) {
                const paramValue = getValue();
                if (paramValue) formData.append(param, paramValue);
            }
            
            fetch(endpoint, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                },
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (data.id) {
                    const option = new Option(data.name, data.id, true, true);
                    select.add(option);
                    input.value = '';
                    container.classList.add('d-none');
                    saveBtn.textContent = '✓ Saved';
                    setTimeout(() => saveBtn.textContent = 'Save', 1000);
                }
            })
            .catch(error => {
                console.error('Error:', error);
                saveBtn.textContent = 'Error!';
                setTimeout(() => saveBtn.textContent = 'Save', 1000);
            });
        };

        saveBtn.addEventListener('click', saveHandler);
        input.addEventListener('keypress', (e) => e.key === 'Enter' && saveHandler());
    };

    // Initialize dynamic field additions
    setupAddField(
        'status-select', 'add-status-btn', 'new-status-container', 
        'new-status-input', 'save-status-btn', '/status/quick-add/'
    );
    setupAddField(
        'type-select', 'add-type-btn', 'new-type-container', 
        'new-type-input', 'save-type-btn', '/type/quick-add/'
    );
    setupAddField(
        'id_category', 'add-category-btn', 'new-category-container',
        'new-category-input', 'save-category-btn', '/category/quick-add/'
    );
    setupAddField(
        'id_subcategory', 'add-subcategory-btn', 'new-subcategory-container',
        'new-subcategory-input', 'save-subcategory-btn', '/subcategory/quick-add/',
        {
            'category_id': () => {
                const categoryId = document.getElementById('id_category').value;
                if (!categoryId) {
                    alert('Please select a category first');
                    return null;
                }
                return categoryId;
            }
        }
    );
    
    // Dynamic subcategory loading
    document.getElementById("id_category")?.addEventListener("change", function() {
        const categoryId = this.value;
        if (!categoryId) return;
        
        fetch(`/get_subcategories/?category_id=${categoryId}`)
            .then(response => response.json())
            .then(data => {
                const select = document.getElementById("id_subcategory");
                select.innerHTML = '<option value="" selected disabled>Select subcategory...</option>';
                data.forEach(item => {
                    select.add(new Option(item.name, item.id));
                });
            });
    });
}