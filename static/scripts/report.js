
const generateSummaryBtn = document.getElementById('generate-summary-btn');
const summaryContainer = document.getElementById('summary-container');
const summaryLoading = document.getElementById('summary-loading');
const summaryContent = document.getElementById('summary-content');
const summaryError = document.getElementById('summary-error');
const summaryText = document.getElementById('summary-text');


generateSummaryBtn.addEventListener('click', async () => {
    // Get report ID from URL
    const reportId = window.location.pathname.split('/').pop();

    if (!reportId) {
        showError('Unable to determine report ID');
        return;
    }

    // Show loading state
    generateSummaryBtn.disabled = true;
    generateSummaryBtn.textContent = 'Generating...';
    summaryContainer.style.display = 'block';
    summaryLoading.style.display = 'block';
    summaryContent.style.display = 'none';
    summaryError.style.display = 'none';

    try {
        const response = await fetch('/generate_summary', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            credentials: 'same-origin',
            body: JSON.stringify({ report_id: parseInt(reportId) })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.message || 'Failed to generate summary');
        }

        if (data.success && data.summary) {
            // Display summary
            summaryText.textContent = data.summary;
            summaryLoading.style.display = 'none';
            summaryContent.style.display = 'block';
            summaryError.style.display = 'none';
            
            // Update button
            generateSummaryBtn.textContent = 'Summary Generated ✓';
            generateSummaryBtn.style.backgroundColor = '#4CAF50';
        } else {
            throw new Error(data.message || 'Unexpected response from server');
        }
    } catch (error) {
        showError(error.message || 'Failed to generate summary. Please try again.');
    } finally {
        generateSummaryBtn.disabled = false;
    }
});

function showError(message) {
    summaryLoading.style.display = 'none';
    summaryContent.style.display = 'none';
    summaryError.style.display = 'block';
    summaryError.textContent = `Error: ${message}`;
    summaryContainer.style.display = 'block';
    generateSummaryBtn.disabled = false;
    generateSummaryBtn.textContent = 'Generate Summary';
}

