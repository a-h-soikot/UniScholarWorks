
// Handle adding multiple authors
const authorsContainer = document.querySelector('.authors-container');
const addAuthorBtn = document.querySelector('.add-author-btn');

addAuthorBtn.addEventListener('click', function() {
    const newAuthorGroup = document.createElement('div');
    newAuthorGroup.className = 'author-input-group';
    newAuthorGroup.innerHTML = `
        <input type="text" name="authors[]" placeholder="Enter author name" required>
        <button type="button" class="remove-author-btn">
            <i class="fas fa-minus"></i>
        </button>
    `;
    authorsContainer.appendChild(newAuthorGroup);
    
    // Add event listener to the new remove button
    const removeBtn = newAuthorGroup.querySelector('.remove-author-btn');
    removeBtn.addEventListener('click', function() {
        authorsContainer.removeChild(newAuthorGroup);
    });
});

// Supervisor suggestions
const supervisorInput = document.getElementById('supervisor');
const suggestionsList = document.getElementById('supervisorSuggestions');
const supervisorIdInput = document.getElementById('supervisor_id');

supervisorInput.addEventListener('input', function() {
    const inputValue = this.value.toLowerCase();
    suggestionsList.innerHTML = '';
    
    if (inputValue.length < 2) {
        suggestionsList.style.display = 'none';
        return;
    }
    
    const matchingSupervisors = supervisors.filter(supervisor => 
        supervisor.name.toLowerCase().includes(inputValue)
    );
    
    if (matchingSupervisors.length > 0) {
        matchingSupervisors.forEach(supervisor => {
            const suggestion = document.createElement('div');
            suggestion.className = 'suggestion-item';
            suggestion.textContent = supervisor.name;
            suggestion.addEventListener('click', function() {
                supervisorInput.value = supervisor.name;
                supervisorIdInput.value = supervisor.teacher_id;
                suggestionsList.style.display = 'none';
            });
            suggestionsList.appendChild(suggestion);
        });
        suggestionsList.style.display = 'block';
    } else {
        suggestionsList.style.display = 'none';
    }
});

// Hide suggestions when clicking outside
document.addEventListener('click', function(e) {
    if (!supervisorInput.contains(e.target) && !suggestionsList.contains(e.target)) {
        suggestionsList.style.display = 'none';
    }
});

// File upload handling
const fileInput = document.getElementById('pdf_file');
const fileNameDisplay = document.querySelector('.file-name');
const fileUploadButton = document.querySelector('.file-upload-button');

fileUploadButton.addEventListener('click', function() {
    fileInput.click();
});

fileInput.addEventListener('change', function() {
    if (this.files.length > 0) {
        fileNameDisplay.textContent = this.files[0].name;
    } else {
        fileNameDisplay.textContent = 'No file selected';
    }
});

// Tags management
const tagInput = document.getElementById('tagInput'); // Text input field
const tagsList = document.getElementById('tagsList'); // Display selected tags
const tagsHiddenInput = document.getElementById('tags'); // Selected tags, but hidden

let tags = [];

// Function to update tags display and hidden input
function updateTags() {

    // Update hidden input for form submission
    tagsHiddenInput.value = tags.join(',');

    tagsList.innerHTML = '';
    
    tags.forEach((tag, index) => {
        const tagElement = document.createElement('span');
        tagElement.className = 'tag-item';
        tagElement.innerHTML = `
            ${tag}
            <span class="remove-tag" data-index="${index}">&times;</span>
        `;
        tagsList.appendChild(tagElement);
    });
    
    
    // Add event listeners to remove buttons
    document.querySelectorAll('.remove-tag').forEach(btn => {
        btn.addEventListener('click', function() {
            const index = parseInt(this.getAttribute('data-index'));
            tags.splice(index, 1); // Delete the tag
            updateTags();
        });
    });
}

// Handle tag input
tagInput.addEventListener('keydown', function(e) {
    if ((e.key === 'Enter' || e.key === ',') && this.value.trim()) {
        e.preventDefault();

        const inputTags = this.value.trim();

        if (!tags.includes(inputTags)) {
            tags.push(inputTags);
        }
        
        updateTags();
        this.value = ''; // Clear the tag input field
    }
});

// Function to add tag from suggested tags
function addTag (tagText) {
    if (!tags.includes(tagText)) {
        tags.push(tagText);
        updateTags();
    }
};